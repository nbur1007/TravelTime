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

        # Country Selector
        country_layout = QHBoxLayout()
        country_layout.addWidget(QLabel("Country:"))
        self.country_combo = QComboBox()
        self.country_combo.setFixedWidth(300)
        countries = [country.name for country in pycountry.countries]
        self.country_combo.addItems(countries)
        self.country_combo.setEditable(True)
        country_layout.addWidget(self.country_combo)
        country_layout.addStretch()
        layout.addLayout(country_layout)
        
        # Arrival Date Selector
        arrival_layout = QHBoxLayout()
        arrival_layout.addWidget(QLabel("Arrival Date:"))
        self.arrival_date = QDateEdit()
        self.arrival_date.setDate(QDate.currentDate())
        self.arrival_date.setCalendarPopup(True)
        self.arrival_date.setFixedWidth(150)
        arrival_layout.addWidget(self.arrival_date)
        arrival_layout.addStretch()
        layout.addLayout(arrival_layout)
        
        # Departure Date Selector
        departure_layout = QHBoxLayout()
        departure_layout.addWidget(QLabel("Departure Date:"))
        self.departure_date = QDateEdit()
        self.departure_date.setDate(QDate.currentDate())
        self.departure_date.setCalendarPopup(True)
        self.departure_date.setFixedWidth(150)
        departure_layout.addWidget(self.departure_date)
        departure_layout.addStretch()
        layout.addLayout(departure_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.add_trip_btn = QPushButton("Add Trip")
        self.view_totals_btn = QPushButton("View Totals")
        self.clear_data_btn = QPushButton("Clear Data")
        self.remove_country_btn = QPushButton("Remove Country Data")
        
        button_layout.addWidget(self.add_trip_btn)
        button_layout.addWidget(self.view_totals_btn)
        button_layout.addWidget(self.clear_data_btn)
        button_layout.addWidget(self.remove_country_btn)
        layout.addLayout(button_layout)
        
        # Output Box
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFixedHeight(200)
        layout.addWidget(self.output_text)




def main():
    app = QApplication(sys.argv)
    window = TravelTimeApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()