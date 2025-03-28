from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QScrollArea, QApplication, QDialog, QHBoxLayout, QLineEdit, QMessageBox, QInputDialog , QFileDialog
from PyQt5.QtCore import Qt, QEvent 
from PyQt5.QtGui import QPixmap , QIcon
import csv
from runner_repository import RunnerRepository
from stopwatch import Stopwatch

class StopkyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.repo = RunnerRepository()  # ← musí byť tu

        self.setWindowTitle("Stopwatch")
        self.setGeometry(0, 0, QApplication.desktop().screenGeometry().width(), QApplication.desktop().screenGeometry().height())
        self.running = False
        self.buffer = ""

        
        background_label = QLabel(self)
        background_label.resize(self.size())
        self.setStyleSheet("background-color:#1f1e1d; color: white;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        
        self.button_layout = QHBoxLayout()

        self.add_runner_button = QPushButton(QIcon("icons/user-plus.svg"), "Add runner")
        self.add_runner_button.setStyleSheet(
            "QPushButton {\n"
            "  background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #455EB5, stop:0.4389 #5643CC, stop:0.6472 #673FD7);\n"
            "  border-radius: 8px;\n"
            "  border: none;\n"
            "  color: #FFFFFF;\n"
            "  font-size: 16px;\n"
            "  font-weight: 500;\n"
            "  text-align: center;\n"
            "}\n"
            "QPushButton:hover {\n"
            "  background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #AEE46A, stop:0.35 #139C1E, stop:0.80 #00F729, stop:1 #00F729);\n"
            "}\n"
        )
        self.add_runner_button.clicked.connect(self.add_runner)
        self.add_runner_button.setMinimumSize(150, 40)  
        self.button_layout.addWidget(self.add_runner_button)

        self.export_button = QPushButton(QIcon("icons/share.svg"), "CSV Export")
        self.export_button.setStyleSheet(
            "QPushButton {\n"
            "  background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #455EB5, stop:0.4389 #5643CC, stop:0.6472 #673FD7);\n"
            "  border-radius: 8px;\n"
            "  border: none;\n"
            "  color: #FFFFFF;\n"
            "  font-size: 16px;\n"
            "  font-weight: 500;\n"
            "  text-align: center;\n"
            "}\n"
            "QPushButton:hover {\n"
            "  background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #1d1d1d, stop:0.3 #63139c, stop:0.7 #650609, stop:1 #650609);\n"
            "}\n"
        )
        self.export_button.clicked.connect(self.export_to_csv)
        self.export_button.setMinimumSize(150, 40)  
        self.button_layout.addWidget(self.export_button)

        self.clear_data_button = QPushButton(QIcon("icons/database.svg"), "Delete data")
        self.clear_data_button.setStyleSheet(
            "QPushButton {\n"
            "  background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #455EB5, stop:0.4389 #5643CC, stop:0.6472 #673FD7);\n"
            "  border-radius: 8px;\n"
            "  border: none;\n"
            "  color: #FFFFFF;\n"
            "  font-size: 16px;\n"
            "  font-weight: 500;\n"
            "  text-align: center;\n"
            "}\n"
            "QPushButton:hover {\n"
            "  background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #DE7E7E, stop:0.3 #9C1313, stop:0.7 #F73100, stop:1 #F73100);\n"
            "}\n"
        )
        self.clear_data_button.clicked.connect(self.clear_all_data)
        self.clear_data_button.setMinimumSize(150, 40)  
        self.button_layout.addWidget(self.clear_data_button)

        
        self.layout.addLayout(self.button_layout)


        # Change to QScrollArea for runner list
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.runners_widget = QWidget()
        self.runners_layout = QVBoxLayout(self.runners_widget)
        self.scroll_area.setWidget(self.runners_widget)

        self.bezci = self.repo.get_all_runners()  # Loading runners from db

        # Loading runners into the list after starting the application
        self.update_runners_listbox()

        self.installEventFilter(self)

    def add_runner(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add runner")

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
            QMessageBox.critical(dialog, "Error", "Please enter a valid runner ID.")
            return

        runner_id = id_text

        if self.repo.runner_exists(runner_id):
            QMessageBox.critical(dialog, "Error", "A runner with this ID already exists.")
            return

        if name == '':
            QMessageBox.critical(dialog, "Error", "Please enter the runner's name.")
            return

        self.repo.insert_runner(runner_id, name)  # Saving the runner to the DB
        self.bezci = self.repo.get_all_runners()
        self.update_runners_listbox()

        self.add_runner_to_layout(runner_id, name)

        id_entry.clear()
        name_entry.clear()

        print(f"Added runner with ID: {runner_id}, Meno: {name}")

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
        
        existing_widgets = [self.runners_layout.itemAt(i).widget() for i in range(self.runners_layout.count())]
        existing_runner_ids = [widget.runner_id for widget in existing_widgets if isinstance(widget, QWidget) and hasattr(widget, 'runner_id')]

        if runner_id not in existing_runner_ids:
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setSpacing(5)  
            layout.addWidget(QLabel(f"ID: {runner_id}, Meno: {name}"))
            stopwatch_widget = Stopwatch(widget, self, runner_id, name)
            layout.addWidget(stopwatch_widget)
            widget.runner_id = runner_id  
            self.runners_layout.addWidget(widget)
            stopwatch_widget.timer.timeout.connect(lambda: self.update_runner_time(runner_id, stopwatch_widget.get_time()))

    def update_runner_time(self, runner_id, time):
        self.bezci[runner_id]["čas"] = time

    def export_to_csv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "", "CSV Files (*.csv)", options=options)
        try:
            with open(file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Meno", "Čas"])
                for runner_id, runner_info in self.bezci.items():
                    writer.writerow([runner_id, runner_info["meno"], runner_info["čas"]])
            QMessageBox.information(self, "Info", "Data successfully exported.")
        except Exception as e:
            print("Error when exporting to CSV:", e)


    
    def clear_all_data(self):
        reply = QMessageBox.question(self, 'Delete database', 'Are you sure you want to delete all data?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.repo.delete_all_runners()
            self.bezci = {}  
            self.update_runners_listbox()  
            QMessageBox.information(self, "Info", "All data has been successfully deleted.")




    def handle_rfid_input(self, rfid):
        runner_id = rfid.strip()
        if runner_id in self.bezci:
            for i in range(self.runners_layout.count()):
                widget = self.runners_layout.itemAt(i).widget()
                if widget and widget.runner_id == runner_id:
                    stopwatch_widget = widget.findChild(Stopwatch)
                    if stopwatch_widget:
                        if stopwatch_widget.timer.isActive():
                            stopwatch_widget.stop()
                            self.repo.update_time(runner_id, stopwatch_widget.get_elapsed_time())
                        else:
                            stopwatch_widget.start()
                        break
        else:
            QMessageBox.warning(self, "Warning", "There is no runner with this ID.")

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            key = event.text()
            if key.isdigit():
                self.buffer += key
            elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.handle_rfid_input(self.buffer)
                self.buffer = ""
            return True
        return super().eventFilter(source, event)