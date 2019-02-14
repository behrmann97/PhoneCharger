from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, \
    QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread, \
    QCoreApplication
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, \
    QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QProgressBar, QGroupBox
from PyQt5.Qt import QTest, QTransform, QSound


class Section(QWidget):

    def __init__(self, parent, name):
        super().__init__(parent)
        self.name_label = QLabel(name + ':', self)
        self.name_label.setGeometry(10,10, 350, 50)

        self.name_label.setFont(QFont("Times", 15))

        self.last_x = 0
        self.current_y = 50
        self.selectedButton = None

        self.show()

    def addOption(self, size, color = None, text = None, default = False):
        option = Option(self, size, color, text, default)
        if default:
            self.selectedButton = option
        if self.last_x + size >= 750:
            self.last_x = 0
            self.current_y += 80
        option.setGeometry(self.last_x + 10, self.current_y, size, size)
        self.last_x += size + 10
        option.show()

    def selectButton(self, button):
        button.changeSelected()
        if self.selectedButton:
            self.selectedButton.changeSelected()
        self.selectedButton = button
        self.parent().defaults[button.returns[0]] = button.returns[1]


class Option(QPushButton):

    def __init__(self, parent, size, color = None, text = None, default =False):
        super().__init__(parent)
        self.selected = False
        self.color = (100,100,100)
        if color:
            self.color = color
            self.returns = ['color', color]
        if not default:
            self.setStyleSheet('background-color: rgba({}, {}, {}, 40%)'.format(*self.color))
        else:
            self.selected = True
            self.setStyleSheet('background-color: rgba({}, {}, {}, 100%)'.format(*self.color))
        if text:
            self.returns = ['size', size]
            self.setText(text)
            self.setFont(QFont('Times',10))


        self.clicked.connect(lambda: self.parent().selectButton(self))

    def changeSelected(self):
        if self.selected:
            self.setStyleSheet('background-color: rgba({}, {}, {}, 40%)'.format(*self.color))
        else:
            self.setStyleSheet('background-color: rgba({}, {}, {}, 100%)'.format(*self.color))
        self.selected = not self.selected
