from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

# LED simulated sizes
LED_WIDTH = 50
LED_HEIGHT = 50

# Size identifiers
LEFT_SIDE = 1
TOP_SIDE = 2
RIGHT_SIDE = 3


class SimulationView(QWidget):
    """
        This view represents the LED strips
    """

    def __init__(self, ctrl, rows, columns):
        super(SimulationView, self).__init__()
        self.__ctrl = ctrl
        self.rows = rows
        self.columns = columns
        self.left_led_strip = []
        self.top_led_strip = []
        self.right_led_strip = []
        self.build_ui()
    
    def generate_random_color(self):
        r, g, b = list(np.random.choice(range(256), size=3))
        return r, g, b
    
    def get_strip_list(self, strip_id):
        if strip_id == LEFT_SIDE:
            return self.left_led_strip
        if strip_id == TOP_SIDE:
            return self.top_led_strip
        if strip_id == RIGHT_SIDE:
            return self.right_led_strip

    def add_led_to_strip(self, led_strip, layout):
        lbl_led = QLabel('', self)
        lbl_led.setFixedSize(LED_WIDTH, LED_HEIGHT)
        # r, g, b = self.generate_random_color()
        r, g, b = 0, 0, 0
        lbl_led.setStyleSheet("background-color: rgb({}, {}, {})".format(r, g, b))
        lbl_led.setVisible(True)
        led_strip.append(lbl_led)
        layout.addWidget(lbl_led)
    
    def fill_led_strip(self, counter, led_strip, layout, reverse=False):
        for row in range(counter):
            self.add_led_to_strip(led_strip, layout)
        if reverse:
            led_strip = led_strip.reverse()
        
    def change_colors_strip(self, strip_side, color_list):
        strip = self.get_strip_list(strip_side)
        for idx_led in range(len(strip)):
            r, g, b = color_list[idx_led]
            strip[idx_led].setStyleSheet("background-color: rgb({}, {}, {})".format(r, g, b))

    def parse_colors(self, colors):
        idx_initial = 0
        idx_final = self.rows
        self.change_colors_strip(LEFT_SIDE, colors[idx_initial:idx_final])
        idx_initial = idx_final
        idx_final += self.columns
        self.change_colors_strip(TOP_SIDE, colors[idx_initial:idx_final])
        idx_initial = idx_final
        idx_final += self.rows
        self.change_colors_strip(RIGHT_SIDE, colors[idx_initial:idx_final])
    
    def closeEvent(self, event):
        self.__ctrl.stop_analyser()

    def build_ui(self):
        
        self.lyt_main = QHBoxLayout()
        self.lyt_left = QVBoxLayout()
        self.lyt_middle = QVBoxLayout()
        self.lyt_top = QHBoxLayout()
        self.lyt_right = QVBoxLayout()

        self.fill_led_strip(self.rows, self.left_led_strip, self.lyt_left, reverse=True)
        self.fill_led_strip(self.columns, self.top_led_strip, self.lyt_top)
        self.fill_led_strip(self.rows, self.right_led_strip, self.lyt_right)

        self.lyt_middle.addLayout(self.lyt_top)
        v_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.lyt_middle.addItem(v_spacer)

        self.lyt_main.addLayout(self.lyt_left)
        self.lyt_main.addLayout(self.lyt_middle)
        self.lyt_main.addLayout(self.lyt_right)
        self.setLayout(self.lyt_main)

        self.setWindowTitle('LED Stripes Simulation')
        self.show()
