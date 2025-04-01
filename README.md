# ChronoTag 🏃‍♂️⏱

**ChronoTag** is a lightweight desktop app for tracking race times using RFID tags or manual input. Ideal for small events, group runs, or training sessions.

---

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()
[![Stars](https://img.shields.io/github/stars/tvoje-meno/ChronoTag.svg?style=social)]()

---

## ✨ Features

- Add runners with RFID tag IDs
- Start/stop timers manually or using RFID scanner
- Scrollable UI with modern dark theme
- Export results to CSV
- Persistent local SQLite database
- Clean interface with icons
- Designed for quick event setups

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yacob-beastak/ChronoTag.git
   cd ChronoTag
   ```

2. Install dependencies:
   ```bash
   pip install PyQt5
   ```

3. Run the app:
   ```bash
   python main.py
   ```

## 🧠 RFID Workflow

1. Register runners with an RFID tag (e.g., `000000123AB`)
2. First beep → start timer
3. Second beep → stop timer
4. Time is saved and can be exported

## 📤 CSV Export

Click the **Export** button to generate a `.csv` file with the following format:

```
ID, Name, Time
```

## 🛠 Tech Stack

- Python 3.10+
- PyQt5 (UI)
- SQLite3 (data storage)

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

---

**Enjoy using ChronoTag!**  
If you like it, give it a ⭐ or contribute improvements.
