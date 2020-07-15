from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QIcon, QFont, QCursor

from time import sleep
import asyncio
import np

from ..controllers.simulation_controller import SimulationController
from ..views.main_view import MainView


class MainController(QObject):
    """
    Provides control for all of the main actions of the software
    """
    def __init__(self):
        super(MainController, self).__init__()
        self.__view = MainView(self)

    def simulate_clicked(self):
        self.simulation_ctrl = SimulationController(
            self.__view.monitor_idx, 
            self.__view.num_led_sides, 
            self.__view.num_led_top, 
            fade_speed=60
            )

    def ok_clicked(self):
        print('Monitor index {}'.format(self.__view.monitor_idx))
    
    def cancel_clicked(self):
        self.__view.close()
