import torch
from collections import OrderedDict
from typing import Union
from mmdet.models.backbones.swin import SwinTransformer
from mmdet.models.detectors.two_stage import TwoStageDetector
from mmdet.structures import DetDataSample
from mmdet.structures.mask import encode_mask_results
from mmengine.config import Config, ConfigDict
from mmdet.apis import init_detector
from copy import deepcopy
from .legacy import RepPointsV2MaskDetector, build_detector, convert_swin_checkpoint_file
from mmengine.runner import load_checkpoint

from mmseg.models.backbones.swin import SwinTransformer as SwinTransformerSeg
from mmseg.models.segmentors import EncoderDecoder


class SplitSwinTransformer(SwinTransformer):
    def __init__(self, **kwargs):
        if 'type' in kwargs:
            del kwargs['type']
        super().__init__(**kwargs)
        # super(SplitSwinTransformer, self).__init__(**kwargs)
        
    @classmethod
    def create_from_swin(cls, swin_instance):
        split_instance = cls(**swin_instance.__dict__)
        split_instance.load_state_dict(swin_instance.state_dict)
        # Return the new instance of Sub
        return split_instance
    
    @classmethod
    def create_from_instance_and_cfg(cls, swin_instance, cfg):
        split_instance = cls(**cfg.model.backbone)
        split_instance.load_state_dict(swin_instance.state_dict())
        # Return the new instance of Subclass
        return split_instance
    
    def split_forward(self, x, hw_shape=0, outs=[], input_layer=0, output_layer=None):
        if input_layer == 0:
            x, hw_shape = self.patch_embed(x)

            if self.use_abs_pos_embed:
                x = x + self.absolute_pos_embed
            x = self.drop_after_pos(x)

        for i, stage in enumerate(self.stages):
            if i < input_layer:
                continue

            x, hw_shape, out, out_hw_shape = stage(x, hw_shape)
            # print(f'x: {x.shape}, hw_shape: {hw_shape}, out: {out.shape}, out_hw_shape: {out_hw_shape}')
            if i in self.out_indices:
                norm_layer = getattr(self, f'norm{i}')
                out = norm_layer(out)
                out = out.view(-1, *out_hw_shape,
                                self.num_features[i]).permute(0, 3, 1,
                                                                2).contiguous()
                outs = outs + [out]
            if i == output_layer:
                return x, hw_shape, outs

        return outs
    def split_forward_v2(self, x, hw_shape=0, outs=[], input_layer=0, output_layer=None):
        if input_layer == 0:
            x, hw_shape = self.patch_embed(x)

            if self.use_abs_pos_embed:
                x = x + self.absolute_pos_embed
            x = self.drop_after_pos(x)

        for i, stage in enumerate(self.stages):
            if i < input_layer-1:
                continue
            if i == input_layer-1:
                out = outs[-1]
                outs = outs[:-1]
                out_hw_shape = hw_shape
                if stage.downsample!=None:
                    x,hw_shape = stage.downsample(out, out_hw_shape)
                else:
                    x,hw_shape = out, out_hw_shape
            else:
                x, hw_shape, out, out_hw_shape = stage(x, hw_shape)
            # print(f'x: {x.shape}, hw_shape: {hw_shape}, out: {out.shape}, out_hw_shape: {out_hw_shape}')
            if i == output_layer:
                return out_hw_shape, outs + [out]
            if i in self.out_indices:
                norm_layer = getattr(self, f'norm{i}')
                out = norm_layer(out)
                out = out.view(-1, *out_hw_shape,
                                self.num_features[i]).permute(0, 3, 1,
                                                                2).contiguous()
                outs = outs + [out]
            

        return outs
    
