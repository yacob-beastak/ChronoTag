from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QScrollArea, QApplication, QDialog, QHBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap
import csv  
import sqlite3
from stopwatch import Stopwatch

class StopkyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stopwatch")
        self.setGeometry(0, 0, QApplication.desktop().screenGeometry().width(), QApplication.desktop().screenGeometry().height())
        self.running = False  

        # Load background image
        background_label = QLabel(self)
        background_label.resize(self.size())
        self.setStyleSheet("background-color: black; color: white;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.add_runner_button = QPushButton("Pridať bežca")
        self.add_runner_button.setStyleSheet("background-color: #7680ad; color: white; padding: 10px 24px; font-size: 16px; border-radius: 10px;")
        self.add_runner_button.clicked.connect(self.add_runner)
        self.layout.addWidget(self.add_runner_button)

        
        self.export_button = QPushButton("Exportovať do CSV")
        self.export_button.setStyleSheet("background-color: #7680ad; color: white; padding: 10px 24px; font-size: 16px; border-radius: 10px;")
        self.export_button.clicked.connect(self.export_to_csv)
        self.layout.addWidget(self.export_button)


        # Zmena na QScrollArea pre zoznam bežcov
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.runners_widget = QWidget()
        self.runners_layout = QVBoxLayout(self.runners_widget)
        self.scroll_area.setWidget(self.runners_widget)

        self.load_runners_from_db()  # Načítanie bežcov z db

        # Načítanie bežcov do výpisu po štarte aplikácie
        self.update_runners_listbox()
    

    def add_runner(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Pridať bežca")

        layout = QVBoxLayout()

        id_label = QLabel("RFID:")
        layout.addWidget(id_label)

        id_entry = QLineEdit()
        layout.addWidget(id_entry)

        name_label = QLabel("Runner name:")
        layout.addWidget(name_label)

        name_entry = QLineEdit()
        layout.addWidget(name_entry)

        add_button = QPushButton("+Add")
        add_button.clicked.connect(lambda: self.save_runner(id_entry, name_entry, dialog))
        layout.addWidget(add_button)

        dialog.setLayout(layout)

        # Štýly pre dialógové okno
        dialog.setStyleSheet(
            "QDialog { background-color: #1f1f1f; }"
            "QLabel { color: white; font-size: 14px;background-color: #1f1f1f; }"
            "QLineEdit { background-color: #3a3a3a; color: white; border-radius: 5px; padding: 5px; }"
            "QPushButton { background-color: #7680ad; color: white; padding: 10px 24px; font-size: 16px; border-radius: 10px; }"
            "QPushButton:hover { background-color: #465287; }"
        )

        dialog.exec_()

    def save_runner(self, id_entry, name_entry, dialog):
        id_text = id_entry.text().strip()
        name = name_entry.text().strip()

        if id_text == '':
            QMessageBox.critical(dialog, "Chyba", "Prosím, zadajte platné ID bežca.")
            return

        runner_id = id_text

        if self.runner_exists_in_db(runner_id):
            QMessageBox.critical(dialog, "Chyba", "Bežec s týmto ID už existuje.")
            return

        if name == '':
            QMessageBox.critical(dialog, "Chyba", "Prosím, zadajte meno bežca.")
            return

        self.insert_runner_to_db(runner_id, name)  # Ukladanie bežca do DB 
        self.load_runners_from_db()
        self.update_runners_listbox()

        self.add_runner_to_layout(runner_id, name)

        id_entry.clear()
        name_entry.clear()

        print(f"Pridaný bežec s ID: {runner_id}, Meno: {name}")

    def runner_exists_in_db(self, runner_id):
        try:
            conn = sqlite3.connect('bezci.db')
            c = conn.cursor()
            c.execute('SELECT * FROM bezci WHERE id=?', (runner_id,))
            return c.fetchone() is not None
        except sqlite3.Error as e:
            print("Chyba pri kontrole existencie bežca v DB:", e)
            return False
        finally:
            conn.close()

    def load_runners_from_db(self):
        try:
            conn = sqlite3.connect('bezci.db')
            c = conn.cursor()
            self.bezci = {}
            c.execute('SELECT * FROM bezci')
            for row in c.fetchall():
                self.bezci[row[0]] = {'meno': row[1], 'čas': row[2]}
        except sqlite3.Error as e:
            print("Chyba pri ukladaní bežca do DB:", e)
            self.bezci = {}
        finally:
            conn.close()

    def insert_runner_to_db(self, runner_id, name):
        try:
            conn = sqlite3.connect('bezci.db')
            c = conn.cursor()
            c.execute('INSERT INTO bezci VALUES (?, ?, ?)', (runner_id, name, '00:00:00'))
            conn.commit()
        except sqlite3.Error as e:
            print("Chyba pri ukladaní bežca do DB:", e)
        finally:
            conn.close()

    def update_runners_listbox(self):
        for i in reversed(range(self.runners_layout.count())):
            widget_item = self.runners_layout.itemAt(i).widget()
            if widget_item is not None:
                widget_runner_id = getattr(widget_item, 'runner_id', None)
                print(f"Widget runner ID: {widget_runner_id}")
                widget_item.setParent(None)

        for runner_id, runner_info in self.bezci.items():
            self.add_runner_to_layout(runner_id, runner_info["meno"])


    def add_runner_to_layout(self, runner_id, name):
        # Skontrolujeme, či sa widget s daným runner_id už nepridal
        existing_widgets = [self.runners_layout.itemAt(i).widget() for i in range(self.runners_layout.count())]
        existing_runner_ids = [widget.runner_id for widget in existing_widgets if isinstance(widget, QWidget) and hasattr(widget, 'runner_id')]

        if runner_id not in existing_runner_ids:
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setSpacing(5)  # Menší priestor medzi bežcami
            layout.addWidget(QLabel(f"ID: {runner_id}, Meno: {name}"))
            stopwatch_widget = Stopwatch(widget, self, runner_id, name)
            layout.addWidget(stopwatch_widget)
            widget.runner_id = runner_id  # Pridáme runner_id ako atribút widgetu
            self.runners_layout.addWidget(widget)
            stopwatch_widget.timer.timeout.connect(lambda: self.update_runner_time(runner_id, stopwatch_widget.get_time()))

    def update_runner_time(self, runner_id, time):
        self.bezci[runner_id]["čas"] = time
        

    def update_runner_time_in_db(self, runner_id, time):
        try:
            conn = sqlite3.connect('bezci.db')
            c = conn.cursor()
            c.execute('UPDATE bezci SET Time=? WHERE id=?', (time, runner_id))
            conn.commit()
            print(f"SQL UPDATE: Updated time for runner ID {runner_id} to {time}")
        except sqlite3.Error as e:
            print("Chyba při aktualizácii času bežca v databáze:", e)
        finally:
            conn.close()

    def export_to_csv(self):
        with open("runners.csv", "w", newline='') as csvfile:
            fieldnames = ['ID', 'Meno', 'Čas']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for runner_id, runner_info in self.bezci.items():
                writer.writerow({'ID': runner_id, 'Meno': runner_info["meno"], 'Čas': runner_info["čas"]})

        # Notifikácia v štýle dialógového okna pridávania bežca
        notification_dialog = QDialog(self)
        notification_dialog.setWindowTitle("Info")
        notification_dialog.setStyleSheet(
            "QDialog { background-color: #1f1f1f; }"
            "QLabel { color: white; font-size: 14px; background-color: #1f1f1f;}"
            "QPushButton { background-color: #7680ad; color: white; padding: 10px 24px; font-size: 16px; border-radius: 10px; }"
            "QPushButton:hover { background-color: #465287; }"
        )

        layout = QVBoxLayout()

        message_label = QLabel("Dáta boli úspešne exportované do CSV súboru.")
        layout.addWidget(message_label)

        close_button = QPushButton("OK")
        close_button.clicked.connect(notification_dialog.accept)
        layout.addWidget(close_button)

        notification_dialog.setLayout(layout)
        notification_dialog.exec_()
