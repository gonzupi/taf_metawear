import logging
import os
import signal
from typing import Callable, List

import numpy as np
import quaternion

from log_setup import LOGS_FILE_PATH
from mbientlab.metawear import POINTER, MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from services.quaternion_service import (quaternion_inverse,
                                         quaternion_to_euler_rads)
from settings import MODE_UI

#logger = logging.getLogger(__name__)


# Configuración del logger para el stream de datos continuo
logger = logging.getLogger('datos')
logging.getLogger('datos').setLevel(logging.INFO)

os.makedirs(LOGS_FILE_PATH, exist_ok=True)
handler_datos = logging.FileHandler(os.path.join(LOGS_FILE_PATH,'datos.csv'))  # Archivo de log para datos
#handler_datos = logging.FileHandler('log_datos.txt') 
formatter_datos = logging.Formatter(f'%(asctime)s;%(message)s')
handler_datos.setFormatter(formatter_datos)
logger.addHandler(handler_datos)
logging.getLogger('datos').propagate = False

def handle_sigabrt(signum, frame):
        print("SIGABRT signal received")
        
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
        signal.signal(signal.SIGABRT, handle_sigabrt)
        self.device = device
        self.samples = 0
        self.callback = FnVoid_VoidP_DataP(self.data_handler)
        self.name = "MetawearCallback"
        self.tag = "[MetawearCallback] - "
        
        self._is_pending_calibration = True
        self._precision = precision
        self._data_callback = data_callback

        self.YAW_TO_CALIBRATE   = 0
        self.PITCH_TO_CALIBRATE = 0
        self.ROLL_TO_CALIBRATE  = 0
        self.QUATERNION_TO_CALIBRATE = None
        
        self._position = [0, 0, 0]
        
    @property
    def position(self)-> List[float]:
        return self._position

    @position.setter
    def position(self, position:List[float]):
        logger.info(f"Actualizando posición virtual a {position}")
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
        if str(type(parsed_data)) == "<class 'mbientlab.metawear.cbindings.Quaternion'>":
            if MODE_UI == "QUATERNIONS":
                return self.data_handler_quaternions(ctx, parsed_data)
            elif MODE_UI == "EULER":
                return self.data_handler_quaternions_euler(ctx, parsed_data)
            else:
                logger.error("MODE_UI no encontrado")
                return
        elif str(type(parsed_data)) ==  "<class 'mbientlab.metawear.cbindings.EulerAngles'>" :
            return self.data_handler_radians(ctx, parsed_data)
        logger.error(f"Problema con los tipos de datos... {type(parsed_data)}")

    
    def data_handler_quaternions(self, ctx, parsed_data):
        
        
        original_value = np.quaternion(parsed_data.w,
            parsed_data.x,
            parsed_data.y,
            parsed_data.z
            )
        value = original_value.normalized()
        if self._is_pending_calibration:
            self.QUATERNION_TO_CALIBRATE = quaternion_inverse(value)
            self._is_pending_calibration = False
            self._position = [0, 0, 0]
            
        if self.QUATERNION_TO_CALIBRATE:
            value = value * self.QUATERNION_TO_CALIBRATE
            
        
        self.samples+= 1
        #r, p, y = quaternion.as_euler_angles(value)
        logger.info(f"Q SENSOR: {original_value}\tFIXED: {value}") #\tEULER: {[p, r, y]}")
        self.data_callback([value.w,    value.x,    value.y,    value.z,])
    
    def data_handler_quaternions_euler(self, ctx, parsed_data):
        
        
        original_value = np.quaternion(parsed_data.w,
            parsed_data.x,
            parsed_data.y,
            parsed_data.z
            )
        value = original_value.normalized()
        if self._is_pending_calibration:
            self.QUATERNION_TO_CALIBRATE = quaternion_inverse(value)
            self._is_pending_calibration = False
            self._position = [0, 0, 0]
            
        if self.QUATERNION_TO_CALIBRATE:
            value = value * self.QUATERNION_TO_CALIBRATE
            
        
        self.samples+= 1
        r, p, y = quaternion.as_euler_angles(value)
        logger.info(f"Q SENSOR: {original_value}\tFIXED: {value}") #\tEULER: {[p, r, y]}")
        self.data_callback([r, p, y])
        
    def data_handler_radians(self, ctx, parsed_data):
        yaw_origin     = parsed_data.yaw
        pitch_origin   = parsed_data.pitch
        roll_origin    = parsed_data.roll
        heading_origin = parsed_data.heading
        logger.debug(f"ORIG;yaw;{round(yaw_origin, self._precision)};pitch;{round(pitch_origin, self._precision)};roll;{round(roll_origin, self._precision)};heading;{round(heading_origin,self._precision)};")
        if self._is_pending_calibration:
            logger.warning("{self.tag}Calibrando")
            self._is_pending_calibration = False
            self.YAW_TO_CALIBRATE = yaw_origin
            self.PITCH_TO_CALIBRATE = pitch_origin
            self.ROLL_TO_CALIBRATE = roll_origin
            self._position = [0, 0, 0]
             
        

        yaw   = MetawearCallback.calibrateDegree(yaw_origin, self.YAW_TO_CALIBRATE)
        pitch = MetawearCallback.calibrateDegree(pitch_origin, self.PITCH_TO_CALIBRATE)
        roll  = MetawearCallback.calibrateDegree(roll_origin, self.ROLL_TO_CALIBRATE)
        
        logger.debug(f"EUL_FIXED;yaw;{round(yaw, self._precision)};pitch;{round(pitch, self._precision)};roll;{round(roll, self._precision)};heading;{round(heading_origin,self.precision)};")
        
        yaw_r     = np.deg2rad(yaw)
        pitch_r   = np.deg2rad(pitch)
        roll_r    = np.deg2rad(roll)
        heading_r = np.deg2rad(heading_origin)
        logger.info(f"RAD;yaw;{round(yaw_r, self._precision)};pitch;{round(pitch_r, self._precision)};roll;{round(roll_r, self._precision)}];heading;{round(heading_r,self.precision)};")

        self.samples+= 1
        
        self.data_callback([pitch_r, roll_r, yaw_r])
        