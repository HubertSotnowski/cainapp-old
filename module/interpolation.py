import platform
import torch
from torchvision import transforms
import subprocess as sp
import kornia
import time
import concurrent.futures
from PIL import Image
import os
try:
    from PyQt6.QtWidgets import *
except:
    from PyQt5.QtWidgets import *
import cv2
import numpy as np
def quantize(img, rgb_range=255):
    return img.mul(255 / rgb_range).clamp(0, 255).round()
transform = transforms.ToTensor()
#
torch.no_grad()
def toffmpeg(out1,output,proc):
    if output:
        print("1")
        try:

            out1=out1.permute(1, 2, 0).numpy().astype(np.uint8)
            print(out1.shape)
            proc.stdin.write(out1.tobytes())
        except Exception as e:
            print(e)
    else:
        print("2")
        out1=np.array(out1)
        proc.stdin.write(out1.tobytes())



def save(argssave):
    out,proc,padding,lowres,x1,x2,yuv=argssave

    out.float().cpu()
    try:
        out=quantize(out.float().data.mul(255))
    except Exception as e:
        print(e)

    if lowres:
        
        out1,out2,out3,out4,out5=out
        del out
        frame1,frame2,frame3,frame4,frame5=x1
        
        frame2,frame3,frame4,frame5,frame6=x2

        toffmpeg(frame1,False,proc)
        try:
            toffmpeg(out1,True,proc)
        except Exception as e:
            print(e)
        
        print("tak")
        toffmpeg(frame2,False,proc)
        toffmpeg(out2,True,proc)

        toffmpeg(frame3,False,proc)
        toffmpeg(out3,True,proc)

        toffmpeg(frame4,False,proc)
        toffmpeg(out4,True,proc)

        toffmpeg(frame5,False,proc) 
        toffmpeg(out5,True,proc)
        
    else:
        out1,out2=out
        del out
        frame1,frame3=x1
        frame2,frame4=x2
        try:
        
            toffmpeg(frame1,False,proc)
            toffmpeg(out1,True,proc)
            toffmpeg(frame2,False,proc)
        except Exception as e:
            print(e)
        toffmpeg(out2,True,proc)
        toffmpeg(frame3,False,proc)
def read(argsread):
    video,im1,lowres,padding,yuv=argsread
    frame1 = im1
    padding_w,padding_h=padding
    ret,frame2 = video.read()
    ret,frame3 = video.read()
    if lowres:
        ret,frame4 = video.read()
        ret,frame5 = video.read()
        ret,frame6 = video.read()
        if ret==False:
            return None
        frame2 = cv2.copyMakeBorder(frame2, int(padding_h/2), int(padding_h/2), int(padding_w/2), int(padding_w/2), cv2.BORDER_REFLECT)
        frame3 = cv2.copyMakeBorder(frame3, int(padding_h/2), int(padding_h/2), int(padding_w/2), int(padding_w/2), cv2.BORDER_REFLECT)
        frame4 = cv2.copyMakeBorder(frame4, int(padding_h/2), int(padding_h/2), int(padding_w/2), int(padding_w/2), cv2.BORDER_REFLECT)
        frame5 = cv2.copyMakeBorder(frame5, int(padding_h/2), int(padding_h/2), int(padding_w/2), int(padding_w/2), cv2.BORDER_REFLECT)
        frame6 = cv2.copyMakeBorder(frame6, int(padding_h/2), int(padding_h/2), int(padding_w/2), int(padding_w/2), cv2.BORDER_REFLECT)

        frame4 = Image.fromarray(frame4)
        frame5 = Image.fromarray(frame5)
        frame6 = Image.fromarray(frame6)
        frame6c=frame6
        x1=(frame1,frame2,frame3,frame4,frame5)
        x2=(frame2,frame3,frame4,frame5,frame6)
        frame2 = transform(np.array(frame2,dtype="float32")/255)
        frame3 = transform(np.array(frame3,dtype="float32")/255)
        frame4 = transform(np.array(frame4,dtype="float32")/255)
        frame5 = transform(np.array(frame5,dtype="float32")/255)
        frame6 = transform(np.array(frame6,dtype="float32")/255)
        x1t=torch.stack((transform(frame1),frame2,frame3,frame4,frame5),dim=0)
        x2t=torch.stack((frame2,frame3,frame4,frame5,frame6),dim=0)
        x1t=kornia.color.bgr_to_rgb(x1t)
        x2t=kornia.color.bgr_to_rgb(x2t)
        if yuv:
            x1t=kornia.color.rgb_to_yuv(x1t)
            x2t=kornia.color.rgb_to_yuv(x2t)
        return x1t,x2t,frame6c,x1,x2,ret
    else:
        if ret==False:
            return None
        frame2 = cv2.copyMakeBorder(frame2, int(padding_h/2), int(padding_h/2), int(padding_w/2), int(padding_w/2), cv2.BORDER_REFLECT)
        frame3 = cv2.copyMakeBorder(frame3, int(padding_h/2), int(padding_h/2), int(padding_w/2), int(padding_w/2), cv2.BORDER_REFLECT)

        frame2 = Image.fromarray(frame2)
        frame3 = Image.fromarray(frame3)
        frame3c=frame3
        x1=(frame1,frame2)
        x2=(frame2,frame3)
        frame2 = transform(np.array(frame2,dtype="float32"))
        frame3 = transform(np.array(frame3,dtype="float32"))
        x1t=torch.stack((transform(frame1),frame2),dim=0)
        x2t=torch.stack((frame2,frame3),dim=0)
        x1t=kornia.color.bgr_to_rgb(x1t)
        x2t=kornia.color.bgr_to_rgb(x2t)
        if yuv:
            x1t=kornia.color.rgb_to_yuv(x1t)
            x2t=kornia.color.rgb_to_yuv(x2t)
        return x1t,x2t,frame3c,x1,x2,ret

