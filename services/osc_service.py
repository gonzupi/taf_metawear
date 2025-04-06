import logging

from pythonosc import udp_client

from settings import OSC_RECIVER_PATH_POS, POS_STEP

logger = logging.getLogger(__name__)


def connect(ip, port):
    logger.info(f"[OSC] connect >> Tratando de conectar por OSC a {ip}:{port}...")
    client =  udp_client.SimpleUDPClient(ip, int(port))

    logger.info("[OSC] connect >> OK")
    return client
    
def init(osc_client, path_pos, default_coordinates=[0, 0, 0]):
    try:
        logger.info(f"[OSC] connect >> Inicializando OSC - path_pos:{path_pos}\tcoords:{default_coordinates}")
        osc_client.send_message(path_pos,default_coordinates )
        logger.info("[OSC] init >> OK")
        return True
    except Exception as e:
        logger.exception("No se ha podido inicializar la comunicación por OSC")
        return False



def up_function(devices, osc_client):
    #logger.info("[up_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_y = pos_y + POS_STEP

        if osc_client:
            osc_client.send_message(OSC_RECIVER_PATH_POS, [pos_x, pos_y, pos_z])
        device.position=[pos_x, pos_y, pos_z]
        logger.info(f"Moving - From {position} -> { [pos_x, pos_y, pos_z]}")
    return devices, osc_client

def down_function(devices, osc_client):
    #logger.info("[down_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_y = pos_y - POS_STEP
        if osc_client:
            osc_client.send_message(OSC_RECIVER_PATH_POS, [pos_x, pos_y, pos_z])
        device.position=[pos_x, pos_y, pos_z]
        logger.info(f"Moving - From {position} -> { [pos_x, pos_y, pos_z]}")
    return devices, osc_client

def right_function(devices, osc_client):
    #logger.info("[right_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_x = pos_x + POS_STEP
        if osc_client:
            osc_client.send_message(OSC_RECIVER_PATH_POS, [pos_x, pos_y, pos_z])
        device.position=[pos_x, pos_y, pos_z]
        logger.info(f"Moving - From {position} -> { [pos_x, pos_y, pos_z]}")
    return devices, osc_client

def left_function(devices, osc_client):
    #logger.info("[left_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_x = pos_x - POS_STEP
        if osc_client:
            osc_client.send_message(OSC_RECIVER_PATH_POS, [pos_x, pos_y, pos_z])
        device.position=[pos_x, pos_y, pos_z]
        logger.info(f"Moving - From {position} -> { [pos_x, pos_y, pos_z]}")
    return devices, osc_client

def in_function(devices, osc_client):
    #logger.info("[in_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_z = pos_z + POS_STEP
        if osc_client:
            osc_client.send_message(OSC_RECIVER_PATH_POS, [pos_x, pos_y, pos_z])
        device.position=[pos_x, pos_y, pos_z]
        logger.info(f"Moving - From {position} -> { [pos_x, pos_y, pos_z]}")
    return devices, osc_client

def out_function(devices, osc_client):
    #logger.info("[out_function] moving")
    for device in devices:
        position = device.position
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        pos_z = pos_z - POS_STEP
        if osc_client:
            osc_client.send_message(OSC_RECIVER_PATH_POS, [pos_x, pos_y, pos_z])
        device.position=[pos_x, pos_y, pos_z]
        logger.info(f"Moving - From {position} -> { [pos_x, pos_y, pos_z]}")
    return devices, osc_client
