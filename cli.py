import argparse


arg_lists = []
parser = argparse.ArgumentParser()

def add_argument_group(name):
    arg = parser.add_argument_group(name)
    arg_lists.append(arg)
    return arg


data_arg = add_argument_group('data')
data_arg.add_argument('--path', type=str, default='frames/')
data_arg.add_argument('--img_fmt', type=str, default='jpg')
data_arg.add_argument('--model', type=str, default='3d.pth')
data_arg.add_argument('--run', type=int, default= 2) # example 1=2x 2=4x 3=8x ...
startnum=0
args = parser.parse_args()
import generate
while args.run>startnum:
    generate.interpolation(batch_size=4, temp_img = args.path, fp16=True, modelp=args.model,img_fmt=args.img_fmt)
    startnum+=1