class SplitTwoStageDetector(TwoStageDetector):
    def __init__(self, cut_point=0, **kwargs):
        if 'type' in kwargs:
            del kwargs['type']
        super().__init__(**kwargs)
        self.cut_point = cut_point

    @classmethod
    def create_from_cfg_and_checkpoint(cls, cfg_path, checkpoint_path, device = 'cpu', cut_point=1):
        model_init = init_detector(cfg_path, checkpoint_path, device=device)
        cfg = Config.fromfile(cfg_path)
        model = cls.create_from_instance_and_cfg(model_init, cfg, cut_point = cut_point )
        # model.prepare_preprocessing()
        return model


    @classmethod
    def create_from_instance_and_cfg(cls, model_instance, cfg, cut_point=0):
        split_instance = cls(cut_point = cut_point, **cfg.model)
        split_instance.load_state_dict(model_instance.state_dict())
        # Return the new instance of Subclass
        split_instance.cfg = model_instance.cfg
        split_instance.backbone = SplitSwinTransformer.create_from_instance_and_cfg(split_instance.backbone, cfg)
        split_instance.prepare_preprocessing()
        return split_instance
    
    def prepare_preprocessing(self):
        self.frontend_preprocessor = deepcopy(self.data_preprocessor)
        self.data_preprocessor = TwoInputIdentity()

    def set_cfg(self, model_instance):
        self.cfg = model_instance.cfg
        
    def extract_feat(self, batch_inputs):
        """Extract features.

        Args:
            batch_inputs (Tensor): Image tensor with shape (N, C, H ,W).

        Returns:
            tuple[Tensor]: Multi-level features that may have
            different resolutions.
        """
        # x, hw_shape, outputs = self.backbone.split_forward(batch_inputs, outs=[], output_layer=1)
        # print("splitting at layer 1")
        # print(batch_inputs)
        if isinstance(batch_inputs, dict):
            x = batch_inputs["x"] if "x" in batch_inputs else None
            hw_shape = batch_inputs["hw_shape"]
            outs = batch_inputs["outs"]
        else:
            x = batch_inputs
            hw_shape = 0
            outs = []
        x = self.backbone.split_forward_v2(x, hw_shape, outs=outs, input_layer=self.cut_point)
        
        if self.with_neck:
            x = self.neck(x)
        return x

    def feature_frontend(self, data):
        
        if isinstance(data, dict):
            data = self.frontend_preprocessor(data)
            x = data['inputs']
        else:
            x = data

        if self.cut_point>0:
            out =  self.backbone.split_forward_v2(x, output_layer = self.cut_point-1)
            data['inputs'] = {"hw_shape": out[0],
                              "outs": out[1]}
        return data       
    
    def backend_inference(self, data):
        return self.test_step(data)

    def backend_raw(self, data):
        return self(data['inputs'], data['data_samples'])
    
    def backend_loss(self, data):
        return self.parse_losses(self.loss(data['inputs'], data['data_samples']))

