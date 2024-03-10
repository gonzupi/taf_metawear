from pythonosc import udp_client
import logging
logger = logging.getLogger(__name__)


def connect(ip, port):
    logger.info(f"[OSC] connect >> Tratando de conectar por OSC a {ip}:{port}...")
    client =  udp_client.SimpleUDPClient(ip, port)
    logger.info("[OSC] connect >> OK")
    return client
    
def init(osc_client, path_pos, default_coordinates):
    logger.info(f"[OSC] connect >> Inicializando OSC")
    osc_client.send_message(path_pos,default_coordinates )
    logger.info("[OSC] init >> OK")
