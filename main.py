# main.py

from PyQt5.QtWidgets import QApplication
from stopky_app import StopkyApp
import sys
import sqlite3


def create_table():
    try:
        conn = sqlite3.connect('bezci.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS bezci (
                        ID TEXT PRIMARY KEY,
                        Meno TEXT,
                        Time TEXT
                    )''')
        conn.commit()
    except sqlite3.Error as e:
        print("Error creating table in database:", e)
    finally:
        conn.close()
 

if __name__ == "__main__":
    create_table()  # Vytvorenie tabuľky pri spustení aplikácie
    app = QApplication(sys.argv)
    ex = StopkyApp()
    ex.showMaximized()
    sys.exit(app.exec_())