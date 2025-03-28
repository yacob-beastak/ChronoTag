import sqlite3

class RunnerRepository:
    def __init__(self, db_path="bezci.db"):
        self.db_path = db_path

    def create_table(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute('''CREATE TABLE IF NOT EXISTS bezci (
                                ID TEXT PRIMARY KEY,
                                Meno TEXT,
                                Time TEXT
                            )''')
        except sqlite3.Error as e:
            print("Error creating table:", e)

    def insert_runner(self, runner_id, name):
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute('INSERT INTO bezci VALUES (?, ?, ?)', (runner_id, name, '00:00:00'))
        except sqlite3.Error as e:
            print("Error inserting runner:", e)

    def runner_exists(self, runner_id):
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute('SELECT 1 FROM bezci WHERE ID=?', (runner_id,))
                return c.fetchone() is not None
        except sqlite3.Error as e:
            print("Error checking runner existence:", e)
            return False

    def get_all_runners(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute('SELECT * FROM bezci')
                return {row[0]: {'meno': row[1], 'cas': row[2]} for row in c.fetchall()}
        except sqlite3.Error as e:
            print("Error loading runners:", e)
            return {}

    def update_time(self, runner_id, time):
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute('UPDATE bezci SET Time=? WHERE ID=?', (time, runner_id))
        except sqlite3.Error as e:
            print("Error updating time:", e)

    def delete_all_runners(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute('DELETE FROM bezci')
        except sqlite3.Error as e:
            print("Error deleting runners:", e)

    def get_runner(self, runner_id):
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute('SELECT * FROM bezci WHERE ID=?', (runner_id,))
                return c.fetchone()
        except sqlite3.Error as e:
            print("Error getting runner:", e)
            return None
