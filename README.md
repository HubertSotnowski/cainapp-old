# CAINAPP 2 BETA🚧

Welcome to CAINAPP 2.0!

### What is CAIN?

##### CAIN - Channel Attention Is All You Need for Video Frame Interpolation

CAIN is a very fast interpolation network that doesn't use much vram (Ex: 5GB with fp16 for 8k)! 



### What is cainapp?



Cainapp is a gui for cain with some new things like fp16, saving frames on other threads and more! Look at the code!



## What are the requirements?

Unlike previously, Cainapp now runs on CUDA. Fortunately, it runs on the driver-based version, so the only requirements are

1. A NVidia GPU that has recently been updated

However, we cannot guarantee that you will have the best experience with lower specced hardware, so we at least suggest getting a GPU with over 2GB of VRAM for at least a decent experience.

## How to install on Windows💾


1. Download Python 3.9 📥 (https://www.python.org/ftp/python/3.9.2/python-3.9.2-amd64.exe)

2. Install Python 3.9, and remember to select "Add to PATH"

3. In cmd run 

   `pip3 install pyqt5`

   `pip3 install qdarkstyle`

   `pip3 install --pre torch torchvision torchaudio -f https://download.pytorch.org/whl/nightly/cu111/torch_nightly.html` this can need much time ⌚

   `pip3 install tqdm`

   `pip3 install opencv-python`
   
   

4. Download Ffmpeg 📥 (https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z) 

   Extract it and put 📦 ffmpeg.exe (located in the `bin` folder) in the cainapp folder📁

5. Download the model and put it into the cainapp folder📁

6. In cmd, run ` cd path/to/cainapp/ ` then ```python3 main.py```

   

## How to install on windows(kepler)

1. Download Python 3.7 📥 (https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe)

   `pip3 install pyqt5`

   `pip3 install qdarkstyle`

   ```pip install torch==1.2.0+cu92 torchvision==0.4.0+cu92 -f https://download.pytorch.org/whl/torch_stable.html``` 

   `pip3 install tqdm`

   `pip3 install opencv-python`

2. Download Ffmpeg 📥 (https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z) 

Extract it and put 📦 ffmpeg.exe in the cainapp folder📁

3. Download the model and put it into the cainapp folder📁

4. In cmd, run ` cd path/to/cainapp/ ` then ```python3 main.py```
5. Select old pytorch model in ai tab

## How to install on Debian/Ubuntu-based distributions💾


1. Install git ```sudo apt install git```

2. Clone cainapp ```git clone https://github.com/Hubert482/cainapp.git```

3. Install python 3 pip ```sudo apt install python3-pip```

4. In terminal run 

   `pip3 install pyqt5`

   `pip3 install qdarkstyle`

   `pip3 install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html` this can need much time ⌚

   `pip3 install tqdm`

   `pip3 install opencv-python-headless`

   `sudo apt install ffmpeg`

5. Download the model and put it into the cainapp folder📁

6. In terminal, run ` cd cainapp/ ` then ```python3 main.py```

Just as a precaution, this code is completely untested on Debian. If you have any feedback, let us know!

## How to install for 2 GPUs (i.e. Ampere & Kepler) ##


1. Install [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#)

2. Install the Python version for the non-Kepler GPU first. This will most likely be 3.9. `conda create -n (name) python=3.9`

3. Install the Python version for the other GPU. For Kepler, this will be 3.7. `conda create -n (name) python=3.7`

4. Continue following the set of instructions for your system, starting from after "install python"

When you wish to switch between the versions you can type in `conda deactivate` and it will disable any current Python versions active in a command prompt. Using `conda activate (name)` will enable the Python version specified by its nickname.

This process is also used if you have applications that run on different python versions. An example would be cainapp, which requires Python 3.9, and [UVR](https://github.com/Anjok07/ultimatevocalremovergui), which requires Python 3.7.


**Optional:**

**How to install tensorRT and torch2trt:**

1. install tensorRT: https://docs.nvidia.com/deeplearning/tensorrt/install-guide/index.html

2. ```bash
   git clone https://github.com/Hubert482/torch2trt/
   cd torch2trt
   python3 setup.py install
   ```

Converting a model to tensorRT:

1. Download the model converter ```git clone https://github.com/Hubert482/cain-tools.git ```

   ```cd cain-tools```

2. Convert your model! ```python3 conv_model.py --width {width of model} --height {height of model} --input "{input model path}" ``` 

3. Copy ```converted.pth``` to the cainapp folder and run!

   If you have some problems with it dm me on discord `hubert#0069`



## How to run the Discord bot🤖

Basically the same as in "how to install" but you need to install 2 more things and do some arranging

`pip3 install discord.py` 

`pip3 install requests`

Put your token in a file called `token.txt` in the main cain directory

Take your model file from before, copy it to a folder named `models`, and rename it to stable.pth.

In line 144 of 1.py, set `TensorRT=True` if you are using TRT. Otherwse, leave it as `False`

And run ```python3 1.py```

Sadly, Discord limits the file size to 8MB, so bitrate isn't high and video length is limited. Audio bitrate is also only 69kbps

## How to train 🚆

[![Open In Colab](https://camo.githubusercontent.com/84f0493939e0c4de4e6dbe113251b4bfb5353e57134ffd9fcab6b8714514d4d1/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/github/Hubert482/CAIN/blob/master/Training.ipynb) It's simple to train with colab. However, it tends to not like being connected to the google-provided GPU, so the code listed below is stolen from Hv#3868.

To keep colab connected,
```
function ConnectButton(){
    console.log("Connect pushed"); 
    document.querySelector("#top-toolbar > colab-connect-button").shadowRoot.querySelector("#connect").click() 
}
setInterval(ConnectButton,60000);
```
 ^ enter this on console (not cell)
and keep colab on foreground.

It's not really good to train in colab, due to its limitation. It takes exponentially longer the more videos you have in your training input folder. However, you could subscribe to https://cloud.google.com/gcp, and watch some youtube tutorials how to utilise its resources to colab.

## Models

https://drive.google.com/drive/folders/1Pljrfv9xjXPU2fiwvSx-D3nvh7XvOx0I

## Donate💰

If you wish to support the project, you can donate to Hubert's patreon [here](https://www.patreon.com/hubert_)!
Hubert's dogecoin and dgb wallets are also listed in the code.

Congratulations! You've read this until the end! We hope that you will have a good experience using cainapp. If you have any questions, and/or want to use the bot without hosting it yourself, join the [discord server](https://discord.gg/m42dCgVkm8)!


## CAIN Citation

```
@inproceedings{choi2020cain,
    author = {Choi, Myungsub and Kim, Heewon and Han, Bohyung and Xu, Ning and Lee, Kyoung Mu},
    title = {Channel Attention Is All You Need for Video Frame Interpolation},
    booktitle = {AAAI},
    year = {2020}
}
```

