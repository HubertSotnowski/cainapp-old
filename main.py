import sys, os
import shutil

################
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog
from PyQt5 import uic
import qdarkstyle
dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()

#################
import generate
import input_and_output as input_and_output
import save_loda
#############
import json
import time
import glob
global OutputPath
OutputPath=""
import platform
os.system("export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64")

ossystem=platform.system()
print(ossystem)
##############

class UI(QMainWindow):
    def __init__(self):
        ###############
        def SelectOutput():
            global OutputPath
            OutputPath = input_and_output.select_path()
            self.label_14.setText(OutputPath)
        def encode():
            os.system('del "frame_list.txt"')
            if self.comboBox_3.currentText()=="lt":
                prores_mode=1
            if self.comboBox_3.currentText()=="standard":
                prores_mode=2
            if self.comboBox_3.currentText()=="hq":
                 prores_mode=3
            if self.comboBox_3.currentText()=="4444":
                 prores_mode=4
            input_and_output.list_frame(dir=f"{OutputPath}/cain/frames", text_path=f"{OutputPath}/cain/")
            time.sleep(2) 
            input_and_output.ExportVideo(dir_path=f"{OutputPath}/cain/", proresmode=prores_mode, imtype=self.comboBox_5.currentText(), fps=f"{video[0]}", factor=self.comboBox_2.currentText(), filetype=self.comboBox.currentText(), useprores=self.checkBox_3.isChecked(),line=self.lineEdit_3.text() )
        def load():
            load = save_loda.load()
            self.lineEdit.setText(load[0])
            self.comboBox_5.setCurrentText(load[1])
            self.lineEdit_3.setText(load[2])
            self.comboBox.setCurrentText(load[3])
            self.checkBox_3.setChecked(load[4])
            self.comboBox_3.setCurrentText(load[5])
            self.comboBox_2.setCurrentText(load[6])
            self.checkBox_4.setChecked(load[7])
            self.comboBox_6.setCurrentText(load[8])
            self.comboBox_4.setCurrentText(load[9])
            self.checkBox_7.setChecked(load[10])
            self.spin_3.setValue(int(load[10]))
        def saveset():
            save_loda.save(self.lineEdit.text(), self.comboBox_5.currentText(), self.lineEdit_3.text(), self.comboBox.currentText(), self.checkBox_3.isChecked(), self.comboBox_3.currentText(), self.comboBox_2.currentText(), self.checkBox_4.isChecked(),  self.comboBox_6.currentText(), self.comboBox_4.currentText(), self.checkBox_7.isChecked(), self.spin_3.value())
        def SelectVideo():
            global video
            video = input_and_output.SelectInput()
            self.label_15.setText(video[2])
            if video[5]==True:
                 self.lineEdit.setText(f"-vf scale={round(round(round(video[4])/8)*8)}:{round(round(round(video[3])/8)*8)}:flags=lanczos")

            print(video)
        def extract():
            input_and_output.ExtractFramesOrSplit(Type=self.comboBox_5.currentText(), chunksize="0", dir_path=OutputPath, Line=self.lineEdit.text(), input=video[2])
        def interpolate():
            if self.comboBox_2.currentText()=="2x":
                generate.interpolation(batch_size=int(self.comboBox_6.currentText()), img_fmt=self.comboBox_5.currentText(), torch_device="cuda", temp_img = f"{OutputPath}/cain/frames", GPUid=self.spin_3.value(), GPUid2=self.checkBox_7.isChecked(), fp16=self.checkBox_4.isChecked(), modelp=self.comboBox_4.currentText(), TensorRT=self.checkBox.isChecked())
            else:
                generate.interpolation(batch_size=int(self.comboBox_6.currentText()), img_fmt=self.comboBox_5.currentText(), torch_device="cuda", temp_img = f"{OutputPath}/cain/frames", GPUid=self.spin_3.value(), GPUid2=self.checkBox_7.isChecked(), fp16=self.checkBox_4.isChecked(), modelp=self.comboBox_4.currentText(), TensorRT=self.checkBox.isChecked())
                generate.interpolation(batch_size=int(self.comboBox_6.currentText()), img_fmt=self.comboBox_5.currentText(), torch_device="cuda", temp_img = f"{OutputPath}/cain/frames", GPUid=self.spin_3.value(), GPUid2=self.checkBox_7.isChecked(), fp16=self.checkBox_4.isChecked(), modelp=self.comboBox_4.currentText(), TensorRT=self.checkBox.isChecked())

        def all():
            extract()
            interpolate()
            encode()


        ###############
        super(UI, self).__init__()
        uic.loadUi("form.ui", self)
        ##########################
        for file in glob.glob("*.pth"):
            print(file)
            self.comboBox_4.addItem(f"{file}")
        self.pushButton.clicked.connect(extract)
        self.pushButton3.clicked.connect(SelectVideo)
        self.pushButton_2.clicked.connect(SelectOutput)
        self.pushButton_4.clicked.connect(interpolate)
        self.pushButton_3.clicked.connect(encode)
        self.pushButton_5.clicked.connect(all)
        self.pushButton_6.clicked.connect(saveset)
        self.pushButton_7.clicked.connect(load)
        ##########################
        self.show()
        app.setStyle('fusion')
        app.setStyleSheet(dark_stylesheet)

app = QApplication(sys.argv)
window = UI()
app.exec()
