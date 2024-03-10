import logging
import keyboard
import services.metawear_service as metawear_service
from settings import BITA_OSC_PATH_POS, POS_STEP
logger = logging.getLogger(__name__)

class ExitException(Exception):
    pass
def exit_function(devices, osc_client, available_keys):
    raise ExitException()


def calibration_function(devices, osc_client, available_keys):
    #logger.info("[calibration_function] Calibrating")
    for device in devices:
        device.is_pending_calibration= True

def restart_function(devices, osc_client, available_keys):
    #logger.info("[restart_function] Calibrating")
    for device in devices:
        metawear_service.restart(device)

def up_function(devices, osc_client, available_keys):
    #logger.info("[up_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_x = pos_y + POS_STEP

        osc_client.send_message(BITA_OSC_PATH_POS, [pos_x, pos_y, pos_z])
        device.position =  [pos_x, pos_y, pos_z]
        

def down_function(devices, osc_client, available_keys):
    #logger.info("[down_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_x = pos_y - POS_STEP

        osc_client.send_message(BITA_OSC_PATH_POS, [pos_x, pos_y, pos_z])
        device.position =  [pos_x, pos_y, pos_z]
        
def right_function(devices, osc_client, available_keys):
    #logger.info("[right_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_x = pos_x + POS_STEP

        osc_client.send_message(BITA_OSC_PATH_POS, [pos_x, pos_y, pos_z])
        device.position =  [pos_x, pos_y, pos_z]
        
def left_function(devices, osc_client, available_keys):
    #logger.info("[left_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_x = pos_x - POS_STEP

        osc_client.send_message(BITA_OSC_PATH_POS, [pos_x, pos_y, pos_z])
        device.position =  [pos_x, pos_y, pos_z]
        
def in_function(devices, osc_client, available_keys):
    #logger.info("[in_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_x = pos_z + POS_STEP

        osc_client.send_message(BITA_OSC_PATH_POS, [pos_x, pos_y, pos_z])
        device.position =  [pos_x, pos_y, pos_z]
        
def out_function(devices, osc_client, available_keys):
    #logger.info("[out_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_x = pos_z - POS_STEP

        osc_client.send_message(BITA_OSC_PATH_POS, [pos_x, pos_y, pos_z])
        device.position =  [pos_x, pos_y, pos_z]
        
def help_function(devices, osc_client, available_keys):
    logger.info("Tiene disponibles las siguientes funciones mediante control por teclado presionando las siguientes teclas:")
    for key in available_keys:
        logger.info(f"  -  Tecla '{key['key']}  - {key['description']}")
    logger.info("")
    
def menu():
    allowed_keys = [
        {
            "key":"e",
            "description":"Exit key",
            "function":exit_function
        },
        {
            "key":"c",
            "description":"Calibration",
            "function":calibration_function
        },
        {
            "key":"r",
            "description":"Restart devices",
            "function":restart_function
        },
        
        { 
            "key" : "down",
            "Description" : f"Move down one step of {POS_STEP}",
            "function":down_function

        },
        { 
            "key" : "up",
            "Description" : f"Move up one step of {POS_STEP}",
            "function":up_function

        },
        { 
            "key" : "right",
            "Description" : f"Move right one step of {POS_STEP}",
            "function":right_function

        },
        { 
            "key" : "left",
            "Description" : f"Move left one step of {POS_STEP}",
            "function":left_function

        },
        { 
            "key" : "i",
            "Description" : f"Move in one step of {POS_STEP}",
            "function":in_function
        },{
            "key" : "o",
            "Description" : f"Move out one step of {POS_STEP}",
            "function":out_function

        },
        { 
            "key" : "h",
            "Description" : f"Help - show description of keys",
            "function":help_function

        },
    ]
    logger.info("Iniciando control por teclado. ")
    help_function()
    keys = [k["key"] for k in keys]
    try:
        while True:
            pressed_key = keyboard.read_key()
            if pressed_key in keys:
                key_obj = [k for k in allowed_keys if k["key"] == pressed_key]
                if len(key_obj) > 0:
                    logger.info(f"Evento de teclado - {key_obj['description']}")
                    key_obj["function"]
    except Exception as e:
        logger.warning("Saliendo del control por teclado. Cerrando stream de comunicación con los sensores, espere unos segundos por favor...")