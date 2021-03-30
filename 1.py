import discord
from discord.ext import commands
######################
from inspect import cleandoc
from typing import Union
import os
import requests
import cv2
import shutil
#######################
import torch
import generate
import input_and_output
#######################
from random import seed
from random import random
#######################
import platform
ossystem=platform.system()
print(ossystem)

usevp9 = open("output_type.txt", "r")

def delete():
    try:
        shutil.rmtree('frames/')
    except:
        print("bug")
    try:
        os.mkdir("frames")
    except:
        print("Frames Not Cleared")
    try:
        os.remove("1.mkv")
    except:
        print("1.mkv Undeleted")
    try:
        os.remove(f"{filename}.mp4")
    except:
        print("Filename.mp4 Undeleted")
    try:
        os.remove(f"{filename}.webm")
    except:
        print("Filename.webm Undeleted")
    try:
        os.remove(f"{filename}.gif")
    except:
        print("Filename.gif Undeleted")
    try:
        os.remove("1.wav")
    except:
        print("1.wav Undeleted")
    try:
        os.remove("3.mp4")
    except:
        print("3.mp4 Undeleted")
    try:
        os.remove("frame_list.txt")
    except:
        print("Frame List Undeleted")
#######################
bot = commands.Bot(command_prefix='!')
#def commands
os.system("nvidia-smi")
@bot.command()
async def gpu(ctx):
    await ctx.channel.send(content=f"bot run on {torch.cuda.get_device_name(0)}\nvram: {int(torch.cuda.get_device_properties('cuda').total_memory/1024/1024/1024)}GB")
