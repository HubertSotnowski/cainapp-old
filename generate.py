import os
import sys
import time
import copy
import shutil
import random
import threading
import torch
import platform
import video
import os
import numpy as np
from tqdm import tqdm
import utils



def interpolation(batch_size=5, img_fmt="png", torch_device="cuda", temp_img = "frameseq/", GPUid=0, GPUid2=2, fp16=True, modelp="1.pth", TensorRT=True):
    #torch.cuda.set_device(GPUid)
    ossystem=platform.system()
    print(ossystem)
    torch.cuda.device(GPUid)
    device = torch.device(torch_device)
    torch.backends.cudnn.enabled = True
    torch.backends.cudnn.benchmark = True
    torch.manual_seed(5325)
    torch.cuda.manual_seed(5325)
    if TensorRT==True:
        from torch2trt import TRTModule
        model_trt = TRTModule()
        model_trt.load_state_dict(torch.load(modelp))
    else:
        from model.cain import CAIN
        model = CAIN(depth=3)
        checkpoint = torch.load(modelp)
        model.load_state_dict(checkpoint)
        model.cuda().half() 
    if ossystem=='Linux':
        def save():
            utils.save_image(out[b], temp_img+"/"+savepath)
    else:
        def save():
            utils.save_image(out[b], temp_img[:-6]+savepath)

    def test():
        global savepath
        global images
        global fInd
        global fpos
        global meta
        global out
        global b
        global tsave
        ##### Load Dataset #####
        test_loader = utils.load_dataset(
            temp_img, batch_size, batch_size, 0, img_fmt=img_fmt)
        #model.eval()

        t = time.time()
        with torch.no_grad():
            for i, (images, meta) in enumerate(tqdm(test_loader)):

                # Build input batch
                im1, im2 = images[0].to(device).half(), images[1].to(device).half()

                # Forward
                if TensorRT==True:
                    out, _ = model_trt(im1, im2)
                else:
                    out, _ = model(im1, im2)
                for b in range(images[0].size(0)):
                    paths = meta['imgpath'][0][b].split('/')
                    fp = temp_img
                    fp = os.path.join(paths[-1][:-4])   # remove '.png' extension

                    # Decide float index
                    i1_str = paths[-1][:-4]
                    i2_str = meta['imgpath'][1][b].split('/')[-1][:-4]
                    try:
                        i1 = float(i1_str.split('_')[-1])
                    except ValueError:
                        i1 = 0.0
                    try:
                        i2 = float(i2_str.split('_')[-1])
                        if i2 == 0.0:
                            i2 = 1.0
                    except ValueError:
                        i2 = 1.0
                    fpos = max(0, fp.rfind('_'))
                    fInd = (i1 + i2) / 2
                    savepath = "%s_%06f.%s" % (fp[:fpos], fInd, img_fmt)
                    tsave = threading.Thread(target=save)
                    tsave.start()

    #
    
    test()
    video.clean()





#
def main():
    interpolation()
    #test()
    #test()
    #test()

if __name__ == "__main__":
    main()
