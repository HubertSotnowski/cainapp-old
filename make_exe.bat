call conda create -n cain_build
call conda activate cain_build
call conda install python=3.8
call pip install --pre torch torchvision torchaudio -f https://download.pytorch.org/whl/nightly/cu111/torch_nightly.html
call conda install nuitka
call pip install pyqt5
call pip install tqdm
call pip install requests
call pip install glob
call pip install opencv-python
call python main.py
call nuitka --standalone --follow-imports --plugin-enable=torch --plugin-enable=numpy --plugin-enable=qt-plugins --no-prefer-source-code --include-module="torch" --plugin-enable=pylint-warnings --windows-product-name=CAINAPP --windows-file-version=0201 --windows-company-name=I_DONT_HAVE_COMPANY main.py
call conda remove --name cain_build --all