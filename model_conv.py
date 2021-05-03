import torch
from model.cain import CAIN
def convert(Input="input.pth",output="1.pth",tensort=False, height=256, width=256):
    model = CAIN(depth=3)
    model = torch.nn.DataParallel(model).to("cuda")
    print(Input)
    checkpoint = torch.load(Input)
    model.load_state_dict(checkpoint['state_dict'])
    model.cuda()
    model.eval()
    try:
        state_dict = model.module.state_dict()
    except AttributeError:
        state_dict = model.state_dict()
    if tensort==False:
        torch.save(state_dict, output)
    else:
        from torch2trt import torch2trt
        data = torch.randn(1, 3,  int(height), int(width)).cuda().half()
        data1 = torch.randn(1, 3,  int(height), int(width)).cuda().half()
        print("Building model: CAIN TENOSR RT")
        model = CAIN(depth=3)
        model.load_state_dict(state_dict)
        model.cuda().half()
        input_names = ["input_1", "input_2"]
        output_names = ["output_frame", "output_features"]
        model_trt = torch2trt(model, (data,data1), input_names=input_names, output_names=output_names, fp16_mode=True, max_batch_size=10)
        model_trt.half()
        torch.save(model_trt.state_dict(), output)
