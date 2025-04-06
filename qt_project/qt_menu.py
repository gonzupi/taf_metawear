import logging
import os
import re
import signal
import sys
import time
from typing import Type

from PyQt5 import QtCore, QtWidgets

import services.osc_service as osc_service
from qt_project.ui_controller_system import Ui_MainScreen
from services.SensorInterface import SensorInterface
from settings import (ASK_FOR_IP, OSC_RECIVER_IP, OSC_DEFAULT_COORDINATES,
                      OSC_RECIVER_PATH_POS, OSC_RECIVER_PATH_PRY, OSC_RECIVER_PORT,
                      IMU_DEVICE_MAC, OSC_IS_ENABLED, POS_STEP)

logger = logging.getLogger(__name__)
logger_datos = logging.getLogger("datos")
import numpy as np


def quaternion_to_euler_angle_vectorized1(arr):
    w = arr[0] 
    x = arr[1]
    y = arr[2] 
    z = arr[3] 
    ysqr = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    X = (np.arctan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = np.where(t2 > +1.0, +1.0, t2)
    # t2 = +1.0 if t2 > +1.0 else t2

    t2 = np.where(t2 < -1.0, -1.0, t2)
    # t2 = -1.0 if t2 < -1.0 else t2
    Y =(np.arcsin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    Z = (np.arctan2(t3, t4))

    return [X, Y, Z]


def handle_sigabrt(signum, frame):
        print("SIGABRT signal received")

signal.signal(signal.SIGABRT, handle_sigabrt)
class ApplicationWindow(QtWidgets.QMainWindow):

    def __init__(self, sensorClassType : Type[SensorInterface]):
        super(ApplicationWindow, self).__init__()
        signal.signal(signal.SIGABRT, handle_sigabrt)

        osc_functions = {
            "move_down": self.down_function_qt,
            "move_up": self.up_function_qt,
            "move_left": self.left_function_qt,
            "move_right": self.right_function_qt,
            "move_out": self.out_function_qt,
            "move_in": self.in_function_qt,
            "connect": self.start_osc,
            "set_enable_osc": self.set_enable_osc,
            "data_callback": self.data_callback,
        }
        devices_function = {
            "calibrate" : self.calibrate,
            "connect"   : self.connect_sensor,
            "disconnect":self.disconnect_sensor
        }

        devices_ip = self.get_ip()
        osc_ip = ""
        self.sensorClassType = sensorClassType
        self.devices = []
        self.ui = Ui_MainScreen(
            None, self.devices, osc_functions, devices_function, devices_ip, osc_ip
        )
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
            euler = quaternion_to_euler_angle_vectorized1(data)
            self.osc_client.send_message(
                f"{self.ui.lineEdit_osc_path_pry.text()}",
                euler,
                # [
                #     data[3],
                #     data[1],
                #     data[2],
                #     data[0],
                #     # data[2],
                #     # data[0],
                #     # data[1],
                #     # data[3],
                #     # data[2],
                #     # data[3],
                #     # data[1],
                #     # data[0],
                # ],
            )

            # self.osc_client.send_message(
            #     f"{BITA_OSC_PATH_PRY}", data
            # )  # pitch_r, roll_r, yaw_r, heading

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

    def start_osc(self, osc_ip, osc_port = OSC_RECIVER_PORT, osc_pos = OSC_RECIVER_PATH_POS, osc_coordinates = OSC_DEFAULT_COORDINATES):
        logger.info(
            f"Habilitando OSC: IP : {osc_ip} \nPORT:{osc_port}\nPOS_PATH:{osc_pos}\nDEFAULT_COORDINATES:{osc_coordinates}"
        )
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
            self.sensor_service = self.sensorClassType(device_mac, self.data_callback)
            self.devices = self.sensor_service.connect()
            self.ui.devices = self.devices
            self.ui.pushButton_disconnect.setEnabled(True)
            self.ui.tabWidget.setCurrentIndex(2)
            # self.ui.sensors.push(self.sensor_service)
        except Exception as e:
            logger.exception("Problema conectando sensor")
            self.sensor_service = None

    def calibrate(self, devices):
        logger.info("Calibrando")
        self.sensor_service.device.is_pending_calibration = True
        # for device in devices:
        #    device.is_pending_calibration= True

    def down_function_qt(self, devices, osc_client):
        if self.OSC_IS_ENABLED:
            logger.info("Moviendo hacia ABAJO")
            devices, osc_client = osc_service.down_function(self.devices, osc_client)
        else:
            for device in devices:
                position = device.position
                pos_x = position[0]
                pos_y = position[1]
                pos_z = position[2]

                pos_y = pos_y - POS_STEP
                device.position = [pos_x, pos_y, pos_z]
        self.update_devices_display_position(devices)

    def up_function_qt(self, devices, osc_client):
        logger.info("Moviendo hacia ARRIBA")
        if self.OSC_IS_ENABLED:
            devices, osc_client = osc_service.up_function(self.devices, osc_client)
        else:
            for device in devices:
                position = device.position
                pos_x = position[0]
                pos_y = position[1]
                pos_z = position[2]

                pos_y = pos_y + POS_STEP
                device.position = [pos_x, pos_y, pos_z]
        self.update_devices_display_position(devices)

    def left_function_qt(self, devices, osc_client):
        logger.info("Moviendo hacia IZQUIERDA")

        if self.OSC_IS_ENABLED:
            devices, osc_client = osc_service.left_function(self.devices, osc_client)
        else:
            for device in devices:
                position = device.position
                pos_x = position[0]
                pos_y = position[1]
                pos_z = position[2]

                pos_x = pos_x - POS_STEP
                device.position = [pos_x, pos_y, pos_z]
        self.update_devices_display_position(devices)

    def right_function_qt(self, devices, osc_client):
        logger.info("Moviendo hacia DERECHA")
        if self.OSC_IS_ENABLED:
            devices, osc_client = osc_service.right_function(self.devices, osc_client)
        else:
            for device in devices:
                position = device.position
                pos_x = position[0]
                pos_y = position[1]
                pos_z = position[2]

                pos_x = pos_x + POS_STEP
                device.position = [pos_x, pos_y, pos_z]
        self.update_devices_display_position(devices)

    def in_function_qt(self, devices, osc_client):
        logger.info("Moviendo hacia DENTRO")
        if self.OSC_IS_ENABLED:
            devices, osc_client = osc_service.in_function(self.devices, osc_client)
        else:
            for device in devices:
                position = device.position
                pos_x = position[0]
                pos_y = position[1]
                pos_z = position[2]

                pos_z = pos_z + POS_STEP
                device.position = [pos_x, pos_y, pos_z]
        self.update_devices_display_position(devices)

    def out_function_qt(self, devices, osc_client):
        logger.info("Moviendo hacia FUERA")
        if self.OSC_IS_ENABLED:
            devices, osc_client = osc_service.out_function(self.devices, osc_client)
        else:
            for device in devices:
                position = device.position
                pos_x = position[0]
                pos_y = position[1]
                pos_z = position[2]

                pos_z = pos_z - POS_STEP

                device.position=[pos_x, pos_y, pos_z]
        self.update_devices_display_position(devices)

    def update_devices_display_position(self, devices):
        logger.info("Actualizando LCDs")

        for device in self.devices:
            position = device.position
            logger.info(f"Posiciones del device : {position}")
            # lcd_x.display(position[0])
            if "X_POS" in self.ui.lcd_displays:
                self.ui.lcd_displays["X_POS"].display(position[0])
            # lcd_y.display(position[1])
            if "Y_POS" in self.ui.lcd_displays:
                self.ui.lcd_displays["Y_POS"].display(position[1])
            # lcd_z.display(position[2])
            if "Z_POS" in self.ui.lcd_displays:
                self.ui.lcd_displays["Z_POS"].display(position[2])


def start_menu(sensorClassType : Type[SensorInterface]):
    global windows
    app = QtWidgets.QApplication(sys.argv)

    application = ApplicationWindow(sensorClassType)
    application.show()
    windows = application
    return application, app 


if __name__ == "__main__":
    start_menu()
