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

#############
import json
import glob
global OutputPath
OutputPath=""

##############

class UI(QMainWindow):
    def __init__(self):
        ###############
        def SelectOutput():
            global OutputPath
            OutputPath = input_and_output.select_path()
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
            input_and_output.ExportVideo(dir_path=f"{OutputPath}/cain/", proresmode=prores_mode, type=self.comboBox_5.currentText(), fps=f"{video[0]}", factor=self.comboBox_2.currentText(), filetype=self.comboBox.currentText(), useprores=self.checkBox_3.isChecked(),line=self.lineEdit_3.text() )


        def SelectVideo():
            global video
            video = input_and_output.SelectInput()
            if video[5]==True:
                 self.lineEdit.setText(f"-vf scale={round(round(round(video[4])/8)*8)}:{round(round(round(video[3])/8)*8)}:flags=lanczos")

            print(video)
        def extract():
            input_and_output.ExtractFramesOrSplit(Type=self.comboBox_5.currentText(), chunksize="0", dir_path=OutputPath, Line=self.lineEdit.text(), input=video[2])
        def interpolate():
            if self.comboBox_2.currentText()=="2x":
                generate.interpolation(batch_size=int(self.comboBox_6.currentText()), img_fmt=self.comboBox_5.currentText(), torch_device="cuda", temp_img = f"{OutputPath}/cain/frames", GPUid=self.spin_3.value(), GPUid2=self.checkBox_7.isChecked(), fp16=self.checkBox_4.isChecked(), modelp=self.comboBox_4.currentText())
            else:
                generate.interpolation(batch_size=int(self.comboBox_6.currentText()), img_fmt=self.comboBox_5.currentText(), torch_device="cuda", temp_img = f"{OutputPath}/cain/frames", GPUid=self.spin_3.value(), GPUid2=self.checkBox_7.isChecked(), fp16=self.checkBox_4.isChecked(), modelp=self.comboBox_4.currentText())
                generate.interpolation(batch_size=int(self.comboBox_6.currentText()), img_fmt=self.comboBox_5.currentText(), torch_device="cuda", temp_img = f"{OutputPath}/cain/frames", GPUid=self.spin_3.value(), GPUid2=self.checkBox_7.isChecked(), fp16=self.checkBox_4.isChecked(), modelp=self.comboBox_4.currentText())

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
        ##########################
        self.show()
        app.setStyle('fusion')
        app.setStyleSheet(dark_stylesheet)

app = QApplication(sys.argv)
window = UI()
app.exec()
