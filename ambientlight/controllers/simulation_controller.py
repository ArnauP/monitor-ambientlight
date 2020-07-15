from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QIcon, QFont, QCursor

import serial, math, time, mss, numpy, cv2
from PIL import Image, ImageStat
from colorsys import rgb_to_hls, hls_to_rgb

from time import sleep
import asyncio
import np

from ..views.simulation_view import SimulationView

# CONSTANTS
REDUCTION_FACTOR = 6
COLOR_REGION = 150
ACKNOWLEDGE = 6


class UpdateLEDStripThread(QThread):
    sig_update_view = pyqtSignal(list)

    def __init__(self, parent):
        super(UpdateLEDStripThread, self).__init__(parent)
        self.__parent = parent
        self.__stop = False
        self.__loop = asyncio.new_event_loop()
    
    def stop_thread(self):
        print("Stopping analyser...")
        self.__stop = True

    def run(self):
        async def callback(parent):
            # Init image handler
            sct = mss.mss()
            while not self.__stop:
                color_list = parent.get_byte_array_for_screen(sct)
                self.sig_update_view.emit(color_list)
                sleep(0.03)

        self.__loop.run_until_complete(asyncio.wait([callback(self.__parent)]))
        self.__loop.stop()
        self.__loop.close()
        del self.__loop
        self.exit(0)


class SimulationController(QObject):

    def __init__(self, monitor_number, led_sides, led_top, fade_speed):
        super(SimulationController, self).__init__()
        self.monitor_number = monitor_number
        self.led_sides = led_sides
        self.led_top = led_top
        self.fade_speed = fade_speed
        self.__view = SimulationView(self, self.led_sides, self.led_top)
        self.run_color_analyser()
    
    def stop_analyser(self):
        self.__disconnect_drive_thread.stop_thread()

    def update_view(self, color_list):
        self.__view.parse_colors(color_list)

    def run_color_analyser(self):
        self.__disconnect_drive_thread = UpdateLEDStripThread(self)
        self.__disconnect_drive_thread.sig_update_view.connect(self.update_view)
        self.__disconnect_drive_thread.start()

    def adjust_color_lightness(self, color):
        # TODO: Define and test a proper algorithm to bring the best color accuracy
        r, g, b = color
        h, l, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        l = max(min(l**0.9, 1.0), 0.0)
        r, g, b = hls_to_rgb(h, l, s)
        return [int(r * 255), int(g * 255), int(b * 255)]

    def average_color_from_area(self, img, area):
        new_img = img.crop(area)
        color = ImageStat.Stat(new_img).median
        adj_color = self.adjust_color_lightness(color)
        if sum(adj_color) <= 10:
            adj_color = [0, 0, 0]

        return adj_color

    def get_byte_array_for_screen(self, sct, byte_mode=False):
        img_src = sct.grab(sct.monitors[self.monitor_number])
        img = Image.frombytes("RGB", img_src.size, img_src.bgra, "raw", "BGRX")
        img = img.reduce(REDUCTION_FACTOR)
        # img.show()

        w, h = img.size
        height_pixels = int(h / self.led_sides)
        width_pixels = int(w / self.led_top)
        depth_pixels = int(COLOR_REGION / REDUCTION_FACTOR)

        border_colors = []

        # Get colors for 3 borders of monitor
        for left_index in range(0, self.led_sides):
            area = (0, left_index*height_pixels, depth_pixels, (left_index+1)*height_pixels)
            border_colors.append(self.average_color_from_area(img, area))
        border_colors.reverse()

        for top_index in range(0, self.led_top):
            area = (top_index*width_pixels, 0, (top_index+1)*width_pixels, depth_pixels)
            border_colors.append(self.average_color_from_area(img, area))

        for right_index in range(0, self.led_sides):
            area = (w-depth_pixels, right_index*height_pixels, w, (right_index+1)*height_pixels)
            border_colors.append(self.average_color_from_area(img, area))
        
        # Create byte list
        byte_list = bytearray()

        for border_color in border_colors:
            for pixel in border_color:
                byte_list.append(pixel)
        # byte_list.append(10) # Terminate with newline character
        
        if byte_mode:
            return byte_list
        return border_colors
