import os
import sys
import time
import copy
import shutil
import random
import threading
import torch
import platform
import os
import numpy as np
from tqdm import tqdm
import utils
import glob
import cv2
import newloader
from utils import quantize
from PIL import Image
def interpolation(batch_size=5, img_fmt="png", torch_device="cuda", temp_img = "frameseq/", GPUid=0, GPUid2=2, fp16=True, modelp="1.pth", TensorRT=True,  appupdate=False, app="hmm", dataloader="new"):    #torch.cuda.set_device(GPUid)
    ossystem=platform.system()
    if appupdate==True:
        import PyQt5.QtGui 
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
        if fp16==True:
            model.cuda().half() 
        else:
            model.cuda()
        
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
            temp_img, batch_size, batch_size, 0, img_fmt=img_fmt, dataloader=dataloader)
        #model.eval()
        bar=0
        count=0
        progres=0
        for file in glob.glob(f"{temp_img}/*.*"):
            count+=1
        count=count/batch_size
        t = time.time()
        with torch.no_grad():
            for i, (images, meta) in enumerate(tqdm(test_loader)):
                # Build input batch
                if fp16==True:
                    im1, im2 = images[0].to(device).half(), images[1].to(device).half()
                else:
                    im1, im2 = images[0].to(device), images[1].to(device)
                

                # Forward
                if TensorRT==True:
                    out, _ = model_trt(im1, im2)
                else:
                    out, _ = model(im1, im2)
                bar+=1
                
                if int(progres) == int(int((bar/count*100)+1)):
                    print("not updating")
                else:
                    progres = round((bar/count*100)+1)
                    print("updated")
                    if appupdate==True:
                        app.progressBar_2.setValue(progres)
                        q_im = quantize(out[0].data.mul(255))
                        im = np.array(q_im.permute(1, 2, 0).cpu().numpy().astype(np.uint8))
                        q_im = cv2.resize(cv2.cvtColor((cv2.cvtColor(np.array(im), cv2.COLOR_BGR2RGB)), cv2.COLOR_BGR2RGB), (448,256), interpolation = cv2.INTER_NEAREST)
                        app.label_5.setPixmap( PyQt5.QtGui.QPixmap(PyQt5.QtGui.QImage(q_im.data, 448, 256, 1344,  PyQt5.QtGui.QImage.Format_RGB888))  )
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


         
    
    test()
    if dataloader=="new":
        newloader.clean()
    try:
        del model
    except:
        del model_trt



#
def main():
    interpolation()
    #test()
    #test()
    #test()

if __name__ == "__main__":
    main()
