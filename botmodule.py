import discord
from discord.ext import commands
######################
from inspect import cleandoc
from typing import Union
import os
import requests
import cv2
import shutil
import subprocess
#######################
import torch
import modules.generate as generate
import modules.input_and_output as input_and_output
#######################
from random import seed
from random import random
#######################
import platform
from typing import Awaitable

async def interpolatevideo(ctx, arg1="--model",arg2="converted", arg3="--discord", arg4="x"):
    wrong=False
    ytdl=False
    gifuse=False
    wgeturl="fdf"
    ytdlurl="none"
    model_name="converted"
    wget=False
    ################  ################

    if arg1=="--model":
        model_name=arg2
    if arg3=="--model":
        model_name=arg4
    ################
    if arg1=="--ytdl":
        ytdlurl=arg2
        ytdl=True
    if arg3=="--ytdl":
        ytdlurl=arg4
        ytdl=True
    ##############
    if arg1=="--wget":
        wgeturl=arg2
        wget=True
    if arg3=="--wget":
        wgeturl=arg4
        wget=True

    embedVar = discord.Embed(title="Settings", description="", color=0x4287f5)
    embedVar.add_field(name="Model", value=model_name, inline=False)
    embedVar.add_field(name="youtube-dl", value=ytdl, inline=False)
    embedVar.add_field(name="youtube-dl url", value=ytdlurl, inline=False)
    for char in ytdlurl:
        if char==";":
            
            wrong=True
    if wrong==True:
        ytdlurl="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    for char in wgeturl:
        if char==";":
            
            wrong=True
    if wrong==True:
        wgeturl="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    await ctx.channel.send(embed=embedVar)
    filename=int(random()*100000000000000)
    try:
        os.mkdir(f"{filename}")
    except:
        _="c"
    ################ Downloading video ################



    message =  await ctx.send(content=f"Downloading video 📥\n")

    if ytdl==True:
        print("using youtube-dl")
        os.system(f"youtube-dl -o {filename} --merge-output-format mkv {ytdlurl}")
    elif wget==True:
        print("using wget")
        os.system(f"wget --output-document={filename}.mkv {wgeturl}")
    else:
        attachment = ctx.message.attachments[0] # gets first attachment that user
        os.system(f"wget --output-document={filename}.mkv {attachment.url}")
        length = len(attachment.url)
        if attachment.url[length -1]=="f":
            gifuse=True
        else:
            gifuse=False


    ################ Using cv2 to get fps, width, height, frames number ################


    try:
        video = cv2.VideoCapture(f"{filename}.mkv");
        fps = video.get(cv2.CAP_PROP_FPS)
        width  = video.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
        height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height` round(width)
        frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        length = int(frames/fps)+2
        if length>70:
            length=80
        bitrate = int(63200/length)
        await message.edit(content=f"bitrate {bitrate}K/s, fps: {fps*2}, frames: {frames}\n")
    except Exception as e:
        await  ctx.channel.send(content=f"error❌\n\n{e}")


    ################ Using ffmpeg to extract frames and audio ################
    
    os.system(f"ffmpeg -i {filename}.mkv -hide_banner -loglevel error -vf scale=640:360 -pix_fmt rgb24 -t 80 {filename}/%6d.png")
    os.system(f"ffmpeg -i {filename}.mkv  -hide_banner -loglevel error -t 80 {filename}.wav")
    if fps==0.0:
        fps=25
    await message.edit(content="finished frame extracting🎞️\n")


    ################ using interpolation ################


    await message.edit(content="interpolating✨\n")
    try:
        generate.interpolation(batch_size=5, img_fmt="png", torch_device="cuda", temp_img = f"{filename}", GPUid=0, GPUid2=False, fp16=True, modelp=f"{model_name}.pth", TensorRT=False)
    except Exception as e:
        await  ctx.channel.send(content=f"interpolation crashed❌\n{e}")
    await message.edit(content="finished interpolation✨\n")


    ################ Using ffmpeg to encode video ################

    input_and_output.rename(f"./{filename}")


    await message.edit(content=f"starting encoding🗄️➡️🎞️\n")


    ################ gif encoidng ################

    if gifuse==True:
        os.system(f'ffmpeg -r {fps*2} -i "{filename}/%6d.png" -filter_complex "scale={int(width)}:{int(height)}:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -hide_banner -loglevel error -fs 7.95M "{filename}.gif"')
        filegif=discord.File(f"{filename}.gif")

    ################ mp4 encoidng ################-b:v {bitrate-69}k  -rc 1

    if os.path.isfile(f'{filename}.wav'):
        os.system(f'ffmpeg -r {fps*2} -i "{filename}/%6d.png" -i {filename}.wav  -b:v {int((bitrate-69))}k  -c:a libopus -b:v {bitrate-69}k  -c:v libx264 -pix_fmt yuv420p -b:a 69k -fs 7.90M  "{filename}.mp4"')
    else:
        os.system(f'ffmpeg -r {fps*2} -i "{filename}/%6d.png"   -b:v {int((bitrate-69))}k  -pix_fmt yuv420p -b:v {bitrate-69}k  -c:v libx264 -pix_fmt yuv420p -b:a 69k -fs 7.90M  "{filename}.mp4"')

    #send video
    filemp4=discord.File(f"{filename}.mp4")
    await ctx.channel.send(file=filemp4, content="finished mp4 encoding\n")
    if gifuse==True:
        await ctx.channel.send(file=filegif,content=f"finished gif encoding\n")

    #delete video
    try:
        os.remove(f"{filename}.mp4")
    except:
        _="c"
    try:
        os.remove(f"{filename}.webm")
    except:
        _="c"
    try:
        os.remove(f"{filename}.gif")
    except:
        _="c"
    try:
        os.remove(f"{filename}.mkv")
    except:
        _="c"
    try:
        os.remove(f"{filename}.wav")
    except:
        _="c"
    shutil.rmtree(f"{filename}/")
    torch.cuda.empty_cache()