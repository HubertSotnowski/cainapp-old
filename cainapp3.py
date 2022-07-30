try:
    from PyQt6.QtWidgets import *
    from PyQt6.QtGui import *
    from PyQt6 import uic
except:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5 import uic
import tqdm
import platform
import os
import torch
import glob
import sys

ossystem = platform.system()
from module.interpolation import *
from module.gui import *

import os
from os.path import exists
from module.video import *

debug = True


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("ui.ui", self)
        self.show()
        print("your current gpu is" + str(torch.cuda.current_device()))
        for file in glob.glob("models/*.pt"):
            print("Found model:" + file)
            self.modellist.addItem(f"{file}")

        def SelectInput():
            global InputPath
            InputPath = SelectInputb()
            self.label_10.setText(InputPath)

        def SelectOutput():
            global OutputPath
            OutputPath = select_path()
            self.label_12.setText(OutputPath)

        self.pushButton_3.clicked.connect(SelectInput)
        self.pushButton_4.clicked.connect(SelectOutput)

        def interpolateb():
            try:
                print(os.path.split(OutputPath)[0])
                if self.precission.currentText() == "fp16":
                    fp16 = True
                else:
                    fp16 = False
                if self.colorspace.currentText() == "YUV":
                    YUV = True
                else:
                    YUV = False
                if exists("temp.mkv"):
                    os.remove("temp.mkv")
                if exists("temp-v.mkv"):
                    os.remove("temp-v.mkv")
                os.system(
                    f"ffmpeg -y -i '{InputPath}' -c:a copy -vn '{os.path.split(OutputPath)[0]}/temp.mkv'"
                )

                QApplication.processEvents()
                interpolate(
                    self,
                    self.Gpuid.value(),
                    fp16,
                    self.modellist.currentText(),
                    self.ffmpegline.text(),
                    YUV,
                    getvideoinfo(InputPath),
                    InputPath,
                    OutputPath,
                    self.progressBar,
                    self.label_2,
                )
                if exists(f"{os.path.split(OutputPath)[0]}/temp.mkv"):
                    os.system(
                        f"ffmpeg -y -i '{os.path.split(OutputPath)[0]}/temp.mkv' -i '{os.path.split(OutputPath)[0]}/temp-v.mkv' -c copy '{OutputPath}'"
                    )
                else:
                    os.system(
                        f"ffmpeg -y -i '{os.path.split(OutputPath)[0]}/temp-v.mkv' -c copy '{OutputPath}'"
                    )
                if exists(f"{os.path.split(OutputPath)[0]}/temp-v.mkv"):
                    os.remove(f"{os.path.split(OutputPath)[0]}/temp-v.mkv")
                if exists(f"{os.path.split(OutputPath)[0]}/temp.mkv"):
                    os.remove(f"{os.path.split(OutputPath)[0]}/temp.mkv")
            except Exception as e:
                QMessageBox.warning(self, "warning", f"warning:\n{e}")

        self.Interpolatebutton.clicked.connect(interpolateb)


app = QApplication(sys.argv)
app.setStyle("fusion")

window = UI()
app.exec()
