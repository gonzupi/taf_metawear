from abc import ABC, abstractmethod


class SensorInterface(ABC):

    @abstractmethod
    def __init__(self, device_mac, data_callback, config=None):
        pass

    @abstractmethod
    def connect(self):
        pass
    @abstractmethod
    def disconnect(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass
    
    @abstractmethod
    def restart(self):
        pass