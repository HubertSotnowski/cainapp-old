call conda create -n cain_build
call conda activate cain_build
call conda install python=3.8
call pip install --pre torch torchvision torchaudio -f https://download.pytorch.org/whl/nightly/cu111/torch_nightly.html
call pip install nuitka
call pip install pyqt5
call pip install tqdm
call pip install requests
call pip install opencv-python