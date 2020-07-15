from PyQt5.QtWidgets import QApplication

from .controllers.simulation_controller import SimulationController
from .controllers.main_controller import MainController


def main():
    app = QApplication([])
    # sim_ctrl = SimulationController(15, 25, 60)
    main_ctrl = MainController()
    app.exec_()


if __name__ == "__main__":
    main()
