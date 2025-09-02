import sys
import os
import json
import pycountry
from pathlib import Path
from datetime import datetime as dt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QComboBox, QPushButton, 
                             QTextEdit, QDateEdit, QDialog, QDialogButtonBox, 
                             QMessageBox)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon

# Creation of data file
app_data_dir = Path.home() / ".TravelTime"
app_data_dir.mkdir(exist_ok=True)
DATA_FILE = app_data_dir / "TravelTime.json"

class TravelTimeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TravelTime+")
        self.setWindowIcon(QIcon('TravelTime.ico'))
        self.setGeometry(100, 100, 600, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

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
        main_layout.addLayout(country_layout)
        
        # Arrival Date Selector
        arrival_layout = QHBoxLayout()
        arrival_layout.addWidget(QLabel("Arrival Date:"))
        self.arrival_date = QDateEdit()
        self.arrival_date.setDate(QDate.currentDate())
        self.arrival_date.setCalendarPopup(True)
        self.arrival_date.setFixedWidth(150)
        arrival_layout.addWidget(self.arrival_date)
        arrival_layout.addStretch()
        main_layout.addLayout(arrival_layout)
        
        # Departure Date Selector
        departure_layout = QHBoxLayout()
        departure_layout.addWidget(QLabel("Departure Date:"))
        self.departure_date = QDateEdit()
        self.departure_date.setDate(QDate.currentDate())
        self.departure_date.setCalendarPopup(True)
        self.departure_date.setFixedWidth(150)
        departure_layout.addWidget(self.departure_date)
        departure_layout.addStretch()
        main_layout.addLayout(departure_layout)
        
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
        main_layout.addLayout(button_layout)
        
        # Output Box
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFixedHeight(200)
        main_layout.addWidget(self.output_text)

        # Button Functionality
        self.add_trip_btn.clicked.connect(self.add_trip)
        self.view_totals_btn.clicked.connect(self.view_totals)
        self.clear_data_btn.clicked.connect(self.clear_data)
        self.remove_country_btn.clicked.connect(self.remove_country_data)
    
    
    def load_country_days(self):
        if DATA_FILE.exists():
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        return {}
    
    def save_country_days(self, TravelTime):
        with open(DATA_FILE, "w") as file:
            json.dump(TravelTime, file)
        
    def clear_country_days(self):
        if DATA_FILE.exists():
            with open(DATA_FILE, "w") as file:
                file.write("{}")
            return "Travel Time data has been cleared."
        else:
            return "No data found to clear."
        
    def remove_country_data_func(self, country_name):
        TravelTime = self.load_country_days()
        if country_name in TravelTime:
            del TravelTime[country_name]
            self.save_country_days(TravelTime)
            return f"Data for {country_name} has been removed."
        return f"No data found for {country_name}."

    def days_spent_in_country(self, country_name, arrival_date, departure_date):
        TravelTime = self.load_country_days()
        
        arrival = dt.strptime(arrival_date, "%Y-%m-%d")
        departure = dt.strptime(departure_date, "%Y-%m-%d")
        
        if arrival > departure:
            return "Error: Arrival date must be before departure date."

        delta = departure - arrival
        days_spent = delta.days
        
        if country_name in TravelTime:
            TravelTime[country_name] += days_spent
        else:
            TravelTime[country_name] = days_spent
        
        self.save_country_days(TravelTime)

        return f"You have added {days_spent} days to your total time in {country_name}."
    
    def add_trip(self):
        country = self.country_combo.currentText().strip()
        arrival = self.arrival_date.date().toString("yyyy-MM-dd")
        departure = self.departure_date.date().toString("yyyy-MM-dd")
        
        if not country or not arrival or not departure:
            self.output_text.setText("Please fill in all fields.")
        else:
            result = self.days_spent_in_country(country, arrival, departure)
            self.output_text.setText(result)
    
    def view_totals(self):
        TravelTime = self.load_country_days()
        if not TravelTime:
            self.output_text.setText("No data available.")
        else:
            output = "Total days spent in each country:\n"
            for country, days in TravelTime.items():
                output += f"{country}: {days} days\n"
            self.output_text.setText(output)
    
    def clear_data(self):
        reply = QMessageBox.question(self, 'Clear Data', 
                                   'Are you sure you want to clear all data?',
                                   QMessageBox.StandardButton.Yes | 
                                   QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            result = self.clear_country_days()
            self.output_text.setText(result)
    
    def remove_country_data(self):
        dialog = RemoveCountryDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            country_to_remove = dialog.get_selected_country()
            if country_to_remove:
                result = self.remove_country_data_func(country_to_remove)
                self.output_text.setText(result)

class RemoveCountryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Remove Country Data")
        self.setModal(True)
        self.resize(300, 120)
        
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Select the country to remove:"))
        
        self.country_combo = QComboBox()
        countries = [country.name for country in pycountry.countries]
        self.country_combo.addItems(countries)
        self.country_combo.setEditable(True)
        layout.addWidget(self.country_combo)
        
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                    QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def get_selected_country(self):
        return self.country_combo.currentText().strip()


def main():
    app = QApplication(sys.argv)
    window = TravelTimeApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()