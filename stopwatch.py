# stopwatch.py

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import QTimer
import time

class Stopwatch(QWidget):
    def __init__(self, parent, app, runner_id, name):
        super().__init__(parent)
        self.app = app
        self.runner_id = runner_id
        self.name = name
        self.start_time = None
        self.running = False
        self.elapsed_time = 0

        self.label = QLabel("00:00:00")
        self.label.setStyleSheet("color: white; font-size: 12px;")

        self.start_stop_button = QPushButton("START")
        self.start_stop_button.clicked.connect(self.start_stop)
        self.start_stop_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 8px 20px; font-size: 14px; border: none; border-radius: 5px; } QPushButton:hover { background-color: #45a049; }")

        self.reset_button = QPushButton("RESET")
        self.reset_button.clicked.connect(self.reset)
        self.reset_button.setStyleSheet("QPushButton { background-color: #532c5c; color: white; padding: 8px 20px; font-size: 14px; border: none; border-radius: 5px; } QPushButton:hover { background-color: #51205c; }")

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.start_stop_button)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)

    def start_stop(self):
        if not self.running:
            self.start()
        else:
            self.stop()

    def start(self):
        self.running = True
        self.start_time = time.time() - self.elapsed_time
        self.app.running = True  
        self.start_stop_button.setText("STOP")
        self.start_stop_button.setStyleSheet("QPushButton { background-color: #f44336; color: white; padding: 8px 20px; font-size: 14px; border: none; border-radius: 5px; } QPushButton:hover { background-color: #d32f2f; }")
        self.timer.start()  
        self.update()  

    def stop(self):
        if self.running:
            self.running = False
            self.elapsed_time = time.time() - self.start_time
            self.start_stop_button.setText("START")
            self.start_stop_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 8px 20px; font-size: 14px; border: none; border-radius: 5px; } QPushButton:hover { background-color: #45a049; }")
            self.timer.stop()  
        if not self.timer.isActive():  
               self.app.update_runner_time_in_db(self.runner_id, self.get_elapsed_time())


    def reset(self):
        self.elapsed_time = 0
        self.start_time = time.time()
        self.label.setText("00:00:00")
        self.start_stop_button.setText("START")
        self.start_stop_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 8px 20px; font-size: 14px; border: none; border-radius: 5px; } QPushButton:hover { background-color: #45a049; }")
        self.timer.stop()  

    def update(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
            hours, rem = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(rem, 60)
            time_str = "{:0>2}:{:0>2}:{:05.2f}".format(
                int(hours), int(minutes), seconds)
            self.label.setText(time_str)

    def get_elapsed_time(self):
        elapsed_time = self.elapsed_time if not self.running else time.time() - self.start_time
        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        time_str = "{:0>2}:{:0>2}:{:05.2f}".format(
            int(hours), int(minutes), seconds)
        return time_str

    def get_time(self):
        return self.get_elapsed_time()  
