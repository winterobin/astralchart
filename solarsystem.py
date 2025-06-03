import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from io import BytesIO
    from PIL import Image
    import base64
    from datetime import datetime, timezone
    return BytesIO, Image, base64, datetime, mo, np, plt, timezone


@app.cell
def _(mo):
    # Cella 1: Dropdown per giorno, mese, anno
    day_dropdown = mo.ui.dropdown(options=list(range(1, 32)), label="Day", value=1)
    month_dropdown = mo.ui.dropdown(options=list(range(1, 13)), label="Month", value=1)
    year_dropdown = mo.ui.dropdown(options=list(range(1900, 2101)), label="Year", value=2024)
    return day_dropdown, month_dropdown, year_dropdown


@app.cell
def _():
    # Cella 2: Pianeti (fino a Marte) con dati orbita e colore
    planets = {
        "Mercury": {"radius": 0.4, "speed": 4.15, "color": "gray"},
        "Venus": {"radius": 0.7, "speed": 1.62, "color": "orange"},
        "Earth": {"radius": 1.0, "speed": 1.00, "color": "blue"},
        "Mars": {"radius": 1.5, "speed": 0.53, "color": "red"},
    }

    return (planets,)


@app.cell
def _(BytesIO, Image, datetime, np, planets, plt, timezone):
    # Cella 3: Funzione che genera immagine del sistema solare
    def genera_sistema_solare(date):
        # Calcola "tempo" come giorno dell'anno più anni trascorsi * 365 (semplificato)
        tempo = (date - datetime(date.year, 1, 1, tzinfo=timezone.utc)).days + (date.year - 1900) * 365
    
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_aspect("equal")
        ax.set_facecolor("black")
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.axis('off')

        # Sole al centro
        ax.plot(0, 0, "o", color="yellow", markersize=12)

        # Orbite tratteggiate
        for planet in planets.values():
            circle = plt.Circle((0, 0), planet["radius"], color="white", linestyle="dashed", fill=False, alpha=0.3)
            ax.add_artist(circle)

        # Posizione pianeti
        for name, planet in planets.items():
            angle = np.radians(tempo * planet["speed"])
            x = planet["radius"] * np.cos(angle)
            y = planet["radius"] * np.sin(angle)
            ax.plot(x, y, "o", color=planet["color"], label=name)

        leg = ax.legend(loc="upper right", fontsize="small", facecolor="black", framealpha=0.5)
        for text in leg.get_texts():
            text.set_color("white")

        # Salva immagine in memoria
        buf = BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight", facecolor='black')
        plt.close(fig)
        buf.seek(0)
        return Image.open(buf)
    return (genera_sistema_solare,)


@app.cell
def _(BytesIO, base64):
    # Cella 4: Funzione di supporto per convertire immagine PIL in base64
    def img_to_base64(img):
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    return (img_to_base64,)


@app.cell
def _(
    datetime,
    day_dropdown,
    genera_sistema_solare,
    img_to_base64,
    mo,
    month_dropdown,
    timezone,
    year_dropdown,
):
    # Cella 5: Funzione che mostra immagine aggiornata in base a dropdown data
    def sistema_solare():
        try:
            date = datetime(year_dropdown.value, month_dropdown.value, day_dropdown.value, tzinfo=timezone.utc)
        except ValueError:
            return mo.md("## Invalid date selected!")

        img = genera_sistema_solare(date)
        img_b64 = img_to_base64(img)
        html = f'<img src="data:image/png;base64,{img_b64}" alt="Solar System" width="400"/>'
        return mo.md(f"### Date: {date.strftime('%Y-%m-%d')}"), mo.md(html)

    # Mostra menu e immagine
    day_dropdown, month_dropdown, year_dropdown, sistema_solare()
    return


if __name__ == "__main__":
    app.run()
