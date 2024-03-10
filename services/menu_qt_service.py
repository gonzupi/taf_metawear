from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
import sys

import services.metawear_service as metawear_service
from settings import BITA_OSC_PATH_POS, OSC_IS_ENABLED, POS_STEP

class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.devices = []  # Esta lista debería ser actualizada con tus dispositivos reales
        self.osc_client = None  # Inicializa tu cliente OSC aquí
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Controlador BITA OSC y Metawear')
        layout = QVBoxLayout()

        # Configuración de IP y MAC
        self.ipLineEdit = QLineEdit()
        self.macLineEdit = QLineEdit()
        self.ipLineEdit.setPlaceholderText('Introduce la IP de BiTA')
        self.macLineEdit.setPlaceholderText('Introduce la MAC del IMU')

        layout.addWidget(QLabel('BITA IP:'))
        layout.addWidget(self.ipLineEdit)
        layout.addWidget(QLabel('DEVICE MAC:'))
        layout.addWidget(self.macLineEdit)

        # Botones de control
        controlLayout = QHBoxLayout()
        self.addButton('Arriba', controlLayout, self.moveUp)
        self.addButton('Abajo', controlLayout, self.moveDown)
        self.addButton('Izquierda', controlLayout, self.moveLeft)
        self.addButton('Derecha', controlLayout, self.moveRight)
        layout.addLayout(controlLayout)
        self.setLayout(layout)

    def addButton(self, text, layout, function):
        button = QPushButton(text)
        button.clicked.connect(function)
        layout.addWidget(button)

    # Funciones de movimiento
    def moveUp(self):
        # Implementa el movimiento hacia arriba aquí
        pass

    def moveDown(self):
        # Implementa el movimiento hacia abajo aquí
        pass

    def moveLeft(self):
        # Implementa el movimiento hacia la izquierda aquí
        pass

    def moveRight(self):
        # Implementa el movimiento hacia la derecha aquí
        pass

# Otros métodos para mover 'in', 'out', etc., y métodos auxiliares (calibración, reinicio, etc.)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec_())
