# usage: python3 main.py 
import logging
import os
import signal
import sys
import time

from log_setup import log_setup
from mbientlab.metawear.cbindings import *
from qt_project.qt_menu import start_menu
from services.metawear_service import MetaWearService
from settings import OSC_RECIVER_PATH_PRY

logger = logging.getLogger(__name__)
if sys.version_info[0] == 2:
    range = xrange

def handler( signum, frame ):
  print("Signal handler caught", signum, "@", time.ctime())
  if signum == 2:
    raise "Caught Signal 2 - Exiting"

#
# Windows Supported Values
#
#signal.signal( signal.SIGABRT, handler )
#signal.signal( signal.SIGFPE, handler )
#signal.signal( signal.SIGILL, handler )
#signal.signal( signal.SIGINT, handler )
#signal.signal( signal.SIGSEGV, handler )
#signal.signal( signal.SIGTERM, handler )

#
# UNIX Supported Values (YMMV)
#
signal.signal( signal.SIGABRT, handler )
signal.signal( signal.SIGALRM, handler )
signal.signal( signal.SIGBUS, handler )
signal.signal( signal.SIGCHLD, handler )
signal.signal( signal.SIGCLD, handler )
signal.signal( signal.SIGCONT, handler )
signal.signal( signal.SIGFPE, handler )
signal.signal( signal.SIGHUP, handler )
signal.signal( signal.SIGILL, handler )
signal.signal( signal.SIGINT, handler )
signal.signal( signal.SIGIO, handler )
signal.signal( signal.SIGIOT, handler )
#signal.signal( signal.SIGKILL, handler )
signal.signal( signal.SIGPIPE, handler )
signal.signal( signal.SIGPOLL, handler )
signal.signal( signal.SIGPROF, handler )
signal.signal( signal.SIGPWR, handler )
signal.signal( signal.SIGQUIT, handler )
signal.signal( signal.SIGRTMAX, handler )
signal.signal( signal.SIGRTMIN, handler )
signal.signal( signal.SIGSEGV, handler )
#signal.signal( signal.SIGSTOP, handler )
signal.signal( signal.SIGSYS, handler )
signal.signal( signal.SIGTERM, handler )
signal.signal( signal.SIGTRAP, handler )
signal.signal( signal.SIGTSTP, handler )
signal.signal( signal.SIGTTIN, handler )
signal.signal( signal.SIGTTOU, handler )
signal.signal( signal.SIGURG, handler )
signal.signal( signal.SIGUSR1, handler )
signal.signal( signal.SIGUSR2, handler )
signal.signal( signal.SIGVTALRM, handler )
signal.signal( signal.SIGWINCH, handler )
signal.signal( signal.SIGXCPU, handler )
signal.signal( signal.SIGXFSZ, handler )
#signal.signal( signal.SIG_DFL, handler )
signal.signal( signal.SIG_IGN, handler )


        

if __name__ == "__main__":
    windows = None
    log_setup("log.log")
    logger.info("Iniciando sistema...")
    application, app = start_menu(MetaWearService) 
    windows = application
    try:
        app.exec_()
    except Exception as e:
        logger.exception("Saliendo de la aplicación")

    