@torch.inference_mode()
def interpolate(self,gpuid,fp16,model_name,FFmpegParams,yuv,videoinfo,path,OutputPath,progressBar,log):
    logs=""
    finishedframes=0
    first=True
    logs="[gui] Startrting interpolation\n"

    log.setText(logs)
    QApplication.processEvents()  


    try:
    
        width,height,fps,frames,padding_h,padding_w=videoinfo
        
    except:
        print("can't extract videoinfo")
        return None

    if int(width)==0:
        QMessageBox.critical(self, "critical", f"error:\nYour video is corupted or unsupported")
        return None

    padding=[padding_w,padding_h]
    logs=logs+f"[interpolation] padding {padding}\n"
    log.setText(logs)
    QApplication.processEvents()  
    if height<720:
        lowres=True
    command = [f"ffmpeg",
            '-y',
            '-f', 'rawvideo',
            '-vcodec','rawvideo',
            '-s', f"{int(width+padding_w)}x{int(height+padding_h)}",
            '-pix_fmt', 'bgr24',
            '-r', str(fps*2),
            '-i', '-']+FFmpegParams.split()+[f"{os.path.split(OutputPath)[0]}/temp-v.mkv"]
    print(command)
    proc = sp.Popen(command, stdin=sp.PIPE, bufsize=10**8)

    try:
        video = cv2.VideoCapture(path)
        ret,im1 = video.read()
        im1 = cv2.copyMakeBorder(im1, int(padding_h/2), int(padding_h/2), int(padding_w/2), int(padding_w/2), cv2.BORDER_REFLECT)

    except Exception as e:
        print("can't read video")
        QMessageBox.critical(self, "critical", f"error:\nCan't read video\n{e}")
        print(e)
        return None
    try:
        cain=torch.jit.load(model_name).cuda()
        print("loaded model")
        logs=logs+f"[cain] loaded model\n"
        log.setText(logs)
        QApplication.processEvents()  

    except Exception as e :
        QMessageBox.critical(self, "critical", f"error:\nCan't load model\n{e}")
        print(e)
        return None
    if fp16:
        cain.half()
        print("using half precision")
        logs=logs+f"[cain] half precision\n"
        log.setText(logs)
        QApplication.processEvents()  
    else:
        cain.float()
        print("using full precision")
    executor=concurrent.futures.ThreadPoolExecutor(max_workers=1)
    executor2=concurrent.futures.ThreadPoolExecutor(max_workers=1)
    logs=logs+f"[cain] Interpolating!\n"
    log.setText(logs)
    QApplication.processEvents()  
    with torch.no_grad():
        while ret==True:
                
                if first:
                    im1 = Image.fromarray(im1)
                    argsread=[video,im1,lowres,padding,yuv]
                    tread = executor.submit(read,argsread)
                    x1,x2,im1,x1n,x2n,ret=tread.result()
                    if ret==False:
                        return None


                if fp16:
                    try:
                        out=cain(x1.cuda().half(),x2.cuda().half())
                        del x1,x2
                        if yuv:
                            out = kornia.color.yuv_to_rgb(out)
                        out = kornia.color.rgb_to_bgr(out)
                    except Exception as e:
                        QMessageBox.critical(self, "critical", f"error:\n{e}")
                        print(e)
                        return None
                else:
                    try:
                        out=cain(x1.cuda(),x2.cuda())
                    except Exception as e:
                        QMessageBox.critical(self, "critical", f"error:\n{e}")
                        print(e)
                        return None
                argssave=[out.cpu(),proc,1,lowres,x1n,x2n,yuv]
                tsave = executor2.submit(save,argssave)
                argsread=[video,im1,lowres,padding,yuv]
                tread = executor.submit(read,argsread)
                try:
                    x1,x2,im1,x1n,x2n,ret=tread.result()
                except:
                    return None
                
                if lowres:
                    finishedframes+=5 
                else:
                    finishedframes+=2
                print(round(finishedframes/frames*100))
                progressBar.setValue(round(finishedframes/frames*100))
                QApplication.processEvents()  

                
                first=False
    return None