class SplitRepPointsV2MaskDetector(RepPointsV2MaskDetector):
    def __init__(self, cut_point=0, **kwargs):
        if 'type' in kwargs:
            del kwargs['type']
        super().__init__(**kwargs)
        self.cut_point = cut_point

    @classmethod
    def create_from_cfg_and_checkpoint(cls, cfg_path, checkpoint_path, device = 'cpu', cut_point=1):
        cfg = Config.fromfile(cfg_path)
        # print(cfg.model)
        if not 'converted' in checkpoint_path:
            dst = checkpoint_path.replace('.pth', '_converted.pth')
            checkpoint_path = convert_swin_checkpoint_file(checkpoint_path, dst)
        
        model_init = init_detector(cfg_path, checkpoint_path, device=device)
        model = cls.create_from_instance_and_cfg(model_init, cfg, cut_point = cut_point)
        # model.prepare_preprocessing()
        return model


    @classmethod
    def create_from_instance_and_cfg(cls, model_instance, cfg, cut_point=0):
        split_instance = cls(cut_point = cut_point, **cfg.model)
        checkpoint = model_instance.state_dict()
        # checkpoint.backbone = swin_converter_inverse(checkpoint.backbone)
        split_instance.load_state_dict(checkpoint)
        # Return the new instance of Subclass
        split_instance.cfg = model_instance.cfg
        split_instance.backbone = SplitSwinTransformer.create_from_instance_and_cfg(split_instance.backbone, cfg)
        split_instance.prepare_preprocessing()
        return split_instance
    
    def prepare_preprocessing(self):
        self.frontend_preprocessor = deepcopy(self.data_preprocessor)
        self.data_preprocessor = TwoInputIdentity()

    def set_cfg(self, model_instance):
        self.cfg = model_instance.cfg
        
    def extract_feat(self, batch_inputs):
        """Extract features.

        Args:
            batch_inputs (Tensor): Image tensor with shape (N, C, H ,W).

        Returns:
            tuple[Tensor]: Multi-level features that may have
            different resolutions.
        """
        # x, hw_shape, outputs = self.backbone.split_forward(batch_inputs, outs=[], output_layer=1)
        # print("splitting at layer 1")
        # print(batch_inputs)
        if isinstance(batch_inputs, dict):
            x = batch_inputs["x"] if "x" in batch_inputs else None
            hw_shape = batch_inputs["hw_shape"]
            outs = batch_inputs["outs"]
        else:
            x = batch_inputs
            hw_shape = 0
            outs = []
        x = self.backbone.split_forward_v2(x, hw_shape, outs=outs, input_layer=self.cut_point)
        
        if self.with_neck:
            x = self.neck(x)
        return x

    def feature_frontend(self, data):
        
        if isinstance(data, dict):
            data = self.frontend_preprocessor(data)
            x = data['inputs']
        else:
            x = data

        if self.cut_point>0:
            out =  self.backbone.split_forward_v2(x, output_layer = self.cut_point-1)
            data['inputs'] = {"hw_shape": out[0],
                              "outs": out[1]}
        return data       
    
    def backend_inference(self, data):
        # if isinstance(data['data_samples'][0], DetDataSample):
        #     img_metas = [ds.metainfo for ds in data['data_samples']]
        result = self.val_step(data)
        # if isinstance(result[0], tuple):
        #     result = [(bbox_results, encode_mask_results(mask_results))
        #               for bbox_results, mask_results in result]
        # data['data_samples'] = self.add_pred_to_datasample(
        #     data['data_samples'], props)
        return result #data['data_samples']

    def backend_raw(self, data):
        return self(data['inputs'], data['data_samples'])
    
    def backend_loss(self, data):
        if isinstance(data['data_samples'][0], DetDataSample):
            img_metas = []
            gt_bboxes = []
            gt_labels = []
            gt_bboxes_ignore = []
            gt_sem_map= []
            gt_sem_weights = []
            gt_masks = []
            for ds in data['data_samples']:
                img_metas.append(ds.metainfo)
                gt_bboxes.append(ds.gt_instances.bboxes)
                gt_labels.append(ds.gt_instances.labels)
                gt_bboxes_ignore.append(ds.ignored_instances.bboxes)
                gt_masks.append(ds.gt_instances.masks)
                gt_sem_map.append(ds.gt_sem.sem_map)
                gt_sem_weights.append(ds.gt_sem.sem_weights)
        return self.parse_losses(self.loss(data['inputs'], img_metas, gt_bboxes, gt_labels, 
                                           gt_bboxes_ignore = gt_bboxes_ignore, 
                                           gt_masks = gt_masks, 
                                           gt_sem_map = gt_sem_map,
                                           gt_sem_weights = gt_sem_weights))


# cfg = Config.fromfile('obj_det/mask-rcnn_swin-t-p4-w7_fpn_1x_coco.py')
# model.backbone = SplitSwinTransformer.create_from_instance_and_cfg(model.backbone, cfg)

class TwoInputIdentity(torch.nn.Module):
    def __init__(self):
        super(TwoInputIdentity,self).__init__()
    def forward(self, x, bol):
        return x


