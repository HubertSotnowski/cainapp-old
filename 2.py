import discord
from discord.ext import commands


import generate
import os
import cv2
import shutil
import input_and_output
from random import seed
from random import random
#set prefix





def delete():
    try:
        shutil.rmtree('frames/')
    except:
        print("bug")
    try:
        os.mkdir("frames")
    except:
        print("bug")
    try:
        os.remove("1.mkv")
    except:
        print("bug")
    try:
        os.remove(f"{filename}.mp4")
    except:
        print("bug")
    try:
        os.remove("1.wav")
    except:
        print("bug")
    try:
        os.remove("3.mp4")
    except:
        print("bug")
    try:
        os.remove("frame_list.txt")
    except:
        print("bug")















bot = commands.Bot(command_prefix='!')
#def commands
@bot.command()
async def interpolate(ctx, arg1="3",arg2="discord", arg3="x"):
    filename=int(random()*1000000000)
    delete()

    ################ Downloading video ################
    await ctx.channel.send(content=f"Downloading video")

    if arg2=="ytdl":
        print("using youtube-dl")
    else:
        attachment = ctx.message.attachments[0] # gets first attachment that user
    if arg2=="ytdl":
        os.system(f"youtube-dl -o 1 --merge-output-format mkv {arg3}")
    else:
        os.system(f"wget --output-document=1.mkv {attachment.url}")


    ################ Using cv2 to get fps, width, height, frames number ################


    try:
        video = cv2.VideoCapture("1.mkv");
        fps = video.get(cv2.CAP_PROP_FPS)
        width  = video.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
        height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height` round(width)
        frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        length = int(frames/fps)+2
        if length>75:
            length=77
        bitrate = int(63200/length)
        ctx.channel.send(content=f"bitrate {bitrate}K/s, fps: {fps*2}, frames: {frames}")
    except Exception as e:
        await ctx.channel.send(content=f"error while getting data and calculating bitrate\n\n {e}")


    ################ Using ffmpeg to extract frames and audio ################

    await ctx.channel.send(content=f"starting frame extraction ")
    if width<height:
        os.system(f"ffmpeg -i 1.mkv -vf scale=256:{int(((height/width)*256)/8)*8} -pix_fmt rgb24 -t 75 frames/%6d.png")
    else:
        os.system(f"ffmpeg -i 1.mkv -vf scale={int(((width/height)*256)/8)*8}:256 -pix_fmt rgb24 -t 75 frames/%6d.png")
    os.system("ffmpeg -i 1.mkv  -pix_fmt rgb24 -t 75 1.wav")
    await ctx.channel.send(content="finished frame extracting")
    if fps==0.0:
        fps=25


    ################ using interpolation ################

    await ctx.channel.send(content="interpolating...")
    generate.interpolation(batch_size=6, img_fmt="png", torch_device="cuda", temp_img = f"frames/", GPUid=1, GPUid2=False, fp16=True, modelp=f"{arg1}.pth")
    input_and_output.list_frame()
    await ctx.channel.send(content="finished interpolation")

    ################ Using ffmpeg to encode video ################


    try:
        await ctx.channel.send(content=f"starting encoding")
        os.system(f'ffmpeg -f concat -safe 0 -r {fps*2} -i "frame_list.txt" -i 1.wav  -b:v {bitrate-69}k -pix_fmt yuv420p -c:v h264_nvenc -vf hqdn3d  -tune hq -rc vbr -preset p7 -c:a libopus  -b:a 69k -fs 7.95M "{filename}.mp4"')#-preset veryslow
        filemp4=discord.File(f"{filename}.mp4")
        await ctx.channel.send(content="finished encoding sending...")
        await ctx.channel.send(file=filemp4, content="cain")

    except:
        os.system(f'ffmpeg -f concat -safe 0 -r {fps*2} -i "frame_list.txt"  -b:v {bitrate-69}k -pix_fmt yuv420p -c:v h264_nvenc -preset p7   -tune hq -vf hqdn3d -rc vbr -fs 7.95M "{filename}.mp4"')#-vf scale={int((width/height)*320)/8*8}:320:flags=lanczos
        filemp4=discord.File(f"{filename}.mp4")
        await ctx.channel.send(content="finished encoding sending...")
        await ctx.channel.send(file=filemp4, content="cain")
        pass
    await ctx.channel.send(content="finished!")
@bot.command()

async def dgb(ctx):
    await ctx.channel.send(content="My dgb wallet :') D9PsnVGnmVr6jkJkDMdmhkueUh6h4xvuYB ")
#

TOKEN=TOKEN HERE!
bot.run(TOKEN)

