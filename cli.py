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
data_arg.add_argument('--model', type=str, default='output.pth')
data_arg.add_argument('--runtimes', type=int, default= 2)
startnum=0
args = parser.parse_args()
import generate
while args.runtimes>startnum:
    generate.interpolation(batch_size=4, temp_img = args.path, fp16=True, modelp=args.model,img_fmt=args.img_fmt)
    startnum+=1