class SplitSwinTransformerSeg(SwinTransformerSeg):
    def __init__(self, **kwargs):
        if 'type' in kwargs:
            del kwargs['type']
        super().__init__(**kwargs)

    @classmethod
    def create_from_swin(cls, swin_instance):
        split_instance = cls(**swin_instance.__dict__)
        split_instance.load_state_dict(swin_instance.state_dict)
        # Return the new instance of Sub
        return split_instance
    
    @classmethod
    def create_from_instance_and_cfg(cls, swin_instance, cfg):
        split_instance = cls(**cfg.model.backbone)
        split_instance.load_state_dict(swin_instance.state_dict())
        # Return the new instance of Subclass
        return split_instance
    
    def split_forward(self, x, hw_shape=0, outs=[], input_layer=0, output_layer=None):
        if input_layer == 0:
            x, hw_shape = self.patch_embed(x)

            if self.use_abs_pos_embed:
                x = x + self.absolute_pos_embed
            x = self.drop_after_pos(x)

        for i, stage in enumerate(self.stages):
            if i < input_layer:
                continue

            x, hw_shape, out, out_hw_shape = stage(x, hw_shape)
            # print(f'x: {x.shape}, hw_shape: {hw_shape}, out: {out.shape}, out_hw_shape: {out_hw_shape}')
            if i in self.out_indices:
                norm_layer = getattr(self, f'norm{i}')
                out = norm_layer(out)
                out = out.view(-1, *out_hw_shape,
                                self.num_features[i]).permute(0, 3, 1,
                                                                2).contiguous()
                outs = outs + [out]
            if i == output_layer:
                return x, hw_shape, outs

        return outs
    
    def split_forward_v2(self, x, hw_shape=0, outs=[], input_layer=0, output_layer=None):
        if input_layer == 0:
            x, hw_shape = self.patch_embed(x)

            if self.use_abs_pos_embed:
                x = x + self.absolute_pos_embed
            x = self.drop_after_pos(x)

        for i, stage in enumerate(self.stages):
            if i < input_layer-1:
                continue
            if i == input_layer-1:
                out = outs[-1]
                outs = outs[:-1]
                out_hw_shape = hw_shape
                if stage.downsample!=None:
                    x,hw_shape = stage.downsample(out, out_hw_shape)
                else:
                    x,hw_shape = out, out_hw_shape
            else:
                x, hw_shape, out, out_hw_shape = stage(x, hw_shape)
            # print(f'x: {x.shape}, hw_shape: {hw_shape}, out: {out.shape}, out_hw_shape: {out_hw_shape}')
            if i == output_layer:
                return out_hw_shape, outs + [out]
            if i in self.out_indices:
                norm_layer = getattr(self, f'norm{i}')
                out = norm_layer(out)
                out = out.view(-1, *out_hw_shape,
                                self.num_features[i]).permute(0, 3, 1,
                                                                2).contiguous()
                outs = outs + [out]
        return outs
    


