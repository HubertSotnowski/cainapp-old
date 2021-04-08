import torch
import numpy as np
import torchvision
from model.cain import CAIN
import time
fps=0
print("Building model: CAIN")
model = CAIN(depth=3)
from torch2trt import torch2trt
data = torch.randn((1, 3, 256, 256))
data1 = torch.randn((1, 3, 256, 256))
checkpoint = torch.load("temp_conv.pth")
model.load_state_dict(checkpoint)

model_trt = torch2trt(model.cuda().half(), [data.cuda().half(),data1.cuda().half()], fp16_mode=True)
startti=time.time()
model_trt.cuda()
torch.save(model_trt.state_dict(), 'converted.pth')
from torch2trt import TRTModule
del model_trt
model_trt = TRTModule()

model_trt.load_state_dict(torch.load('converted.pth'))
while fps<1000:
    x=model_trt(data.cuda(), data1.cuda())
    print(fps)
    fps+=1
endti=time.time()
print(endti-startti)
