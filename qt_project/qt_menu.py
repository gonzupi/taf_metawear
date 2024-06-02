
import logging
import os
import re
import signal
import sys
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal

import services.osc_service as osc_service
from qt_project.ui_controller_system import Ui_MainScreen
from services.metawear_service import MetaWearService
from settings import (ASK_FOR_IP, BITA_IP, BITA_OSC_DEFAULT_COORDINATES,
                      BITA_OSC_PATH_POS, BITA_OSC_PATH_PRY, BITA_PORT,
                      DEVICE_MAC, OSC_IS_ENABLED)

logger = logging.getLogger(__name__)
logger_datos = logging.getLogger("datos")


def handle_sigabrt(signum, frame):
        print("SIGABRT signal received")
        
signal.signal(signal.SIGABRT, handle_sigabrt)
class ApplicationWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        signal.signal(signal.SIGABRT, handle_sigabrt)

        osc_functions = {
            "move_down" : self.down_function_qt,
            "move_up"   : self.up_function_qt,
            "move_left" : self.left_function_qt,
            "move_right": self.right_function_qt,
            "move_in"   : self.in_function_qt,
            "move_out"  : self.out_function_qt,
            "connect"   : self.start_osc,
            "set_enable_osc" : self.set_enable_osc,
        }
        devices_function = {
            "calibrate" : self.calibrate,
            "connect"   : self.connect_sensor,
            "disconnect":self.disconnect_sensor
        }
        
        devices_ip = self.get_ip()
        osc_ip = ""
        self.ui = Ui_MainScreen(None, [], osc_functions, devices_function,  devices_ip, osc_ip)
        self.ui.setupUi(self)
        self.osc_client = None
        self.devices_ip=devices_ip
        self.osc_ip=""
        self.OSC_IS_ENABLED = False
        self.sensor_service = None

    def data_callback( self, data):
        tag = "[data_callback]"
        if self.OSC_IS_ENABLED and  self.osc_client:
            logger_datos.debug(f"{tag}Enviando por osc {data}")
            self.osc_client.send_message(f"{BITA_OSC_PATH_PRY}", data)

        # self.ui.lcd_displays["pitch"].display(round(data[0], 2))
        # self.ui.lcd_displays["roll"].display(round(data[1], 2))
        # self.ui.lcd_displays["yaw"].display(round(data[2], 2)) 
        self.ui.data_signal.emit(data)
        # self.ui.add_point(self.ui.counter, data[0], data[1], data[2])
        # self.ui.counter += 1
    
    def closeEvent(self, event):
        self.disconnect_sensor()
    def on_exit(self):
        logger.info("Saliendo del programa...")
        self.disconnect_sensor()

    def start_osc(self, osc_ip, osc_port = BITA_PORT, osc_pos = BITA_OSC_PATH_POS, osc_coordinates = BITA_OSC_DEFAULT_COORDINATES):
        logger.info(f"Habilitando OSC: IP : {osc_ip} \nPORT:{osc_port}\nPOS_PATH:{BITA_OSC_PATH_POS}\nDEFAULT_COORDINATES:{BITA_OSC_DEFAULT_COORDINATES}")
        osc_client = osc_service.connect(osc_ip, osc_port)
        if not osc_service.init(osc_client, osc_pos, osc_coordinates):
            logger.warning("Problema iniciando el OSC")
            self.ui.checkBox_osc_is_enabled=False
            self.osc_client = None
        else:
            self.osc_client = osc_client
        return osc_client

    def set_enable_osc(self, is_osc_enabled):
        self.OSC_IS_ENABLED = is_osc_enabled == QtCore.Qt.Checked
        if self.OSC_IS_ENABLED:
            self.start_osc(self.ui.comboBox_aviable_ips.currentText(), self.ui.lineEdit_port.text(), self.ui.lineEdit_osc_path_pos.text(), [0, 0, 0])
        else:
            self.osc_client = None
    def get_ip(self):
        devices = ["127.0.0.1"]
        logger.info("Analizando IPs disponibles...")
        for device in os.popen('arp -a'): devices.append(device)
        for index, device in enumerate(devices):
            d = device.replace('\n', '')
            logger.info(f"{index} - {d}")
        result = []
        for data in devices:
            try:
                patron_ip = r"\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)"

                ip = re.search(patron_ip, data).group(1)
                result.append(ip)
            except Exception as e:
                logger.warning(f"Problema parseando la IP - {data}")
            
        return result

    def disconnect_sensor(self):
        try:
            if self.sensor_service is not None:
                logger.info("Desconectando dispositivo")
                self.sensor_service.disconnect()
                self.ui.pushButton_disconnect.setEnabled(False)
                
        except Exception as e:
            logger.exception("Problema desconectandome del sensor")
        finally:
            self.sensor_service = None
            
    def connect_sensor(self, device_mac):
        try:
            if self.sensor_service is not None:
                logger.info("Desconectando dispositivo")
                self.sensor_service.disconnect()
                self.ui.pushButton_disconnect.setEnabled(False)
            logger.info("Conectando dispositivo")
            self.sensor_service = MetaWearService(device_mac, self.data_callback)
            devices = self.sensor_service.connect_device()
            for device in devices:
                self.sensor_service.configure_device(device)
            self.ui.pushButton_disconnect.setEnabled(True)
            self.ui.tabWidget.setCurrentIndex(2)
        except Exception as e:
            logger.exception("Problema conectando sensor")
            self.sensor_service = None
        

    def calibrate(self, devices):
        logger.info("Calibrando")
        self.sensor_service.device.is_pending_calibration = True
        #for device in devices:
        #    device.is_pending_calibration= True
            
    def down_function_qt(self, devices, osc_client):
        if self.OSC_IS_ENABLED:
            devices, osc_client = osc_service.down_function(devices, osc_client)
        self.update_devices_display_position(devices)

    def up_function_qt(self, devices, osc_client):
        if self.OSC_IS_ENABLED:
            devices, osc_client = osc_service.up_function(devices, osc_client)
        self.update_devices_display_position(devices)

    def left_function_qt(self, devices, osc_client):
        if self.OSC_IS_ENABLED:
            devices, osc_client = osc_service.left_function(devices, osc_client)
        self.update_devices_display_position(devices)

    def right_function_qt(self, devices, osc_client):
        if self.OSC_IS_ENABLED:
            devices, osc_client = osc_service.right_function(devices, osc_client)
        self.update_devices_display_position(devices)

    def in_function_qt(self, devices, osc_client):
        if self.OSC_IS_ENABLED:
            devices, osc_client = osc_service.in_function(devices, osc_client)
        self.update_devices_display_position(devices)

    def out_function_qt(self, devices, osc_client):
        if self.OSC_IS_ENABLED:
            devices, osc_client = osc_service.out_function(devices, osc_client)
        self.update_devices_display_position(devices)

    def update_devices_display_position(self, devices):
        logger.info("Actualizando LCDs")
        for device in devices:
            position = device.position
            #lcd_x.display(position[0])
            self.ui.lcd_displays["x"].display(position[0])
            #lcd_y.display(position[1])
            self.ui.lcd_displays["y"].display(position[1])
            #lcd_z.display(position[2])
            self.ui.lcd_displays["z"].display(position[2])
        
def start_menu():
    global windows
    app = QtWidgets.QApplication(sys.argv)

    application = ApplicationWindow()
    application.show()
    windows = application
    print( app, application)
    
    return application, app 


if __name__ == "__main__":
    start_menu()