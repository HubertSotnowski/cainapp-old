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
ossystem=platform.system()
print(ossystem)
from botmodule import *
import threading
import asyncio
#######################
bot = commands.Bot(command_prefix='!')
#def commands
os.system("nvidia-smi")
@bot.command()
async def gpu(ctx):
    await ctx.channel.send(content=f"bot run on {torch.cuda.get_device_name(0)}\nvram: {int(torch.cuda.get_device_properties('cuda').total_memory/1024/1024/1024)}GB")
    


@bot.command()
async def interpolate(ctx, arg1="--model",arg2="converted", arg3="--discord", arg4="x"):
    asyncio.gather(interpolatevideo(ctx, arg1=arg1,arg2=arg2, arg3=arg3, arg4=arg4))

    
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
    r = requests.get('https://gitlab.com/hubert.sontowski2007/cainapp/-/raw/main/ver.txt')
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
        description=cleandoc("yyy just use default is best for now")
    )
    await ctx.send(embed=embed)
                           

tokenfile = open("token.txt", "r")
TOKEN=tokenfile.read()
bot.run(TOKEN)

