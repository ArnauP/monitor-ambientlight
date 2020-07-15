from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

import mss


class MainView(QWidget):
    """
        This view will let the user select the monitor that will be used to track the colors.
    """

    def __init__(self, ctrl):
        super(MainView, self).__init__()
        self.__ctrl = ctrl
        self.build_ui()
    
    def build_ui(self):
        self.lyt_main = QVBoxLayout()
        lyt_info = QHBoxLayout()
        lyt_selector = QHBoxLayout()
        lyt_action = QHBoxLayout()

        h_spacer = QSpacerItem(0, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.lbl_info = QLabel('Select the target monitor')
        lyt_info.addItem(h_spacer)
        lyt_info.addWidget(self.lbl_info)
        lyt_info.addItem(h_spacer)

        monitors = mss.mss().monitors
        self.cmb_monitor = QComboBox()
        for idx_monitor in range(len(monitors)):
            self.cmb_monitor.addItem('Monitor {} ({}x{})'.format(idx_monitor + 1, monitors[idx_monitor]['width'], monitors[idx_monitor]['height']))
        self.btn_simulate = QPushButton('Simulate')
        self.btn_simulate.clicked.connect(self.__ctrl.simulate_clicked)
        lyt_selector.addItem(h_spacer)
        lyt_selector.addWidget(self.cmb_monitor)
        lyt_selector.addWidget(self.btn_simulate)
        lyt_selector.addItem(h_spacer)

        self.btn_ok = QPushButton('OK')
        self.btn_cancel = QPushButton('Cancel')
        self.btn_ok.clicked.connect(self.__ctrl.ok_clicked)
        self.btn_cancel.clicked.connect(self.__ctrl.cancel_clicked)
        lyt_action.addWidget(self.btn_ok)
        lyt_action.addItem(h_spacer)
        lyt_action.addWidget(self.btn_cancel)

        self.lyt_main.addLayout(lyt_info)
        self.lyt_main.addLayout(lyt_selector)
        self.lyt_main.addLayout(lyt_action)
        self.setLayout(self.lyt_main)

        self.setFixedSize(300, 150)
        self.setWindowTitle('Responsive ambientlight')
        self.show()

    @property
    def monitor_idx(self):
        return self.cmb_monitor.currentIndex()