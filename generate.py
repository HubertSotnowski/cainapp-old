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
from torchvision import transforms
import numpy as np
from tqdm import tqdm
import utils
import glob
import cv2
from utils import quantize
from PIL import Image
def interpolation(batch_size=5, img_fmt="png", torch_device="cuda", temp_img = "frameseq/", GPUid=0, GPUid2=2, fp16=True, modelp="1.pth", TensorRT=False,  appupdate=False, app="hmm", dataloader="new",partialconv2d=True, funnynumber=1):    #torch.cuda.set_device(GPUid)
    ossystem=platform.system()
    if appupdate==True:
        import PyQt5.QtGui 
    print(ossystem)

    
    def update(progres="0"):         
        if int(progres) == int(int((bar/count*100)+1)):
            print("")
        else:
            progres = round((bar/count*100)+1)
        if appupdate==True:
            if count>200:
                app.progressBar_2.setValue(progres)
                q_im = quantize(out[0].data.mul(255))
                im = np.array(q_im.permute(1, 2, 0).cpu().numpy().astype(np.uint8))
                q_im = cv2.resize(cv2.cvtColor((cv2.cvtColor(np.array(im), cv2.COLOR_BGR2RGB)), cv2.COLOR_BGR2RGB), (448,256), interpolation = cv2.INTER_NEAREST)
                app.label_5.setPixmap( PyQt5.QtGui.QPixmap(PyQt5.QtGui.QImage(q_im.data, 448, 256, 1344,  PyQt5.QtGui.QImage.Format_RGB888)))
    def test():
        #set global things
        global savepath
        global images
        global fInd
        global framenum
        global progres
        global bar
        global count
        global out1
        global out2
        global fpos
        global meta
        global out
        global b
        global tsave
        #set important things
        var3=2
        bar=0
        count=0
        framenum=0
        progres=0
        num=0
        T = transforms.ToTensor()
        var1=sorted(glob.glob(f"{temp_img}/*.*"))
        for file in var1:
            count+=1
        count=count/batch_size
        #rename files
        startnum=0
        for file in var1:
            os.rename(file,temp_img + "/"+ str(startnum).zfill(6)+".0.png")
            startnum+=1
            
        ### load model
        torch.set_default_tensor_type(torch.cuda.HalfTensor)
        torch.cuda.device(GPUid)
        device = torch.device(torch_device)
        from model.cain import CAIN
        model = CAIN(depth=3)
        checkpoint = torch.load(modelp)
        model.load_state_dict(checkpoint)
        model.cuda()
        ### list frames
        
            
        for file in sorted(glob.glob(f"{temp_img}/*.*")):
            try:
                frames+=[file]
            except:
                frames=[file]
            count+=1
        for b in frames:
            print(b)
        ###render
        with torch.no_grad():
            while num<count-4:
                if  os.path.exists(frames[num+4]) ==True:
                    frame1=Image.open(frames[num])
                    frame2=Image.open(frames[num+1]) 
                    frame3=Image.open(frames[num+2])
                    frame22=Image.open(frames[num+3]) 
                    frame32=Image.open(frames[num+4])
                    frame1=T(frame1)
                    frame2=T(frame2)
                    frame3=T(frame3)
                    frame22=T(frame22)
                    frame32=T(frame32)
                    im1=torch.stack((frame1,frame3),dim=0)
                    im2=torch.stack((frame2,frame22),dim=0)
                    im3=torch.stack((frame3,frame32),dim=0)
                    s=time.time()
                    out1,out2,_=model(im1.cuda(),im2.cuda(),im3.cuda())
                    e=time.time()
                    print(e-s)
                    def save(saveout1,saveout2,saveout3,saveout4,num):
                        utils.save_image(saveout1, temp_img+"/"+str(num).zfill(6)+".5.png")
                        utils.save_image(saveout2, temp_img+"/"+str(num+1).zfill(6)+".5.png")
                        utils.save_image(saveout3, temp_img+"/"+str(num+2).zfill(6)+".5.png")
                        utils.save_image(saveout4, temp_img+"/"+str(num+3).zfill(6)+".5.png")
                    tsave = threading.Thread(target=save,args=(out1[0],out2[0],out1[1],out2[1],num))
                    tsave.start()
                    num+=4
                    e=time.time()
                    print(((e-s)))
                    print(num)

    test()




#
def main():
    interpolation()
    #test()
    #test()
    #test()

if __name__ == "__main__":
    main()
