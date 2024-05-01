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
        print("Chyba pri vytváraní tabuľky v databáze:", e)
    finally:
        conn.close()


def select_all_from_table():
    try:
        conn = sqlite3.connect('bezci.db')
        c = conn.cursor()
        c.execute('SELECT * FROM bezci')
        rows = c.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print("Chyba pri získavaní údajov z tabuľky:", e)
    finally:
        conn.close()

# Volanie funkcie na zobrazenie všetkých záznamov z tabuľky
select_all_from_table()


if __name__ == "__main__":
    create_table()  # Vytvorenie tabuľky pri spustení aplikácie
    app = QApplication(sys.argv)
    ex = StopkyApp()
    ex.showMaximized()
    sys.exit(app.exec_())


