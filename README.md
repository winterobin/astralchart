Solar System Visualization with Marimo
This project is an interactive visualization of the solar system (up to Mars) created using Python and Marimo.

Features
Displays the Sun and planets Mercury, Venus, Earth, and Mars orbiting around it.

Shows planetary orbits as dashed circles.

Includes a dropdown menu to select the date (day, month, year).

Planet positions update dynamically based on the selected date.

Dark theme with clear legend showing planet names in white.

Installation
Make sure you have Python installed (version 3.7 or higher recommended).

Install the required packages:

bash
Copia
Modifica
pip install marimo numpy matplotlib skyfield pillow
How to Run
Run the main script (e.g. app.py) with:

bash
Copia
Modifica
python app.py
This will start the Marimo app in your default browser.

Usage
Use the dropdown menus to select the day, month, and year.

The plot updates automatically to show the planetary positions for the selected date.

The orbits are displayed as dashed circles, and planets as colored dots.

The legend identifies each planet by color.

Code Structure
planets dictionary defines orbital radius, orbital speed, and color for each planet.

genera_sistema_solare(date) function generates the plot image for the given date.

Marimo UI components handle user input and display the image.

License
MIT License

