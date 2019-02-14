from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, \
    QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread, \
    QCoreApplication, QDir
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, \
    QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QProgressBar, QGroupBox, QFileDialog, QComboBox
from PyQt5.Qt import QTest, QTransform, QSound
from config_clases import Section
import json


class Window(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setGeometry(400, 30, 800, 1000)
        self.show()
        with open('defaults.json') as json_file:
            self.defaults = json.load(json_file)
        self.colors = Section(self, "Color")
        self.colors.setGeometry(30, 10, 750, 300)

        for i in range(3):
            for j in range(2):
                for k in range(4):
                    self.colors.addOption(70, (i * 70, j *120, k * 60), default = self.defaults['color'] == [i * 70, j * 120, k * 60])
        self.colors.addOption(70, (61,83,103), default = self.defaults['color'] == [61,83,103])
        self.colors.addOption(70, (255,255,255))

        self.sizes = Section(self, "Tamaño del botón flotante")
        self.sizes.setGeometry(30, 320, 700, 300)
        self.sizes.addOption(75, text = 'pequeño', default = self.defaults['size'] == 75)
        self.sizes.addOption(140, text = 'mediano', default = self.defaults['size'] == 140 )
        self.sizes.addOption(195, text = 'grande (recomendado)', default =self.defaults['size'] == 195 )
        self.sizes.addOption(250, text = 'muy grande', default = self.defaults['size'] == 250)

        self.select_image = Section(self, "Seleccionar Imagen")
        self.select_image.setGeometry(30, 620, 700, 50)

        self.image_button = QPushButton(self.defaults['image'], self)
        self.image_button.setFont(QFont("Times",12))
        self.image_button.setGeometry(30, 680, 300, 40)
        self.image_button.clicked.connect(self.selectFile)
        self.image_button.show()

        self.image_shower = QLabel(self)
        self.image_shower.setGeometry(350, 680, 95, 95)
        self.image_shower.setPixmap(QPixmap(self.defaults['image']).scaled(95, 95))
        self.image_shower.show()

        self.times = Section(self, "Tiempo de inactividad")
        self.times.setGeometry(30, 785, 700, 50)

        self.time_shower = QLabel(str(self.defaults['time']), self)
        self.time_shower.setGeometry(350, 840, 20, 50)
        self.time_shower.setFont(QFont("Times",15))
        self.time_shower.show()

        self.add_time = QPushButton('+', self)
        self.add_time.setGeometry(380, 840, 50,50)
        self.add_time.clicked.connect(self.addTime)
        self.add_time.show()

        self.substract_time = QPushButton('-', self)
        self.substract_time.setGeometry(290, 840, 50, 50)
        self.substract_time.clicked.connect(self.subTime)
        self.substract_time.show()

        self.save_button = QPushButton("Guardar",self)
        self.save_button.setGeometry(350, 950, 100, 50)
        self.save_button.setFont(QFont("Times",15))
        self.save_button.clicked.connect(self.saveFile)
        self.save_button.show()

    def saveFile(self):
        with open('defaults.json', 'w') as outfile:
            json.dump(self.defaults, outfile)
        exit()

    def addTime(self):
        self.defaults['time'] += 1
        self.time_shower.setText(str(self.defaults['time']))

    def subTime(self):
        self.defaults['time'] -= 1
        self.time_shower.setText(str(self.defaults['time']))

    def selectFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Single File', '' , '*.png')
        self.defaults['image'] = fileName
        if len(fileName) > 15:
            fileName = '...' + fileName[-13:]
        self.image_button.setText(fileName)
        self.image_shower.setPixmap(QPixmap(self.defaults['image']).scaled(95, 95))






if __name__ == "__main__":
    app = QApplication([])
    editor = Window()
    app.exec_()
