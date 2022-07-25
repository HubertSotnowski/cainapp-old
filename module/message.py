try:
    from PyQt6.QtWidgets import *
    from PyQt6.QtGui import *
    from PyQt6 import uic
except:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5 import uic
import sys
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        #self.setMinimumSize(QSize(300, 200))    
        self.setWindowTitle("PyQt messagebox example - pythonprogramminglanguage.com") 

        pybutton = QPushButton('Show messagebox', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200,64)
        pybutton.move(50, 50)        

    def clickMethod(self):
        QMessageBox.about(self, "Title", "Message")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec())