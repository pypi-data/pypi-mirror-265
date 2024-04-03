import torch
import json

from mmengine.config import Config
from mmengine.runner import Runner
from split_utils import SplitEncoderDecoder


def setup_config():
    # setup the config file
    cfg = Config.fromfile('segmentation/swin-tiny-patch4-window7-in1k-pre_upernet_8xb2-160k_ade20k-512x512.py')

    # set the data_root of the config file
    data_root = 'data/ade/ADEChallengeData2016'
    cfg.data_root = data_root
    cfg.test_dataloader.dataset.data_root = data_root
    cfg.train_dataloader.dataset.data_root = data_root
    cfg.val_dataloader.dataset.data_root = data_root


    train_pipeline = [{'type': 'LoadImageFromFile'},
                    {'reduce_zero_label': True, 'type': 'LoadAnnotations'},
                    {'keep_ratio': True,
                    'ratio_range': (0.5, 2.0),
                    'scale': (2048, 1024), # (2048, 512)
                    'type': 'RandomResize'},
                    {'cat_max_ratio': 0.75, 'crop_size': (512, 512), 'type': 'RandomCrop'},
                    {'prob': 0.5, 'type': 'RandomFlip'},
                    {'type': 'PhotoMetricDistortion'},
                    {'type': 'PackSegInputs'}]

    cfg.train_dataloader.dataset.pipeline = train_pipeline

    cfg.dump('segmentation/swin-tiny-patch4-window7-in1k-pre_upernet_8xb2-160k_ade20k-512x512_modified.py')

    config_file = "segmentation/swin-tiny-patch4-window7-in1k-pre_upernet_8xb2-160k_ade20k-512x512_modified.py"
    checkpoint_file = 'segmentation/upernet_swin_tiny_patch4_window7_512x512_160k_ade20k_pretrain_224x224_1K_20210531_112542-e380ad3e.pth'
    return cfg, config_file, checkpoint_file



def main():
    cfg, config_file, checkpoint_file = setup_config()

    model = SplitEncoderDecoder.create_from_cfg_and_checkpoint(config_file, checkpoint_file)
    if torch.cuda.is_available():
        model.to('cuda')
    model.zero_grad()
    model.eval()

    dataloader = Runner.build_dataloader(cfg.val_dataloader)
    val_eval = Runner.build_evaluator(None, cfg.val_evaluator)
    setattr(val_eval,'dataset_meta', dataloader.dataset.metainfo)

    for i, data in enumerate(dataloader):
        print(f"Processing image {i}")
        features = model.feature_frontend(data)
        result_backend_inference = model.backend_inference(features)
        val_eval.process(result_backend_inference)
        # eval_result = val_eval.offline_evaluate(result_backend_inference)
        # eval_results.append(eval_result)
        # result_backend_raw = model.backend_raw(data)
        print(f"Processed image {i}")

    result = val_eval.evaluate(len(dataloader))
    print(result)
    # Open a file for writing in text mode (use 'w' for writing)
    with open('result.json', 'w') as json_file:
        # Convert the dictionary to a JSON string with human-readable indentation
        json_string = json.dumps(result, indent=4)

        # Write the JSON string to the file
        json_file.write(json_string)

if __name__ == '__main__':
    main()

    