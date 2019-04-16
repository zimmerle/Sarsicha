
from src.singleton import Singleton


class Logger(metaclass=Singleton):
    DEFAULT_LEVEL = 1000

    def __init__(self):
        self._currentLevel = self.DEFAULT_LEVEL
        pass


    def log(self, lvl, msg):
        if lvl < self._currentLevel:
            print("" + msg)
        

def log(lvl, msg):
    return Logger().log(lvl, msg)