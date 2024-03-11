
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

from qt_project.ui_controller_system import MenuUI
from PyQt5.QtCore import QThread, pyqtSignal

def start_menu() -> MenuUI:
    
    window = Worker()
    window.start()
    return window

    
def configure_menu(devices, osc_client):
    print("TODO")
    
    
    

class Worker(QThread):
    finished = pyqtSignal()  # Señal para indicar que el trabajo ha terminado

    def run(self):
        # Aquí puedes inicializar tu UI y realizar tareas pesadas
        # Por ejemplo, supongamos que tu MenuUI necesita hacer algo costoso en setupUi
        print("En la hebra Worker")
        self.app = QApplication(sys.argv)
        print("En la hebra Worker1")

        self.window = MenuUI()
        print("En la hebra Worker2")

        self.window.show()
        print("En la hebra Worker3")

        self.app.exec()
        print("En la hebra Worker4")

        #self.finished.emit()  # Emitir señal cuando hayas terminado
        