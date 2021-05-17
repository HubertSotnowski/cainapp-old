import os

import glob
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image

global img1
global img2
img2="nothing"
img1="nothing"
framenum=0

def clean():
    global img1
    global img2
    print(img1)
    print(img2)
    img1="nothing"
    img2="nothing"
class Video(Dataset):
    def __init__(self, data_root, fmt='png'):
        images = sorted(glob.glob(os.path.join(data_root, '*.%s' % fmt)))
        for im in images:
            try:
                float_ind = float(im.split('_')[-1][:-4])
            except ValueError:
                os.rename(im, '%s_%.06f.%s' % (im[:-4], 0.0, fmt))
        # re
        images = sorted(glob.glob(os.path.join(data_root, '*.%s' % fmt)))
        self.imglist = [[images[i], images[i+1], images[i+2]] for i in range(len(images)-2)]
        img2="nothing"
        img1="nothing"
        print('[%d] images ready to be loaded' % len(self.imglist))



    def __getitem__(self, index):
        T = transforms.ToTensor()
        global img1
        global img2
        imgpaths = self.imglist[index]
        img1 = Image.open(imgpaths[0])
        img2 = Image.open(imgpaths[1])
        img3 = Image.open(imgpaths[2])
        img1 = T(img1)        
        img2 = T(img2)  
        img3 = T(img3)  
        imgs = [img1, img2,img3] 
        meta = {'imgpath': imgpaths}
        return imgs, meta

    def __len__(self):
        return len(self.imglist)


def get_loader(mode, data_root, batch_size, img_fmt='png', shuffle=False, num_workers=0, n_frames=1):
    if mode == 'train':
        is_training = True
    else:
        is_training = False
    dataset = Video(data_root, fmt=img_fmt)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers, pin_memory=True)
