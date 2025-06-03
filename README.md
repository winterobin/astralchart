# 🌞 Solar System Visualization with Marimo 🚀
An interactive and dynamic solar system visualization built in Python using Marimo, showing the orbits of Mercury, Venus, Earth, and Mars around the Sun.

---

## ✨ Features
- 🌍 Displays the Sun and first four planets with accurate orbits

- 🔄 Planets move according to the selected date

- 📅 Select any date via dropdown menus for Day, Month, and Year

- 🎨 Dark theme with white labels and colored planets

- 🔭 Dashed circular orbits for a clean look

- 🪐 Legend with planet names in white for easy identification

---

## ⚙️ Installation
Make sure you have Python 3.7+ installed.

Install dependencies via pip:

pip install marimo numpy matplotlib skyfield pillow

---

## ▶️ How to Run
Run your main app script (e.g., app.py):

python app.py

The app will open in your default web browser.

---

## 🖱️ Usage
- Use dropdown menus to pick a specific date (Day, Month, Year)

- The solar system visualization updates in real-time

- See the planets orbiting with their respective colors and the Sun at the center

- View the orbits as dashed rings around the Sun

- Planet names are displayed in a clear legend on the top right

---

## 🧩 Code Overview
- planets dictionary contains data on each planet's orbital radius, speed, and color

- genera_sistema_solare(date) generates the matplotlib plot for the selected date

- Marimo UI components create dropdown menus and display the generated image dynamically

---

## 📄 License
This project is released under the MIT License.