# usage: python3 main.py 
#from __future__ import print_function
import time
from mbientlab.metawear import MetaWear, libmetawear, parse_value, POINTER
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event
import numpy as np
import platform
import sys
import logging
from services.menu_service import menu
from settings import ASK_FOR_IP, BITA_OSC_DEFAULT_COORDINATES, BITA_OSC_PATH_POS, BITA_OSC_PATH_PRY, BITA_PORT, DEVICE_MAC, BITA_IP
from log_setup import log_setup
import services.osc_service as osc_service
import services.metawear_service as metawear_service
import os
import re
logger = logging.getLogger(__name__)
if sys.version_info[0] == 2:
    range = xrange

def data_callback(data):
    tag = "[data_callback]"
    logger.info(f"{tag}Enviando datos por osc {data}")
    osc_client.send_message(f"{BITA_OSC_PATH_PRY}", data)


def get_ip():
   
    devices = []
    for device in os.popen('arp -a'): devices.append(device)
    logger.info("Selecciona una de las IPs Locales:")
    for index, device in enumerate(devices):
        logger.info(f"{index} - {device}")
    ip_input = input("Selecciona un número o introduce la IP manualmente: \t")
    try:
        data = devices[int(ip_input)]
        patron_ip = r"\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)"

        ip = re.search(patron_ip, data).group(1)
        logger.info(f"IP seleccionada {ip}")
        return ip
    except Exception as e:
        return ip_input
        

if __name__ == "__main__":
    log_setup("./log.log")
    logger.info("Iniciando sistema...")
    
    logger.info("Iniciando OSC")
    if ASK_FOR_IP:
        logger.info("Analizando red, buscando dispositivos disponibles...")
        osc_ip = get_ip()
    else:
        osc_ip = BITA_IP
    logger.info(f"[OSC] - Tratando de conectar a la ip : {osc_ip} - y al puerto {BITA_PORT}")
    osc_client = osc_service.connect(osc_ip, BITA_PORT)
    osc_service.init(osc_client, BITA_OSC_PATH_POS, BITA_OSC_DEFAULT_COORDINATES)
    logger.info("OK")

    logger.info("Conectando con dispositivo MetaWear")
    devices = metawear_service.connect_device(DEVICE_MAC, data_callback)
    logger.info("OK")

    logger.info(f"Configurando {len(devices)} dispositivos")
    for device in devices:
        metawear_service.configure_device(device)
    logger.info("OK")


    menu()
    
    logger.warning("Desconectando dispositivos")
    for device in devices:
        metawear_service.disconnect(device)
    logger.info("OK")
    
    logger.info("[RESUMEN] - Total Samples Received")
    for device in devices:
        logger.info("%s -> %d" % (device.device.address, device.samples))