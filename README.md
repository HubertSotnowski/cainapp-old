# CAINAPP 2 BETA🚧

Welcome to CAINAPP 2.0!

### What is CAIN?

##### CAIN - Channel Attention Is All You Need for Video Frame Interpolation

CAIN is a very fast interpolation network that doesn't use much vram (Ex: 5GB with fp16 for 8k)! 



### What is cainapp?

##### 

Cainapp is a gui for cain with some new things like fp16, saving frames on other threads and more! Look at the code!



## How to install 💾

1. download python 3.8 📥 (https://www.python.org/ftp/python/3.8.7/python-3.8.7-amd64.exe)

2. install python 3.8 remember to select add to path

3. in cmd run 

   `pip install pyqt5`

   `pip install qdarkstyle`

   `pip install pip install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html` this can need much time ⌚

   `pip install tqdm`

   `pip install opencv-python`

   

   

4. Download ffmpeg 📥 (https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z) 

5. Extract 📦 ffmpeg.exe in cainapp folder📁

6. Download models and put them into the cain folder📁

7. In cmd, run ` cd path/to/cainapp/ ` then ```python main.py```

## How to run the discord bot🤖

Basically the same as in How to install but you need to install 2 more things

`pip install discord.py` 

`pip install requests`

And put your token to token.txt 

And run ```python3 1.py```

Sadly, Discord limits the file size to 8MB, so bitrate isn't high and video length is limited. Audio is also only 69kbps

## How to train 🚆

[![Open In Colab](https://camo.githubusercontent.com/84f0493939e0c4de4e6dbe113251b4bfb5353e57134ffd9fcab6b8714514d4d1/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/github/Hubert482/CAIN/blob/master/Training.ipynb) Simple train colab try it! Its simple! 



## Donate💰

If you wish to support the project, you can donate to Hubert's patreon [here](https://www.patreon.com/hubert_)!
Hubert's dogecoin and dgb wallets are also listed in the code.



## CAIN Citation

```
@inproceedings{choi2020cain,
    author = {Choi, Myungsub and Kim, Heewon and Han, Bohyung and Xu, Ning and Lee, Kyoung Mu},
    title = {Channel Attention Is All You Need for Video Frame Interpolation},
    booktitle = {AAAI},
    year = {2020}
}
```
