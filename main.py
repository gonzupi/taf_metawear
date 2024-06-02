# usage: python3 main.py 
import logging
import sys

from log_setup import log_setup
from mbientlab.metawear.cbindings import *
from qt_project.qt_menu import start_menu
from settings import BITA_OSC_PATH_PRY

logger = logging.getLogger(__name__)
if sys.version_info[0] == 2:
    range = xrange



        

if __name__ == "__main__":
    windows = None
    log_setup("./log.log")
    logger.info("Iniciando sistema...")
    application, app = start_menu() 
    windows = application
    app.exec_()

    