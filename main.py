# main.py

from PyQt5.QtWidgets import QApplication
from stopky_app import StopkyApp
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = StopkyApp()
    ex.showMaximized()
    sys.exit(app.exec_())