@bot.command()
async def interpolate(ctx, arg1="--model",arg2="HubertV3", arg3="--discord", arg4="x"):
    wrong=False
    ytdl=False
    gifuse=False
    ytdlurl="none"
    model_name="HubertV3"
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

    embedVar = discord.Embed(title="Settings", description="", color=0x4287f5)
    embedVar.add_field(name="Model", value=model_name, inline=False)
    embedVar.add_field(name="youtube-dl", value=ytdl, inline=False)
    embedVar.add_field(name="youtube-dl url", value=ytdlurl, inline=False)
    for char in ytdlurl:
        print(char)
        if char==";":
            
            wrong=True
        else:
            print("good")
    if wrong==False:
        print("good")
    else:
        ytdlurl="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    await ctx.channel.send(embed=embedVar)
    filename=int(random()*1000000000)
    delete()

    ################ Downloading video ################


    message =  await ctx.send(content=f"Downloading video 📥\n")

    if ytdl==True:
        print("using youtube-dl")
        os.system(f"youtube-dl -o 1 --merge-output-format mkv {ytdlurl}")
    else:
        attachment = ctx.message.attachments[0] # gets first attachment that user
        os.system(f"wget --output-document=1.mkv {attachment.url}")
        length = len(attachment.url)
        if attachment.url[length -1]=="f":
            gifuse=True
        else:
            gifuse=False
    #

    ################ Using cv2 to get fps, width, height, frames number ################


    try:
        video = cv2.VideoCapture("1.mkv");
        fps = video.get(cv2.CAP_PROP_FPS)
        width  = video.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
        height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height` round(width)
        frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        length = int(frames/fps)+2
        if length>75:
            length=75+7
        bitrate = int(63200/length)
        await message.edit(content=f"bitrate {bitrate}K/s, fps: {fps*2}, frames: {frames}\n")
    except Exception as e:
        await  ctx.channel.send(content=f"Error getting video info. :x:\n\n{e}")


    ################ Using ffmpeg to extract frames and audio ################

    await message.edit(content=f"Extracting Frames🎞️\n")
    if width<height:
        os.system(f"ffmpeg -i 1.mkv -vf scale=256:{int(((height/width)*256)/8)*8} -pix_fmt rgb24 frames/%6d.png")
    else:
        os.system(f"ffmpeg -i 1.mkv -vf scale={int(((width/height)*256)/8)*8}:256 -pix_fmt rgb24 frames/%6d.png")
    os.system("ffmpeg -i 1.mkv -pix_fmt rgb24 1.wav")
    await message.edit(content="Frames Extracted🎞️\n")
    if fps==0.0:
        fps=25


    ################ Interpolating ################


    await message.edit(content="Interpolating :flushed:\n")
    try:
      generate.interpolation(batch_size=10, img_fmt="png", torch_device="cuda", temp_img = f"frames", GPUid=1, GPUid2=False, fp16=False, modelp=f"models/{model_name}.pth")
    except Exception as e:
        await  ctx.channel.send(content=f"Out of GPU memory, Interpolation crashed ❌\n{e}")
    await message.edit(content="Finished interpolation :thumbsup:\n")


    ################ Using ffmpeg to encode video ################
    if ossystem=='Linux':
        print("skip")
    else:
        input_and_output.list_frame(dir="./frames", text_path="./")


    await message.edit(content=f"Encoding🗄️➡️🎞️\n")


    ################ gif encoding ################
    if ossystem=='Linux':
        if gifuse==True:
            os.system(f'ffmpeg -r {fps*2} -pattern_type glob -i "frames/*.png" -b:v {bitrate-69}k -filter_complex "scale={int(width)}:{int(height)}:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -fs 7.95M "{filename}.mp4"')
            filemp4=discord.File(f"{filename}.gif")
            await ctx.channel.send(file=filemp4, content="Finished!✔️\n Output:")
    else:
        if gifuse==True:
            os.system(f'ffmpeg -f concat -safe 0 -r {fps*2} -i "frame_list.txt"  -filter_complex "scale={int(width)}:{int(height)}:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"   -fs 7.95M "{filename}.gif"')
            filemp4=discord.File(f"{filename}.gif")
            await ctx.channel.send(file=filemp4, content="Finished!✔️\n Output:")    

            
        


    ################ mp4 encoidng ################
    if ossystem=='Linux':
        try:
            os.system(f'ffmpeg -r {fps*2} -pattern_type glob -i "frames/*.png" -i 1.wav  -b:v {bitrate-69}k -pix_fmt yuv420p -c:v libx264 -preset veryslow -strict -2 -vf hqdn3d -fs 7.95M  "{filename}.mp4"')#-preset veryslow
            filemp4=discord.File(f"{filename}.mp4")
            await ctx.channel.send(file=filemp4, content="Finished!✔️\n Output:")
        except:
            os.system(f'ffmpeg -r {fps*2} -pattern_type glob -i "frames/*.png" -b:v {bitrate-69}k -pix_fmt yuv420p -c:v libx264 -preset veryslow -strict -2 -vf hqdn3d -fs 7.95M "{filename}.mp4"')#-vf scale={int((width/height)*320)/8*8}:320:flags=lanczos
            filemp4=discord.File(f"{filename}.mp4")
            await ctx.channel.send(file=filemp4, content="Finished!✔️\n Output:")
        torch.cuda.empty_cache()
        os.remove(f"{filename}.mp4")
        os.remove(f"{filename}.gif")
        os.remove(f"{filename}.webm")
    else:  
        try:
            os.system(f'ffmpeg -f concat -safe 0 -r {fps*2} -i "frame_list.txt" -i 1.wav  -b:v {bitrate-69}k -pix_fmt yuv420p -c:v h264 -preset hq -strict -2 -tune hq -vf hqdn3d -rc vbr -fs 7.95M  "{filename}.mp4"')#-preset veryslow
            filemp4=discord.File(f"{filename}.mp4")
            await ctx.channel.send(file=filemp4, content="Finished!✔️\n Output:")
        except:
            os.system(f'ffmpeg -f concat -safe 0 -r {fps*2} -i "frame_list.txt" -b:v {bitrate-69}k -pix_fmt yuv420p -c:v h264 -preset hq -strict -2 -tune hq -vf hqdn3d -rc vbr -fs 7.95M "{filename}.mp4"')#-vf scale={int((width/height)*320)/8*8}:320:flags=lanczos
            filemp4=discord.File(f"{filename}.mp4")
            await ctx.channel.send(file=filemp4, content="Finished!✔️\n Output:")
        torch.cuda.empty_cache()
        os.remove(f"{filename}.mp4")
        os.remove(f"{filename}.gif")
        os.remove(f"{filename}.webm")

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {int(bot.latency*100)}ms')
#
@bot.command()
async def status(ctx):
    await ctx.send('Bot is currently working..')

#
@bot.command()
async def version(ctx):
    versfile = open("ver.txt", "r")
    curverssion=versfile.read()
    r = requests.get('https://raw.githubusercontent.com/Hubert482/cainapp/main/ver.txt')
    await ctx.send(f'This bot is using {curverssion}, Latest Version: {r.text}')

#+
@bot.command()

async def dgb(ctx):
    await ctx.channel.send(content="My dgb wallet :') D9PsnVGnmVr6jkJkDMdmhkueUh6h4xvuYB ")
#
@bot.command()

async def doge(ctx):
    await ctx.channel.send(content="My doge wallet :') DCSFWg8Djhk1UX3BZXHJe7zkaUurRn5ppn ")

    #
#
@bot.command()
async def credits(ctx):
    await ctx.channel.send(content="This bot was created by Hubert Sontowski with the help of Dire Meganium97, Tika Takumika, and Anon Shiwo.")
#
@bot.command()

async def models(ctx):
    '''Lists current models'''
    embed = discord.Embed(
        title="List of current models",
        color=0x4287f5,
        description=cleandoc("""
            HubertV3 - stable model trained on vimeo90k i think can be good for most things
            
            We need more models! DM if you have CAIN model that can be added (hubert#0069) 
        """)
    )
    await ctx.send(embed=embed)

usevp9 = open("output_type.txt", "r")
tokenfile = open("token.txt", "r")
TOKEN=tokenfile.read()
bot.run(TOKEN)