class SplitEncoderDecoder(EncoderDecoder):
    def __init__(self, cut_point=0, **kwargs):
        if 'type' in kwargs:
            del kwargs['type']
        super().__init__(**kwargs)
        self.cut_point = cut_point

    @classmethod
    def create_from_cfg_and_checkpoint(cls, cfg_path, checkpoint_path, device = 'cpu'):
        model_init = init_detector(cfg_path, checkpoint_path, device=device)
        cfg = Config.fromfile(cfg_path)
        model = cls.create_from_instance_and_cfg(model_init, cfg, cut_point=1)
        # model.prepare_preprocessing()
        return model


    @classmethod
    def create_from_instance_and_cfg(cls, model_instance, cfg, cut_point=0):
        split_instance = cls(cut_point = cut_point, **cfg.model)
        split_instance.load_state_dict(model_instance.state_dict())
        # Return the new instance of Subclass
        split_instance.cfg = model_instance.cfg
        split_instance.backbone = SplitSwinTransformerSeg.create_from_instance_and_cfg(split_instance.backbone, cfg)
        split_instance.prepare_preprocessing()
        return split_instance
    
    def prepare_preprocessing(self):
        self.frontend_preprocessor = self.data_preprocessor
        self.data_preprocessor = TwoInputIdentity()

    def set_cfg(self, model_instance):
        self.cfg = model_instance.cfg

    def extract_feat(self, batch_inputs):
        """Extract features.

        Args:
            batch_inputs (Tensor): Image tensor with shape (N, C, H ,W).

        Returns:
            tuple[Tensor]: Multi-level features that may have
            different resolutions.
        """
        # x, hw_shape, outputs = self.backbone.split_forward(batch_inputs, outs=[], output_layer=1)
        # print("splitting at layer 1")
        if isinstance(batch_inputs, dict):
            x = batch_inputs["x"] if "x" in batch_inputs else None
            hw_shape = batch_inputs["hw_shape"]
            outs = batch_inputs["outs"]
        else:
            x = batch_inputs
            hw_shape = 0
            outs = []
        x = self.backbone.split_forward_v2(x, hw_shape, outs=outs, input_layer=self.cut_point)
        
        if self.with_neck:
            x = self.neck(x)
        return x
    
    def feature_frontend(self, data):
        
        if isinstance(data, dict):
            data = self.frontend_preprocessor(data)
            x = data['inputs']
        else:
            x = data

        if self.cut_point>0:
            out =  self.backbone.split_forward_v2(x, output_layer = self.cut_point-1)
            data['inputs'] = {"hw_shape": out[0],
                              "outs": out[1]}
        return data       
    
    def backend_inference(self, data):
        return self.test_step(data)

    def backend_raw(self, data):
        return self(data['inputs'], data['data_samples'])
    
    def backend_loss(self, data):
        return self.parse_losses(self.loss(data['inputs'], data['data_samples']))
    
    def swap_preprocessor(self):
        temp = self.data_preprocessor
        self.data_preprocessor = self.frontend_preprocessor
        self.frontend_preprocessor = temp

    def set_cut_point(self, cut_point):
        self.cut_point = cut_point

# TODO: this get_mean_metrics function does not seem to be correct
# def get_mean_metrics(metrics_list):
#     # Initialize sums for each metric
#     sum_aAcc = 0
#     sum_mIoU = 0
#     sum_mAcc = 0

#     # Iterate through the list of dictionaries
#     for item in metrics_list:
#         sum_aAcc += item['aAcc']
#         sum_mIoU += item['mIoU']
#         sum_mAcc += item['mAcc']

#     # Calculate the mean for each metric
#     mean_aAcc = sum_aAcc / len(metrics_list)
#     mean_mIoU = sum_mIoU / len(metrics_list)
#     mean_mAcc = sum_mAcc / len(metrics_list)

#     # Create a dictionary to store the means
#     mean_metrics = {
#         'mean_aAcc': mean_aAcc,
#         'mean_mIoU': mean_mIoU,
#         'mean_mAcc': mean_mAcc
#     }

#     return mean_metrics


