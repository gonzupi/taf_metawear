# -*- coding: utf-8 -*-
# Author : Gonzalo Bueno Santana
#################################################
# LOG_SETUP
#################################################
import logging  # , coloredlogs
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
#from settings import LOGS_FILE_PATH
# Si se desea se pueden importar estas configuraciones desde el archivo settings.py
# from settings import log_level, log_fileCount, log_fileSize

# En función del nivel del log se verán unos mensajes u otros
# Si se define aquí sobreescribe al de settings
# log_level = logging.WARNING
#log_level = logging.INFO
log_level = logging.DEBUG

LOGS_FILE_PATH = "./LOG"
log_fileSize = 25  # Tamaño de cada archivo de log en mb
log_fileCount = 10  # Número de archivos de log que se van a guardar (sistema rotativo)
logger = logging.getLogger(__name__)


grey = "\x1b[38m"
cyan = "\x1b[36m"
purple = "\x1b[35m"
yellow = "\x1b[33m"
blue = "\x1b[34m"
lightblue = "\033[94m"
green = "\x1b[32m"
bold_yellow = "\x1b[33m"
bold_blue = "\x1b[34m"
bold_green = "\x1b[32m"
red = "\x1b[31m"
bold_red = "\x1b[31m"
reset = "\x1b[0m"


def log_setup(file_name: str = "server.log"):
    """Configuro el log del sistema, me crea una carpeta 
    de logs que guarda varios archivos de un tamaño máximo 
    cada uno en un sistema de logs rotativos
    """
    
    LOGS_PATH = Path(LOGS_FILE_PATH)
    os.makedirs(LOGS_PATH, exist_ok=True)
    fileSize = log_fileSize  # Mb per file
    fileCount = log_fileCount  # Number of log files
    
    logger.setLevel(logging.INFO) 
       
    # loggingLevel = logging.DEBUG # Lo dejo en settings.
    fileHandler = TimedRotatingFileHandler(
        LOGS_PATH / Path(file_name), when="MIDNIGHT", interval=1, backupCount=40
    )
    """
    fileHandler = RotatingFileHandler(
        filename  = LOGS_PATH / Path('log'),
        mode = 'a',
        maxBytes = fileSize * 1024 * 1024,
        backupCount = fileCount,
        encoding = None,
        )
    """
    stdoutHandler = logging.StreamHandler()
    fileFormat = logging.Formatter(
        "%(asctime)s - %(name)s - [%(threadName)-12.12s] [%(levelname) -5.5s] - %(message)s - %(filename)s"
    )
    # stdoutHandler.setFormatter(format)
    # fileHandler.setFormatter(fileFormat)
    fileHandler.setFormatter(CustomFormatter())
    stdoutHandler.setFormatter(CustomFormatter())
    # coloredlogs.install(level='DEBUG', logger=stdoutHandler)
    # coloredlogs.install(level='DEBUG')

    stdoutHandler.setLevel(log_level)
    fileHandler.setLevel(log_level)

    logging.basicConfig(
        level=log_level,
        datefmt="%d-%m-%y %H:%M:%S",
        handlers=[fileHandler, stdoutHandler],
    )
    
    
   
    


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    header = "%(asctime)s "
    level = "%(levelname)s   [%(name)s] "
    lastPart = "%(message)s (%(filename)s - %(lineno)d)"
    FORMATS = {
        logging.DEBUG: blue + header + grey + level + reset + lastPart,
        logging.INFO: blue + header + green + level + reset + lastPart,
        logging.WARNING: blue + header + yellow + level + lastPart + reset,
        logging.ERROR: blue + header + red + level + lastPart + reset,
        logging.CRITICAL: blue + header + bold_red + level + lastPart + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

