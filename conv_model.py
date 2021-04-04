import torch
import numpy as np
import torchvision
import os
from model.cain import CAIN
os.system("export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64")
print("Building model: CAIN")
model = CAIN(depth=3)
model = torch.nn.DataParallel(model).to("cuda")
checkpoint = torch.load("1.pth")
model.load_state_dict(checkpoint['state_dict'])
model.cuda().cpu()
model.eval()
try:
    state_dict = model.module.state_dict()
except AttributeError:
    state_dict = model.state_dict()

torch.save(state_dict, 'temp_conv.pth')
os.system("python3 trt.py")