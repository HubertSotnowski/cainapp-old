from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog
from PyQt5 import uic
import os
import shutil
import os.path
import cv2
import torch
import platform
ossystem=platform.system()
print(ossystem)

filename="test.mp4"
def SelectInput():
    global filename
    global fps
    filename = QFileDialog.getOpenFileName()
    video = cv2.VideoCapture(filename[0]);
    fps = video.get(cv2.CAP_PROP_FPS)
    frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    width  = video.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height` round(width)
    if round(height)==round(round(round(height)/8)*8):
        scale1=False
    else:
        scale1=True

    if round(width)==round(round(round(width)/8)*8):
        scale=False
    else:
        scale=True
    if scale1==True:
        scale=True

    return fps, frames, filename[0], round(height), round(width), scale

def select_path():
    global dir_path
    dir_path = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
    return dir_path


def  ExtractFramesOrSplit(Type="jpg", chunksize="00:01:00", dir_path="./",Line=" ", input="./"):

    print(f"{Type} {chunksize} {dir_path}/{input}")
    if os.path.isdir(f'{dir_path}/cain/'):
        try:
            shutil.rmtree(f'{dir_path}/cain')
            os.mkdir(f'{dir_path}/cain/')
            os.mkdir(f'{dir_path}/cain/frames')
        except:
            print("wtf")
    else:
        os.mkdir(f'{dir_path}/cain')
        os.mkdir(f'{dir_path}/cain/frames')

    os.system(f'ffmpeg -i "{input}" -hide_banner {Line} -q 2 -pix_fmt rgb24 "{dir_path}/cain/frames/%6d.{Type}"')
    os.system(f'ffmpeg -i "{input}" -hide_banner "{dir_path}/cain/1.wav"')



def list_frame(dir="./frames", text_path="./frames"):
    try:
        os.remove(f'{text_path}/frame_list.txt')
    except:
        print("file exist")
    txt = open(f'{text_path}/frame_list.txt', 'a')
    for file in os.listdir(dir):
        print(os.path.join(dir, file))
        string = (f"file 'frames/{os.path.join(file)}'\n")
        txt.write(string)


def ExportVideo(dir_path, proresmode, imtype, fps, factor, filetype, useprores, line):
    if factor=="2x":
        fpss=2*float(fps)
        print(fpss)
        print(fps)
    else:
        fpss=4*float(fps)
        print(fpss)
        print(fps)
    #list_frame(dir=f"frames")
    if ossystem=='Linux':
        if useprores==True:

            os.system(f'ffmpeg -r {float(fpss)}  -pattern_type glob -i "{dir_path}frames/*.{imtype}"  -c:v prores_ks {line} -profile:v {proresmode} "{dir_path}/video.{filetype}"')
            torch.cuda.empty_cache()
        else:
            os.system(f'ffmpeg -r {float(fpss)}  -pattern_type glob -i "{dir_path}frames/*.{imtype}" {line} "{dir_path}/video.{filetype}"')
            torch.cuda.empty_cache()
        if os.path.isfile(f"{dir_path}/1.wav"):
            os.system(f'ffmpeg -i "{dir_path}/video.{filetype}"  -i "{dir_path}/1.wav" -c:v copy "{dir_path}/video_audio.mp4"')
            torch.cuda.empty_cache()
    else:

        if useprores==True:
            os.system(f'ffmpeg -f concat -safe 0 -r {float(fpss)} -i "{dir_path}/frame_list.txt" -c:v prores_ks {line} -profile:v {proresmode} "{dir_path}/video.{filetype}"')
            torch.cuda.empty_cache()
        else:
            os.system(f'ffmpeg -f concat -safe 0 -r {float(fpss)} -i "{dir_path}/frame_list.txt" {line} "{dir_path}/video.{filetype}"')
            torch.cuda.empty_cache()
        if os.path.isfile(f"{dir_path}/1.wav"):
            os.system(f'ffmpeg -i "{dir_path}/video.{filetype}" -i "{dir_path}/1.wav" -c:v copy "{dir_path}/video_audio.mp4"')
            torch.cuda.empty_cache()




