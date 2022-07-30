try:
    from PyQt6.QtWidgets import *
    from PyQt6.QtGui import *
    from PyQt6 import uic
except:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5 import uic


def select_path():
    global dir_path
    dir_path = QFileDialog.getSaveFileName(None, "Open file", "video", ".mkv")
    print(dir_path)
    return dir_path[0] + dir_path[1]


def SelectInputb():

    filename = QFileDialog.getOpenFileName()

    return filename[0]
