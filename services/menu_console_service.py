import logging
import keyboard
import services.metawear_service as metawear_service
from settings import BITA_OSC_PATH_POS, OSC_IS_ENABLED, POS_STEP
logger = logging.getLogger(__name__)

class ExitException(Exception):
    pass
def exit_function(devices, osc_client, available_keys):
    raise ExitException()


def calibration_function(devices, osc_client, available_keys):
    #logger.info("[calibration_function] Calibrating")
    for device in devices:
        device.is_pending_calibration= True
    return devices, osc_client, available_keys

def restart_function(devices, osc_client, available_keys):
    #logger.info("[restart_function] Calibrating")
    for device in devices:
        metawear_service.restart(device)
    return devices, osc_client, available_keys

def up_function(devices, osc_client, available_keys):
    #logger.info("[up_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_x = pos_y + POS_STEP

        if OSC_IS_ENABLED:
            osc_client.send_message(BITA_OSC_PATH_POS, [pos_x, pos_y, pos_z])
        device.position=[pos_x, pos_y, pos_z]
        logger.info(f"Moving - From {position} -> { [pos_x, pos_y, pos_z]}")
    return devices, osc_client, available_keys

def down_function(devices, osc_client, available_keys):
    #logger.info("[down_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_x = pos_y - POS_STEP
        if OSC_IS_ENABLED:
            osc_client.send_message(BITA_OSC_PATH_POS, [pos_x, pos_y, pos_z])
        device.position=[pos_x, pos_y, pos_z]
        logger.info(f"Moving - From {position} -> { [pos_x, pos_y, pos_z]}")
    return devices, osc_client, available_keys

def right_function(devices, osc_client, available_keys):
    #logger.info("[right_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_x = pos_x + POS_STEP
        if OSC_IS_ENABLED:
            osc_client.send_message(BITA_OSC_PATH_POS, [pos_x, pos_y, pos_z])
        device.position=[pos_x, pos_y, pos_z]
        logger.info(f"Moving - From {position} -> { [pos_x, pos_y, pos_z]}")
    return devices, osc_client, available_keys

def left_function(devices, osc_client, available_keys):
    #logger.info("[left_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_x = pos_x - POS_STEP
        if OSC_IS_ENABLED:
            osc_client.send_message(BITA_OSC_PATH_POS, [pos_x, pos_y, pos_z])
        device.position=[pos_x, pos_y, pos_z]
        logger.info(f"Moving - From {position} -> { [pos_x, pos_y, pos_z]}")
    return devices, osc_client, available_keys

def in_function(devices, osc_client, available_keys):
    #logger.info("[in_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_x = pos_z + POS_STEP
        if OSC_IS_ENABLED:
            osc_client.send_message(BITA_OSC_PATH_POS, [pos_x, pos_y, pos_z])
        device.position=[pos_x, pos_y, pos_z]
        logger.info(f"Moving - From {position} -> { [pos_x, pos_y, pos_z]}")
    return devices, osc_client, available_keys

def out_function(devices, osc_client, available_keys):
    #logger.info("[out_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_x = pos_z - POS_STEP
        if OSC_IS_ENABLED:
            osc_client.send_message(BITA_OSC_PATH_POS, [pos_x, pos_y, pos_z])
        device.position=[pos_x, pos_y, pos_z]
        logger.info(f"Moving - From {position} -> { [pos_x, pos_y, pos_z]}")
    return devices, osc_client, available_keys

def help_function(devices, osc_client, available_keys):
    logger.info("Tiene disponibles las siguientes funciones mediante control por teclado presionando las siguientes teclas:")
    for key in available_keys:
        logger.info(f"  -  Tecla '{key['key']}  - {key['description']}")
    logger.info("")
    return devices, osc_client, available_keys

def menu(devices, osc_client):
    available_keys = [
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
            "key" : "s",
            "description" : f"Move down one step of {POS_STEP}",
            "function":down_function

        },
        { 
            "key" : "w",
            "description" : f"Move up one step of {POS_STEP}",
            "function":up_function

        },
        { 
            "key" : "d",
            "description" : f"Move right one step of {POS_STEP}",
            "function":right_function

        },
        { 
            "key" : "a",
            "description" : f"Move left one step of {POS_STEP}",
            "function":left_function

        },
        { 
            "key" : "i",
            "description" : f"Move in one step of {POS_STEP}",
            "function":in_function
        },{
            "key" : "o",
            "description" : f"Move out one step of {POS_STEP}",
            "function":out_function

        },
        { 
            "key" : "h",
            "description" : f"Help - show description of keys",
            "function":help_function

        },
    ]
    logger.info("Iniciando control por teclado. ")
    help_function(devices, osc_client, available_keys)
    keys = [k["key"] for k in available_keys]
    try:
        while True:
            #pressed_key = keyboard.read_key()
            pressed_key=input("Introduce una letra y presiona intro: ")
            if pressed_key in keys:
                logger.info(f"Evento de teclado - Presionada la tecla {pressed_key}")
                key_obj_list = [k for k in available_keys if k["key"] == pressed_key]
                if len(key_obj_list) > 0:
                    key_obj = key_obj_list[0]
                    logger.info(f"key_obj {key_obj}")
                    logger.info(f"Evento de teclado - Ejecutando : {key_obj['description']}")
                    devices, osc_client, available_keys = key_obj["function"](devices, osc_client, available_keys)
   
    except ExitException as e:
        logger.warning("Saliendo del control por teclado. Cerrando stream de comunicación con los sensores, espere unos segundos por favor...")
    except Exception as e:
        logger.exception("Ha ocurrido un problema")