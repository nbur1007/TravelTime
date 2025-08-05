import sys
import os
import json
import pycountry
from datetime import datetime as dt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QComboBox, QPushButton, 
                             QTextEdit, QDateEdit, QDialog, QDialogButtonBox, 
                             QMessageBox)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon

DATA_FILE = "TravelTimeData.json"

class TravelTimeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TravelTime+")
        self.setWindowIcon(QIcon('TravelTime.png'))
        self.setGeometry(100, 100, 600, 500)

        central_widgit = QWidget()
        self.setCentralWidget(central_widgit)

        layout = QHBoxLayout(central_widgit)

def main():
    app = QApplication(sys.argv)
    window = TravelTimeApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()