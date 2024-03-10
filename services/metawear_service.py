import time
from classes.metawear_callback_class import MetawearCallback
from mbientlab.metawear import MetaWear, libmetawear, parse_value, POINTER
from mbientlab.metawear.cbindings import *
import logging
logger = logging.getLogger(__name__)

def connect_device(device_mac, data_callback):
    tag = "[metawear_service] >> connect_device >> "
    connected = False
    devices = []
    while not connected:
        try:
            #d = MetaWear(sys.argv[i + 1])
            d = MetaWear(device_mac)
            d.connect()
            
            logger.info(f"{tag}Connected to {d.address} over {('USB' if d.usb.is_connected else 'BLE')}")
            devices.append(MetawearCallback(d, data_callback))
            connected = True
        except:
            TIME_TO_RETRY = 0.5
            logger.exception(f"{tag}Error en la conexión, reintentando en {TIME_TO_RETRY}s...")
            time.sleep(TIME_TO_RETRY)
    return devices

def configure_device(device, with_ble_setup = True):
    tag = "[metawear_service] >> configure_device >> "
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
    signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(device.device.board, SensorFusionData.EULER_ANGLE)
    libmetawear.mbl_mw_datasignal_subscribe(signal, None, device.callback)
    # start acc, gyro, mag
    libmetawear.mbl_mw_sensor_fusion_enable_data(device.device.board, SensorFusionData.EULER_ANGLE)
    libmetawear.mbl_mw_sensor_fusion_start(device.device.board)
    

def disconnect(device):
    tag = "[metawear_service] >> disconnect >> "
    logger.info(f"{tag}Disconnecting device")
    # stop
    libmetawear.mbl_mw_sensor_fusion_stop(device.device.board);
    # unsubscribe to signal
    signal = libmetawear.mbl_mw_sensor_fusion_get_data_signal(device.device.board, SensorFusionData.EULER_ANGLE);
    libmetawear.mbl_mw_datasignal_unsubscribe(signal)
    # disconnect
    libmetawear.mbl_mw_debug_disconnect(device.device.board)
    

def stop(device):
    tag = "[metawear_service] >> stop >> "
    logger.info(f"{tag} Stopping device")
    libmetawear.mbl_mw_sensor_fusion_stop(device.device.board);

def restart(device):
    tag = "[metawear_service] >> Restarting >> "
    logger.info(f"{tag} Stopping device")
    stop(device)
    TIME_TO_SLEEP=5
    logger.info("{tag}Sleepping {TIME_TO_SLEEP}s")
    time.sleep(TIME_TO_SLEEP)
    logger.info(f"{tag} Starting device again")
    configure_device(device, with_ble_setup=False)
    
    