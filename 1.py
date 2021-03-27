import discord
from discord.ext import commands
######################
from inspect import cleandoc
from typing import Union
import os
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
async def interpolate(ctx, arg1="--model",arg2="TVP_Cain_abriged", arg3="--discord", arg4="x"):
    ytdl=False
    gifuse=False
    ytdlurl="none"
    model_name="hubert_v0.1"
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
    #
    embedVar = discord.Embed(title="Settings", description="", color=0x00ff00)
    embedVar.add_field(name="Model", value=model_name, inline=False)
    embedVar.add_field(name="youtube-dl", value=ytdl, inline=False)
    embedVar.add_field(name="youtube-dl url", value=ytdlurl, inline=False)
    await ctx.channel.send(embed=embedVar)
    filename=int(random()*1000000000)
    delete()

    ################ Downloading video ################


    message =  await ctx.send(content=f"Downloading video\n")

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
            length=75
        bitrate = int(63200/length)
        message.edit(content=f"bitrate {bitrate}K/s, fps: {fps*2}, frames: {frames}\n")
    except Exception as e:
        await  ctx.channel.send(content=f"error while getting data and calculating bitrate\n\n {e}")


    ################ Using ffmpeg to extract frames and audio ################

    await message.edit(content=f"starting frame extraction \n")
    if width<height:
        os.system(f"ffmpeg -i 1.mkv -vf scale=256:{int(((height/width)*256)/8)*8} -pix_fmt rgb24 -t 75 frames/%6d.png")
    else:
        os.system(f"ffmpeg -i 1.mkv -vf scale={int(((width/height)*256)/8)*8}:256 -pix_fmt rgb24 -t 165 frames/%6d.png")
    os.system("ffmpeg -i 1.mkv  -pix_fmt rgb24 -t 75 1.wav")
    await message.edit(content="finished frame extracting\n")
    if fps==0.0:
        fps=25


    ################ using interpolation ################


    await message.edit(content="interpolating\n")
    try:
      generate.interpolation(batch_size=10, img_fmt="png", torch_device="cuda", temp_img = f"frames/", GPUid=1, GPUid2=False, fp16=False, modelp=f"models/{model_name}.pth")
    except Exception as e:
        await  ctx.channel.send(content=f"its oom? \n{e}")
    input_and_output.list_frame(dir="./frames", text_path="./")
    await message.edit(content="finished interpolation\n")


    ################ Using ffmpeg to encode video ################


    await message.edit(content=f"starting encoding\n")


    ################ gif encoidng ################


    if gifuse==True:
        os.system(f'ffmpeg -f concat -safe 0 -r {fps*2} -i "frame_list.txt"  -filter_complex "scale={int(width)}:{int(height)}:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"   -fs 7.95M "{filename}.gif"')#-preset veryslow
        filemp4=discord.File(f"{filename}.gif")
        await ctx.channel.send(file=filemp4, content="gif")


    ################ mp4 encoidng ################
    try:
        os.system(f'ffmpeg -f concat -safe 0 -r {fps*2} -i "frame_list.txt" -i 1.wav  -b:v {bitrate-69}k -pix_fmt yuv420p -c:v h264_nvenc -vf hqdn3d  -tune hq -rc vbr -preset p7 -c:a libopus  -b:a 69k -fs 7.95M "{filename}.mp4"')#-preset veryslow
        filemp4=discord.File(f"{filename}.mp4")

        await ctx.channel.send(file=filemp4, content="cain")

    except:
        os.system(f'ffmpeg -f concat -safe 0 -r {fps*2} -i "frame_list.txt"  -b:v {bitrate-69}k -pix_fmt yuv420p -c:v h264_nvenc -preset p7   -tune hq -vf hqdn3d -rc vbr -fs 7.95M "{filename}.mp4"')#-vf scale={int((width/height)*320)/8*8}:320:flags=lanczos
        filemp4=discord.File(f"{filename}.mp4")
        await ctx.channel.send(file=filemp4, content="mp4")
        pass
    await ctx.channel.send(content="finished!")
    torch.cuda.empty_cache()

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
        description=cleandoc("""
            broken - hubert says its "very epileptic" and to "try it"
            stbale - stable model trained on vimeo90k i think can be good for most things
            TVP_WIP-8E - problems with green not tested
        """)
    )
    
    await ctx.send(embed=embed)



TOKEN='token here'
bot.run(TOKEN)

