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
#######################
bot = commands.Bot(command_prefix='!')
#def commands
os.system("nvidia-smi")
@bot.command()
async def gpu(ctx):
    await ctx.channel.send(content=f"bot run on {torch.cuda.get_device_name(0)}\nvram: {int(torch.cuda.get_device_properties('cuda').total_memory/1024/1024/1024)}GB")
@bot.command()
async def interpolate(ctx, arg1="--model",arg2="converted", arg3="--discord", arg4="x"):
    wrong=False
    ytdl=False
    gifuse=False
    ytdlurl="none"
    model_name="converted"
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
    filename=int(random()*100000000000000)
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


    ################ Using cv2 to get fps, width, height, frames number ################


    try:
        video = cv2.VideoCapture("1.mkv");
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
    
    os.system(f"ffmpeg -i 1.mkv -vf scale=640:360 -pix_fmt rgb24 -t 80 frames/%6d.png")
    os.system(f"ffmpeg -i 1.mkv -t 80 1.wav")
    if fps==0.0:
        fps=25
    await message.edit(content="finished frame extracting🎞️\n")


    ################ using interpolation ################


    await message.edit(content="interpolating✨\n")
    try:
      generate.interpolation(batch_size=1, img_fmt="png", torch_device="cuda", temp_img = f"frames", GPUid=0, GPUid2=False, fp16=True, modelp=f"{model_name}.pth", TensorRT=True)
    except Exception as e:
        await  ctx.channel.send(content=f"its oom? interpolation crashed❌\n{e}")
    await message.edit(content="finished interpolation✨\n")


    ################ Using ffmpeg to encode video ################
    if ossystem=='Linux':
        print("skip")
    else:
        input_and_output.listframe(dir="./frames", text_path="./")


    await message.edit(content=f"starting encoding🗄️➡️🎞️\n")


    ################ gif encoidng ################
    if ossystem=='Linux':
        if gifuse==True:
            os.system(f'ffmpeg -r {fps*2} -pattern_type glob -i "frames/*.png" -filter_complex "scale={int(width)}:{int(height)}:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -fs 7.95M "{filename}.gif"')
            filemp4=discord.File(f"{filename}.gif")
            await ctx.channel.send(file=filemp4, content="finished!✔️")
    else:
        if gifuse==True:
            os.system(f'ffmpeg -f concat -safe 0 -r {fps*2} -i "frame_list.txt"  -filter_complex "scale={int(width)}:{int(height)}:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"   -fs 7.95M "{filename}.gif"')
            filemp4=discord.File(f"{filename}.gif")
            await ctx.channel.send(file=filemp4, content="finished!✔️")    

    ################ mp4 encoidng ################-b:v {bitrate-69}k  -rc 1
    if width>1280:
        width=(width/height)*720
    if height>720:
        height=720
    if ossystem=='Linux':
        if os.path.isfile('1.wav'):
            os.system(f'ffmpeg -r {fps*2} -pattern_type glob -i "frames/*.png" -i 1.wav  -b:v {int((bitrate-69)*0.30)}k -preset 7 -pix_fmt yuv420p -c:v libsvt_vp9 -tune 0 -vf scale={int(width/8)*8}:{int(height/8)*8},hqdn3d  -b:v {bitrate-69}k  -rc 1 -b:a 69k -fs 7.40M  "SPOILER_{filename}.webm"')#-preset veryslow
            os.system(f'ffmpeg -r {fps*2} -pattern_type glob -i "frames/*.png" -i 1.wav  -b:v {int((bitrate-69))}k   -b:v {bitrate-69}k  -c:v h264_nvenc -b:a 69k -fs 7.90M  "{filename}.mp4"')
        else:
            os.system(f'ffmpeg -r {fps*2} -pattern_type glob -i "frames/*.png" -b:v {int((bitrate-69)*0.30)}k -preset 7  -pix_fmt yuv420p -c:v libsvt_vp9 -tune 0 -vf scale={int(width/8)*8}:{int(height/8)*8},hqdn3d  -b:v {bitrate-69}k  -rc 1  -b:a 69k -fs 7.40M "SPOILER_{filename}.webm"')#-vf scale={int((width/height)*320)/8*8}:320:flags=lanczos
            os.system(f'ffmpeg -r {fps*2} -pattern_type glob -i "frames/*.png"  -b:v {int((bitrate-69))}k  -pix_fmt yuv420p -b:v {bitrate-69}k  -c:v h264_nvenc -b:a 69k -fs 7.90M  "{filename}.mp4"')
        filemp4=discord.File(f"SPOILER_{filename}.webm")
        filemp41=discord.File(f"{filename}.mp4")
    else:  
        if os.path.isfile('1.wav'):
            os.system(f'ffmpeg -f concat -safe 0 -r {fps*2} -i "frame_list.txt" -i 1.wav  -b:v {bitrate-69}k -pix_fmt yuv420p -c:v h264_nvenc -preset hq -strict -2  -tune hq -vf scale={int(width/8)*8}:{int(height/8)*8},hqdn3d  -rc vbr -fs 7.95M  "{filename}.mp4"')
        else:
            os.system(f'ffmpeg -f concat -safe 0 -r {fps*2} -i "frame_list.txt"  -b:v {bitrate-69}k -pix_fmt yuv420p -c:v h264_nvenc -preset hq -strict -2 -vf scale={int(width/8)*8}:{int(height/8)*8},hqdn3d  -tune hq -vf  -rc vbr -fs 7.95M "{filename}.mp4"')
        
        filemp4=discord.File(f"{filename}.mp4")
    try:
        await ctx.channel.send(file=filemp41, content="mp4 look bad but not crash discord...✔️")
        await ctx.channel.send(file=filemp4, content="WEBM better but can crash discord✔️")
    except:
        await ctx.channel.send(file=filemp4, content="finished!✔️")
    
    os.remove(f"{filename}.mp4")
    os.remove(f"{filename}.gif")
    torch.cuda.empty_cache()

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {int(bot.latency*100)}ms')
#
@bot.command()
async def status(ctx):
    await ctx.send('bot work. now..')

#
@bot.command()
async def verssion(ctx):
    versfile = open("ver.txt", "r")
    curverssion=versfile.read()
    r = requests.get('https://raw.githubusercontent.com/Hubert482/cainapp/main/ver.txt')
    await ctx.send(f'this bot work on {curverssion}, latest verssion: {r.text}')

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
    await ctx.channel.send(content="The bot was created by Hubert Sontowski")
#
@bot.command()

async def models(ctx):
    '''Lists current models'''
    embed = discord.Embed(
        title="List of current models",
        color=0x4287f5,
        description=cleandoc("""
            stable_e3 - stable model trained on vimeo90k i think can be good for most things
            
            Need more models.  dm  if you have cain model hubert#0069 
        """)
    )
    await ctx.send(embed=embed)


tokenfile = open("token.txt", "r")
TOKEN=tokenfile.read()
bot.run(TOKEN)

