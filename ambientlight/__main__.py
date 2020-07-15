from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from .controllers.simulation_controller import SimulationController
from .controllers.main_controller import MainController

from .utils import utils


def main():
    app = QApplication([])
    app.setWindowIcon(QIcon(utils.get_path('ambientlight/resources/icons/app_icon.svg')))
    utils.load_style_sheet(utils.get_path('ambientlight/resources/css/style.css'), app)
    main_ctrl = MainController()
    app.exec_()


if __name__ == "__main__":
    main()
