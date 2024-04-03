from mim import install 
                            
def install_mmdet():
    install(['mmengine'])
    install(['mmcv>=2.0.0'])
    install(['mmdet==3.3.0'])
if __name__ == '__main__':
    install_mmdet()