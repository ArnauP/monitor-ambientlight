from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from .controllers.simulation_controller import SimulationController
from .controllers.main_controller import MainController

from .utils import utils


def main():
    app = QApplication([])
    main_ctrl = MainController()
    app.exec_()


if __name__ == "__main__":
    main()
