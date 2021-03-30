# CAINAPP 2 BETA🚧

Welcome to CAINAPP 2.0!

### What is CAIN?

##### CAIN - Channel Attention Is All You Need for Video Frame Interpolation

CAIN is a very fast interpolation network that doesn't use much vram (Ex: 5GB with fp16 for 8k)! 



### What is cainapp?



Cainapp is a gui for cain with some new things like fp16, saving frames on other threads and more! Look at the code!



## What are the requirements?

Unlike previously, Cainapp now runs on CUDA. Fortunately, it runs on the driver-based version, so the only requirements are

1. A nvidia GPU
2. Driver version >396.26

So in theory, it could even run on a GTX 650



## How to install on windows💾


1. Download python 3.9 📥 (https://www.python.org/ftp/python/3.9.2/python-3.9.2-amd64.exe)

   python 3.9 only supports Windows 8+, if you want run cain app on windows 7 use python 3.8

   

2. Install python 3.9, and remember to select "Add to PATH"

3. In cmd run 

   `pip3 install pyqt5`

   `pip3 install qdarkstyle`

   `pip3 install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html` this can need much time ⌚

   `pip3 install tqdm`

   `pip3 install opencv-python`

   

4. Download ffmpeg 📥 (https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z) 

   Extract 📦 ffmpeg.exe in cainapp folder📁

5. Download the model and put it into the cain folder📁d

6. In cmd, run ` cd path/to/cainapp/ ` then ```python3 main.py```

   

## How to install on ubuntu💾


1. install git ```sudo apt install git```

2. clone cainapp ```git clone https://github.com/Hubert482/cainapp.git```

3. install python 3 pip ```sudo apt install python3-pip```

4. In terminal run 

   `pip3 install pyqt5`

   `pip3 install qdarkstyle`

   `pip3 install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html` this can need much time ⌚

   `pip3 install tqdm`

   `pip3 install opencv-python-headless`

   `sudo apt install ffmpeg`

5. Download the model and put it into the cain folder📁

6. In terminal, run ` cd cainapp/ ` then ```python3 main.py```

   

## How to run the discord bot🤖

Basically the same as in How to install but you need to install 2 more things and do some arranging

`pip3 install discord.py` 

`pip3 install requests`

Put your token in a file called `token.txt` in the main cain directory

Take your model file from before, copy it to a folder named `models`, and rename it to stable.pth.

And run ```python3 1.py```

Sadly, Discord limits the file size to 8MB, so bitrate isn't high and video length is limited. Audio bitrate is also only 69kbps

## How to train 🚆

[![Open In Colab](https://camo.githubusercontent.com/84f0493939e0c4de4e6dbe113251b4bfb5353e57134ffd9fcab6b8714514d4d1/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/github/Hubert482/CAIN/blob/master/Training.ipynb) Simple train colab try it! Its simple! 

## Models

https://drive.google.com/drive/folders/1Pljrfv9xjXPU2fiwvSx-D3nvh7XvOx0I

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
