from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, \
    QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread, \
    QCoreApplication
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, \
    QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QProgressBar, QGroupBox
from PyQt5.Qt import QTest, QTransform, QSound
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from clases import TextEdit, Keyboard
import json
import time
import serial

SCREEN_WIDTH *= 1.25
SCREEN_HEIGHT *=1.25


class Window(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.ser = serial.Serial('COM3')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.show()
        self.start = time.time()
        self.small = True

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_time)
        self.smallScreen()

        self.background = QLabel(self)
        self.background.setGeometry(0,0, SCREEN_WIDTH,SCREEN_HEIGHT)
        self.background.setStyleSheet("background-color: #3d5367")

        self.newfont = QFont("Times", 30)
        self.smallfont = QFont("Times", 15)
        self.errorfont = QFont("Times", 10)

        self.icon = QLabel(self)
        self.icon.setGeometry(SCREEN_WIDTH/2 - 200, SCREEN_HEIGHT/4 - 250, 400, 400)
        self.icon.setPixmap(QPixmap('assets/logo-blanco').scaled(400,400))

    def check_time(self):
        newtime = time.time()
        if not self.small and newtime - self.start >= 5:
            self.smallScreen()


    def smallScreen(self):
        if not self.small:
            self.charge_button.hide()
            self.take_button.hide()
            self.cancel_button.hide()
            self.rut_editor.hide()
            self.enter_button.hide()
            self.error_label.hide()
            self.keyboard.hide()
            self.box_button.hide()
            self.box_text.hide()
            self.text.hide()
        self.timer.stop()
        self.small = True
        self.setGeometry(SCREEN_WIDTH-200, SCREEN_HEIGHT -200, 195, 195)
        self.small_icon = QLabel(self)
        self.small_icon.setPixmap(QPixmap('assets/Loguito').scaled(195,195))
        self.small_icon.show()

    def bigScreen(self):
        self.small_icon.hide()
        self.start = time.time()
        self.small = False
        self.setGeometry(0,0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.timer.start(500)
        with open('data.txt') as json_file:
            self.boxes = json.load(json_file)
        self.show()
        self.background.show()
        self.icon.show()

        self.charge_button = QPushButton('', self)
        self.charge_button.setIcon(QIcon('assets/Cargar'))
        self.charge_button.setIconSize(QSize(400,400))
        self.charge_button.setGeometry(SCREEN_WIDTH/2 - 500, SCREEN_HEIGHT/4 + 150, 400, 400)
        self.charge_button.clicked.connect(self.charge)
        self.charge_button.setFont(self.smallfont)

        self.take_button = QPushButton('', self)
        self.take_button.setIcon(QIcon('assets/Retirar'))
        self.take_button.setIconSize(QSize(400,400))
        self.take_button.setGeometry(SCREEN_WIDTH/2 + 100, SCREEN_HEIGHT/4 + 150, 400, 400)
        self.take_button.clicked.connect(self.take)
        self.take_button.setFont(self.smallfont)

        self.text = QLabel('Ingresa tu RUT :', self)
        self.text.setStyleSheet("color: white")
        self.text.setGeometry(SCREEN_WIDTH/2 - 400, SCREEN_HEIGHT/4 + 150, 400, 60)
        self.text.setFont(self.newfont)

        self.rut_editor = TextEdit(self)
        self.rut_editor.setGeometry(SCREEN_WIDTH/2 + 50, SCREEN_HEIGHT/4 + 150, 250, 60)

        self.enter_button = QPushButton('Ingresar', self)
        self.enter_button.setGeometry(SCREEN_WIDTH/2 + 300, SCREEN_HEIGHT/4 + 150, 120, 60)
        self.enter_button.clicked.connect(self.EnterRut)
        self.enter_button.setFont(QFont("Times", 17))

        self.error_label = QLabel('RUT inválido', self)
        self.error_label.setGeometry(SCREEN_WIDTH/2+250, SCREEN_HEIGHT/4 + 220, 200, 60)
        self.error_label.setFont(self.errorfont)
        self.error_label.setStyleSheet('color:red')

        self.keyboard = Keyboard(self, self.rut_editor)
        self.keyboard.setGeometry(SCREEN_WIDTH/2 -275, SCREEN_HEIGHT/4 + 250, 360, 400)


        self.box_text = QLabel(self)
        self.box_text.setGeometry(SCREEN_WIDTH/2 - 200, SCREEN_HEIGHT/4 + 100, 400, 200)
        self.box_text.setFont(self.smallfont)

        self.box_button = QPushButton('Cerrar casilla', self)
        self.box_button.setFont(self.smallfont)
        self.box_button.setGeometry(SCREEN_WIDTH/2 - 230, SCREEN_HEIGHT/4 + 320, 160, 50 )
        self.box_button.clicked.connect(self.closeBox)

        self.cancel_button = QPushButton('Cancelar',self)
        self.cancel_button.setFont(self.smallfont)
        self.cancel_button.setGeometry(SCREEN_WIDTH/2 +180, SCREEN_HEIGHT/4 + 320, 160, 50)
        self.cancel_button.clicked.connect(self.setUp)

        self.setUp()

    def setUp(self):

        self.rut = ''
        self.rut_editor.resetRut()

        self.taking = False
        self.charge_button.show()
        self.take_button.show()

        self.text.hide()
        self.rut_editor.hide()
        self.enter_button.hide()

        self.box_text.hide()
        self.box_button.hide()
        self.cancel_button.hide()
        self.keyboard.hide()
        self.error_label.hide()


    def charge(self):
        self.start = time.time()
        self.box_text.hide()
        self.cancel_button.show()
        self.taking = False
        if not self.getBox():
            self.box_text.show()
            self.box_text.setText('''Lo sentimos, en este
momento no hay casillas disponibles''')
        else:
            self.text.show()
            self.rut_editor.show()
            self.enter_button.show()

        self.charge_button.hide()
        self.take_button.hide()
        self.box_button.hide()

    def take(self):
        self.start = time.time()
        self.taking = True
        self.text.show()
        self.rut_editor.show()
        self.enter_button.show()
        self.cancel_button.show()

        self.charge_button.hide()
        self.take_button.hide()

        self.box_text.hide()
        self.box_button.hide()

    def mousePressEvent(self, event):
        self.start = time.time()
        if self.small:
            self.hide()
            self.bigScreen()
        else:
            self.keyboard.hide()

    def EnterRut(self):
        self.start = time.time()
        if self.rut_editor.isValidRut():
            self.keyboard.hide()
            self.enter_button.hide()
            self.text.hide()
            self.rut_editor.hide()
            self.rut = self.rut_editor.numbers

            if self.taking:
                box = self.openBox()
                self.box_text.show()
                if box:
                    self.box_text.setText('''Por favor, retira tu celular
    en la casilla número {}'''.format(box))
                else:
                    self.box_text.setText('''No hay ninguna casilla
                    asignada a ese RUT''')
                self.cancel_button.show()

            else:
                box = self.getBox()
                self.box_text.show()
                if box != 'MAX':
                    self.box_text.setText('''Por favor, deja tu celular
    en la casilla número {}'''.format(box))
                    self.arduino_write(int(box))

                    self.box_button.show()
                else:
                    self.box_text.setText('''Ya hay una casilla asignada a
    este RUT''')

                self.cancel_button.show()

        else:
            self.error_label.show()


    def getBox(self):
        for i in self.boxes:
            if self.boxes[i] == self.rut:
                return 'MAX'
        for i in self.boxes:
            if not self.boxes[i]:
                return i
        return False


    def closeBox(self):
        self.start = time.time()
        self.boxes[self.getBox()] = self.rut
        with open('data.txt', 'w') as file:
            json.dump(self.boxes, file)
        self.setUp()

    def openBox(self):
        self.start = time.time()
        for i in self.boxes:
            if self.boxes[i] == self.rut:
                self.boxes[i] = False
                with open('data.txt', 'w') as file:
                    json.dump(self.boxes, file)
                return i
        return False

    def arduino_write(self, b_numer):
        try:
            self.ser.write(b_numer)
            return True
        except:
            return False







if __name__ == "__main__":
    app = QApplication([])
    editor = Window()
    app.exec_()
