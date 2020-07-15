from PyQt5.QtCore import QFile, QTextStream
import sys
import os



def get_path(path):
    """ Obtain absolute path for file contained within the package.

        Args:
            path (str): Relative path to package.

        Returns:
            (str): Absolute path of the given relative path.
    """

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, path)

def load_style_sheet(stylesheet, obj):
    """
    Loads the given style file to the targeted qt app
    """

    file = QFile(stylesheet)
    file.open(QFile.ReadOnly)
    obj.setStyleSheet(QTextStream(file).readAll())
    file.close()