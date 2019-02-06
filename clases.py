from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, \
    QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread, \
    QCoreApplication
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, \
    QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QProgressBar, QGroupBox
from PyQt5.Qt import QTest, QTransform, QSound
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
import time


class TextEdit(QLineEdit):

    def __init__(self, parent = None):
        super().__init__(parent)

        self.setText('ej: 12345678-9')
        self.numbers = ''
        self.digit = ''
        self.setFont(QFont("Times", 19))


    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.parent().keyboard.show()
        self.parent().error_label.hide()
        self.parent().start = time.time()
        if self.text() =='ej: 12345678-9':
             self.setText('')


    def keyPress(self, key):
        self.parent().error_label.hide()
        self.parent().start = time.time()

        if key == 'DEL':
            if self.numbers:
                end = self.numbers[len(self.numbers)-1]
                self.numbers = self.numbers[0:len(self.numbers) -1]
                self.digit = end
            else:
                self.digit = ''

        else:
            self.numbers += self.digit
            self.digit = key


        self.setText(self.numbers + '-' + self.digit)

    def isValidRut(self):
        if len(self.numbers) < 7 or len(self.numbers) > 8:
            return False
        if 'K' in self.numbers:
            return False
        multipliers = [2,3,4,5,6,7]
        counter = 0
        total = 0
        for i in self.numbers[::-1]:
            total += int(i) * multipliers[counter%6]
            counter += 1
        if self.digit == 'K' and str(11- total%11) == 10:
            return True
        if str(11 -(total%11 if total%11 !=0 else  11 )) == self.digit:
            return True
        return False

    def resetRut(self):
        self.numbers = ''
        self.digit = ''
        self.setText('ej: 12345678-9')


class Button(QPushButton):

    def __init__(self, parent, key, icon= None):
        super().__init__(parent)
        self.clicked.connect(lambda: self.parent().editor.keyPress(key))
        if icon:
            self.setIcon(QIcon(icon))
            self.setIconSize(QSize(30,30))
        else:
            self.setText(key)
            self.setFont(QFont("Times", 25))



class Keyboard(QWidget):

    def __init__(self, parent, editor):
        super().__init__(parent)
        self.editor = editor
        self.buttons = []

        for i in range(10):
            button = Button(self, str((i+1)%10))
            self.buttons.append(button)
            button.setGeometry(((i)%3* 120) + i//9 * 120, i//3 *100, 120, 100)
            button.show()
        button = Button(self, 'K')
        self.buttons.append(button)
        button.setGeometry(0,360, 120, 100)
        button.show()
        button = Button(self,'DEL','assets/delete')
        self.buttons.append(button)
        button.setGeometry(200, 360, 120, 100)
        button.show()
