
import time
from PyQt5 import QtWidgets
import sys

from qt_project.ui_controller_system import Ui_MainScreen
from PyQt5.QtCore import QThread, pyqtSignal

import logging

from services.osc_service import down_function, up_function,left_function,right_function,in_function,out_function
logger = logging.getLogger(__name__)

class Worker(QThread):
    def __init__(self, devices):
        super().__init__()
        self.devices = devices
        
    def run(self):
        logger.info("Aquí va la lógica del sensor. Se debe comunicar por colas.")
        while 1:
            #logger.info("Hebra ")
            time.sleep(1)

def calibrate(devices):
    for device in devices:
        device.is_pending_calibration= True
        
def down_function_qt(devices, osc_client, lcd_x, lcd_y, lcd_z):
    devices, osc_client = down_function(devices, osc_client)
    update_devices_position(devices, lcd_x, lcd_y, lcd_z)

def up_function_qt(devices, osc_client, lcd_x, lcd_y, lcd_z):
    devices, osc_client = up_function(devices, osc_client)
    update_devices_position(devices, lcd_x, lcd_y, lcd_z)

def left_function_qt(devices, osc_client,  lcd_x, lcd_y, lcd_z):
    devices, osc_client = left_function(devices, osc_client)
    update_devices_position(devices, lcd_x, lcd_y, lcd_z)

def right_function_qt(devices, osc_client,  lcd_x, lcd_y, lcd_z):
    devices, osc_client = right_function(devices, osc_client)
    update_devices_position(devices, lcd_x, lcd_y, lcd_z)

def in_function_qt(devices, osc_client,  lcd_x, lcd_y, lcd_z):
    devices, osc_client = in_function(devices, osc_client)
    update_devices_position(devices, lcd_x, lcd_y, lcd_z)

def out_function_qt(devices, osc_client,  lcd_x, lcd_y, lcd_z):
    devices, osc_client = out_function(devices, osc_client)
    update_devices_position(devices, lcd_x, lcd_y, lcd_z)

def update_devices_position(devices, lcd_x, lcd_y, lcd_z):
    for device in devices:
        position = device.position
        lcd_x.display(position[0])
        lcd_y.display(position[1])
        lcd_z.display(position[2])



class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, osc_client, devices, devices_ip, osc_ip):
        super(ApplicationWindow, self).__init__()
        osc_functions = {
            "move_down" : down_function_qt,
            "move_up"   : up_function_qt,
            "move_left" : left_function_qt,
            "move_right": right_function_qt,
            "move_in"   : in_function_qt,
            "move_out"  : out_function_qt,
            
        }
        devices_function = {
            "calibrate" : calibrate
        }
        self.ui = Ui_MainScreen(osc_client, devices, osc_functions, devices_function,  devices_ip, osc_ip)
        self.ui.setupUi(self)
        self.osc_client = osc_client
        self.devices_ip=devices_ip
        self.osc_ip=osc_ip


def start_menu(osc_client, devices, devices_ip, osc_ip):
    global windows
    app = QtWidgets.QApplication(sys.argv)
    # application.ui.comboBox_aviable_ips.addItems()
    # application.ui.comboBox_aviable_ips.currentText(osc_ip)
    application = ApplicationWindow(osc_client, devices, devices_ip, osc_ip)
    application.show()
    worker = Worker(devices)
    worker.start()
    #sys.exit(app.exec_())
    windows = application
    print( app, application, worker)
    
    return application, app, worker


if __name__ == "__main__":
    start_menu()