def swin_converter_inverse(ckpt):

    new_ckpt = OrderedDict()

    def correct_unfold_reduction_order(x):
        out_channel, in_channel = x.shape
        x = x.reshape(out_channel, 4, in_channel // 4)
        x = x[:, [0, 2, 1, 3], :].transpose(1,
                                            2).reshape(out_channel, in_channel)
        return x
    
    def correct_reverse_unfold_reduction_order(x):
        out_channel, in_channel = x.shape
        x = x.reshape(out_channel, in_channel // 4, 4)
        x = x[:, :, [0, 2, 1, 3]].transpose(1,
                                            2).reshape(out_channel, in_channel)
        return x

    def correct_unfold_norm_order(x):
        in_channel = x.shape[0]
        x = x.reshape(4, in_channel // 4)
        x = x[[0, 2, 1, 3], :].transpose(0, 1).reshape(in_channel)
        return x
    
    def correct_reverse_unfold_norm_order(x):
        in_channel = x.shape[0]
        x = x.reshape(in_channel // 4, 4)
        x = x[:, [0, 2, 1, 3]].transpose(0, 1).reshape(in_channel)
        return x

    for k, v in ckpt.items():
        if k.startswith('head'):
            continue
        elif k.startswith('backbone.stages'):
            new_v = v
            if 'attn.' in k:
                # new_k = k.replace('attn.', 'attn.w_msa.')
                new_k = k.replace('attn.w_msa.', 'attn.')
            elif 'ffn.layers' in k:
                if 'ffn.layers.0.0.' in k:
                    # new_k = k.replace('mlp.fc1.', 'ffn.layers.0.0.')
                    new_k = k.replace('ffn.layers.0.0.', 'mlp.fc1.' )
                elif 'ffn.layers.1.' in k:
                    # new_k = k.replace('mlp.fc2.', 'ffn.layers.1.')
                    new_k = k.replace('ffn.layers.1.', 'mlp.fc2.')
                else:
                    new_k = k.replace('ffn.', 'mlp.')
            elif 'downsample' in k:
                new_k = k
                if 'reduction.' in k:
                    new_v = correct_reverse_unfold_reduction_order(v)
                elif 'norm.' in k:
                    new_v = correct_reverse_unfold_norm_order(v)
            else:
                new_k = k
            # new_k = new_k.replace('layers', 'stages', 1)
            new_k = new_k.replace('stages', 'layers', 1)
        elif k.startswith('backbone.patch_embed'):
            new_v = v
            if 'proj' in k:
                # new_k = k.replace('proj', 'projection')
                new_k = k.replace('projection', 'proj')
            else:
                new_k = k
        else:
            new_v = v
            new_k = k

        new_k = new_k.replace('backbone.', '')
        # new_k = new_k.replace('stages.', '')
        new_ckpt[new_k] = new_v
        

    return new_ckpt


def correct_unfold_reduction_order(x):
        out_channel, in_channel = x.shape
        x = x.reshape(out_channel, 4, in_channel // 4)
        x = x[:, [0, 2, 1, 3], :].transpose(1,
                                            2).reshape(out_channel, in_channel)
        return x
    
def correct_reverse_unfold_reduction_order(x):
    out_channel, in_channel = x.shape
    x = x.reshape(out_channel, in_channel // 4, 4)
    x = x[:, :, [0, 2, 1, 3]].transpose(1,
                                        2).reshape(out_channel, in_channel)
    return x

def correct_unfold_norm_order(x):
        in_channel = x.shape[0]
        x = x.reshape(4, in_channel // 4)
        x = x[[0, 2, 1, 3], :].transpose(0, 1).reshape(in_channel)
        return x
    
def correct_reverse_unfold_norm_order(x):
    in_channel = x.shape[0]
    x = x.reshape(in_channel // 4, 4)
    x = x[:, [0, 2, 1, 3]].transpose(0, 1).reshape(in_channel)
    return x

def main():
    x = torch.rand(32, 16)
    y = correct_unfold_reduction_order(x)
    y2 = correct_reverse_unfold_reduction_order(y)

    print(torch.all(x == y2))

    x = torch.rand(16)
    y = correct_unfold_norm_order(x)
    y2 = correct_reverse_unfold_norm_order(y)

    print(torch.all(x == y2))

def get_train_pipeline_cfg(cfg: Union[str, ConfigDict]) -> ConfigDict:
    """Get the test dataset pipeline from entire config.

    Args:
        cfg (str or :obj:`ConfigDict`): the entire config. Can be a config
            file or a ``ConfigDict``.

    Returns:
        :obj:`ConfigDict`: the config of test dataset.
    """
    if isinstance(cfg, str):
        cfg = Config.fromfile(cfg)

    def _get_train_pipeline_cfg(dataset_cfg):
        if 'pipeline' in dataset_cfg:
            return dataset_cfg.pipeline
        # handle dataset wrapper
        elif 'dataset' in dataset_cfg:
            return _get_train_pipeline_cfg(dataset_cfg.dataset)
        # handle dataset wrappers like ConcatDataset
        elif 'datasets' in dataset_cfg:
            return _get_train_pipeline_cfg(dataset_cfg.datasets[0])

        raise RuntimeError('Cannot find `pipeline` in `train_dataloader`')

    return _get_train_pipeline_cfg(cfg.train_dataloader.dataset)

# if __name__ == '__main__':
#     main()