import logging
import signal
import time

from classes.metawear_callback_class import MetawearCallback
from mbientlab.metawear import POINTER, MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from services.SensorInterface import SensorInterface
from settings import MODE_SENSOR

logger = logging.getLogger(__name__)

def handle_sigabrt(signum, frame):
        print("SIGABRT signal received")
        
class MetaWearService(SensorInterface):
    def __init__(self, device_mac, data_callback, config=None):
        self.device_mac = device_mac
        self.data_callback = data_callback
        self.device = None
        signal.signal(signal.SIGABRT, handle_sigabrt)

    
    def connect(self):
        tag = "[metawear_service] >> connect_device >> "
        connected = False
        devices = []
        logger.info(f"Conectando a dispositivo - {self.device_mac}")
        while not connected:
            try:
                #d = MetaWear(sys.argv[i + 1])
                d = MetaWear(self.device_mac)
                d.connect()
                
                logger.info(f"{tag}Connected to {d.address} over {('USB' if d.usb.is_connected else 'BLE')}")
                devices.append(MetawearCallback(d, self.data_callback))
                connected = True
            except:
                TIME_TO_RETRY = 0.5
                logger.exception(f"{tag}Error en la conexión, reintentando en {TIME_TO_RETRY}s...")
                time.sleep(TIME_TO_RETRY)
        logger.info(f"{tag} CONNECT - OK")
        for device in devices:
            self.configure_device(device)
        return devices

    def configure_device(self, device, with_ble_setup = True):
        tag = "[metawear_service] >> configure_device >> "
        self.data_type = SensorFusionData.EULER_ANGLE if MODE_SENSOR != "QUATERNIONS" else SensorFusionData.QUATERNION

        logger.info(f"{tag}Configuring device")
        # setup ble
        if(with_ble_setup):
            libmetawear.mbl_mw_settings_set_connection_parameters(device.device.board, 7.5, 7.5, 0, 6000)
            time.sleep(1.5)
        # setup quaternion
        libmetawear.mbl_mw_sensor_fusion_set_mode(device.device.board, SensorFusionMode.NDOF);
        libmetawear.mbl_mw_sensor_fusion_set_acc_range(device.device.board, SensorFusionAccRange._8G)
        libmetawear.mbl_mw_sensor_fusion_set_gyro_range(device.device.board, SensorFusionGyroRange._2000DPS)
        libmetawear.mbl_mw_sensor_fusion_write_config(device.device.board)
        # get quat signal and subscribe
        signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(device.device.board, self.data_type)
        libmetawear.mbl_mw_datasignal_subscribe(signal, None, device.callback)
        # start acc, gyro, mag
        libmetawear.mbl_mw_sensor_fusion_enable_data(device.device.board, self.data_type)
        libmetawear.mbl_mw_sensor_fusion_start(device.device.board)
        self.device = device
        logger.info(f"{tag} CONFIGURATION - OK")

    def disconnect(self):
        tag = "[metawear_service] >> disconnect >> "
        logger.info(f"{tag}Disconnecting device")
        # stop
        libmetawear.mbl_mw_sensor_fusion_stop(self.device.device.board);
        # unsubscribe to signal
        signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(self.device.device.board, self.data_type);
        libmetawear.mbl_mw_datasignal_unsubscribe(signal)
        # disconnect
        libmetawear.mbl_mw_debug_disconnect(self.device.device.board)
        logger.info(f"{tag} DISCONNECT - OK")


    def stop(self):
        tag = "[metawear_service] >> stop >> "
        logger.info(f"{tag} Stopping device")
        libmetawear.mbl_mw_sensor_fusion_stop(self.device.device.board);
        logger.info(f"{tag} STOP - OK")

    def restart(self):
        tag = "[metawear_service] >> Restarting >> "
        logger.info(f"{tag} Stopping device")
        self.stop(self.device)
        TIME_TO_SLEEP=5
        logger.info("{tag}Sleepping {TIME_TO_SLEEP}s")
        time.sleep(TIME_TO_SLEEP)
        logger.info(f"{tag} Starting device again")
        self.configure_device(self.device, with_ble_setup=False)
        logger.info(f"{tag} RESTART - OK")

        