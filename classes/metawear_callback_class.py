from typing import Callable
from mbientlab.metawear import MetaWear, libmetawear, parse_value, POINTER
import numpy as np

from mbientlab.metawear.cbindings import *
import logging
#logger = logging.getLogger(__name__)


# Configuración del logger para el stream de datos continuo
logger = logging.getLogger('datos')
logging.getLogger('datos').setLevel(logging.INFO)

handler_datos = logging.FileHandler('./LOG/datos.log')  # Archivo de log para datos
#handler_datos = logging.FileHandler('log_datos.txt') 
formatter_datos = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler_datos.setFormatter(formatter_datos)
logger.addHandler(handler_datos)
logging.getLogger('datos').propagate = False


logger_general = logging.getLogger(__name__)
class MetawearCallback:
    # init
    def __init__(self, device, data_callback : Callable,  precision:int =2):
        """Clase de manejo de callbacks de los sensores.

        Args:
            device (_type_): El dispositivo metawear a conectar.-
            data_callback (Callable): Función callback que recibirá los datos yaw pitch y roll en radianes al recibir los datos del dispositivo.
            precision (int, optional): Dígitos decimales a mandar.. Defaults to 2.
        """
        self.device = device
        self.samples = 0
        self.callback = FnVoid_VoidP_DataP(self.data_handler)
        self.name = "MetawearCallback"
        self.tag = "[MetawearCallback] - "
        
        self._is_pending_calibration = True
        self._precision = precision
        self._data_callback = data_callback

        self.YAW_TO_CALIBRATE = 0
        self.PITCH_TO_CALIBRATE = 0
        self.ROLL_TO_CALIBRATE = 0
        
        self._position = [0, 0, 0]
        
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
        
    @property
    def data_callback(self):
        return self._data_callback

    @data_callback.setter
    def data_callback(self, data_callback):
        self._data_callback = data_callback
    
    @property
    def is_pending_calibration(self):
        return self._is_pending_calibration

    @is_pending_calibration.setter
    def is_pending_calibration(self, is_pending_calibration):
        self._is_pending_calibration = is_pending_calibration
    
    @property
    def precision(self):
        return self._precision

    @precision.setter
    def precision(self, precision):
        self._precision = precision
    
    @staticmethod
    def calibrateDegree(value, calibration_values):
        #return (abs(value  - calibration_values))%360
        return (value - calibration_values)%360 if (value  - calibration_values) >0 else (value  - calibration_values + 360)%360

    def data_handler(self, ctx, data):
        
        
        parsed_data = parse_value(data)
        yaw_origin = parsed_data.yaw
        pitch_origin = parsed_data.pitch
        roll_origin = parsed_data.roll
        heading_origin = parsed_data.heading
        logger.info(f"{self.tag}ORIG: [yaw : {round(yaw_origin, self._precision)}]\t\t[pitch : {round(pitch_origin, self._precision)}]\t\t[roll : {round(roll_origin, self._precision)}] \t\t[heading : {round(heading_origin,self._precision)}]")
        if self._is_pending_calibration:
            logger.info("{self.tag}Calibrando")
            self._is_pending_calibration = False
            self.YAW_TO_CALIBRATE = yaw_origin
            self.PITCH_TO_CALIBRATE = pitch_origin
            self.ROLL_TO_CALIBRATE = roll_origin
            self._position = [0, 0, 0]
             
        

        yaw = MetawearCallback.calibrateDegree(yaw_origin, self.YAW_TO_CALIBRATE)
        pitch = MetawearCallback.calibrateDegree(pitch_origin, self.PITCH_TO_CALIBRATE)
        roll = MetawearCallback.calibrateDegree(roll_origin, self.ROLL_TO_CALIBRATE)
        
        logger.info(f"{self.tag}EUL: [yaw : {round(yaw, self._precision)}]\t\t[pitch : {round(pitch, self._precision)}]\t\t[roll : {round(roll, self._precision)}] \t\t[heading : {round(heading_origin,self.precision)}]")
        
        yaw_r = np.deg2rad(yaw)
        pitch_r = np.deg2rad(pitch)
        roll_r = np.deg2rad(roll)
        heading_r = np.deg2rad(heading_origin)
        logger.info(f"{self.tag}RAD: [yaw : {round(yaw_r, self._precision)}]\t\t[pitch : {round(pitch_r, self._precision)}]\t\t[roll : {round(roll_r, self._precision)}]\t\t[heading : {round(heading_r,self.precision)}]")
        logger.info("")

        self.samples+= 1
        
        self.data_callback([pitch_r, roll_r, yaw_r])
        