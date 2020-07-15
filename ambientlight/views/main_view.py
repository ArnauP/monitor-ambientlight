from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, QSpacerItem, QSizePolicy, QLineEdit
from PyQt5.QtCore import Qt

import mss


class MainView(QWidget):
    """
    This view will let the user choose the basic settings.
    """

    def __init__(self, ctrl):
        super(MainView, self).__init__()
        self.__ctrl = ctrl
        self.build_ui()
    
    def check_inputs(self):
        # TODO: Improve function as restyling task is done
        valid_inputs = True
        self.le_num_led_sides.setStyleSheet("border: 1px solid black;")
        self.le_num_led_top.setStyleSheet("border: 1px solid black;")
        if self.le_num_led_sides.text() == '' or not self.le_num_led_sides.text().isnumeric() or self.num_led_sides <= 0:
            self.le_num_led_sides.setStyleSheet("border: 1px solid red;")
            valid_inputs = False
        if self.le_num_led_top.text() == '' or not self.le_num_led_top.text().isnumeric() or self.num_led_top <= 0:
            self.le_num_led_top.setStyleSheet("border: 1px solid red;")
            valid_inputs = False
        return valid_inputs

    def simulate_clicked(self):
        if self.check_inputs():
            self.__ctrl.simulate_clicked()
    
    def ok_clicked(self):
        self.__ctrl.ok_clicked()

    def cancel_clicked(self):
        self.__ctrl.cancel_clicked()
    
    def build_ui(self):
        self.lyt_main = QVBoxLayout()
        lyt_monitor = QHBoxLayout()
        lyt_led_sides = QHBoxLayout()
        lyt_led_top = QHBoxLayout()
        lyt_action = QHBoxLayout()

        h_spacer = QSpacerItem(0, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.lbl_info = QLabel('Monitor')
        monitors = mss.mss().monitors
        self.cmb_monitor = QComboBox()
        for idx_monitor in range(len(monitors)):
            self.cmb_monitor.addItem('Monitor {} ({}x{})'.format(idx_monitor + 1, monitors[idx_monitor]['width'], monitors[idx_monitor]['height']))
        self.btn_simulate = QPushButton('Simulate')
        self.btn_simulate.clicked.connect(self.simulate_clicked)
        lyt_monitor.addWidget(self.lbl_info)
        lyt_monitor.addWidget(self.cmb_monitor)
        lyt_monitor.addWidget(self.btn_simulate)
        lyt_monitor.setAlignment(Qt.AlignCenter)

        self.lbl_num_led_sides = QLabel('Nº LED sides')
        self.le_num_led_sides = QLineEdit()
        lyt_led_sides.addWidget(self.lbl_num_led_sides)
        lyt_led_sides.addWidget(self.le_num_led_sides)

        self.lbl_num_led_top = QLabel('Nº LED top')
        self.le_num_led_top = QLineEdit()
        lyt_led_top.addWidget(self.lbl_num_led_top)
        lyt_led_top.addWidget(self.le_num_led_top)

        self.btn_ok = QPushButton('OK')
        self.btn_cancel = QPushButton('Cancel')
        self.btn_ok.clicked.connect(self.ok_clicked)
        self.btn_cancel.clicked.connect(self.cancel_clicked)
        lyt_action.addWidget(self.btn_ok)
        lyt_action.addItem(h_spacer)
        lyt_action.addWidget(self.btn_cancel)

        self.lyt_main.addLayout(lyt_monitor)
        self.lyt_main.addLayout(lyt_led_sides)
        self.lyt_main.addLayout(lyt_led_top)
        self.lyt_main.addLayout(lyt_action)
        self.setLayout(self.lyt_main)

        # self.setFixedSize(300, 250)
        self.setWindowTitle('Responsive ambientlight')
        self.show()

    @property
    def monitor_idx(self):
        return self.cmb_monitor.currentIndex()
    
    @property
    def num_led_sides(self):
        return int(self.le_num_led_sides.text())

    @property
    def num_led_top(self):
        return int(self.le_num_led_top.text())
