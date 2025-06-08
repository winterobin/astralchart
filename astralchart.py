import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import datetime as dt
    from astropy.time import Time
    from astropy.coordinates import get_body_barycentric, SphericalRepresentation, solar_system_ephemeris, get_body
    import astropy.units as u
    import pandas as pd
    import altair as alt
    return Time, alt, dt, get_body, mo, np, pd, solar_system_ephemeris, u


@app.cell
def _(dt, mo):
    datetime_picker = mo.ui.datetime(
        start=dt.datetime(1900, 1, 1),
        stop=dt.datetime(2200, 12, 31, 23, 59, 59),
        value=dt.datetime.now(),
    )
    datetime_picker
    return (datetime_picker,)


@app.cell
def _(Time, datetime_picker, dt, get_body, np, pd, u):
    ref_zodiac = [
        {"name": "aries",
        "start": dt.datetime(datetime_picker.value.year, 3, 21, 0, 0, 0),
        "end": dt.datetime(datetime_picker.value.year, 4, 20, 23, 59, 59),
         "element": "fire",
         "color": "red",
        },
        {"name": "taurus",
        "start": dt.datetime(datetime_picker.value.year, 4, 21, 0, 0, 0),
        "end": dt.datetime(datetime_picker.value.year, 5, 20, 23, 59, 59),
        "element": "earth",
        "color": "green",
        },
        {"name": "gemini",
        "start": dt.datetime(datetime_picker.value.year, 5, 21, 0, 0, 0),
        "end": dt.datetime(datetime_picker.value.year, 6, 21, 23, 59, 59),
        "element": "air",
        "color": "cyan",
        },
        {"name": "cancer",
        "start": dt.datetime(datetime_picker.value.year, 6, 22, 0, 0, 0),
        "end": dt.datetime(datetime_picker.value.year, 7, 22, 23, 59, 59),
        "element": "water",
        "color": "blue",
        },
        {"name": "leo",
        "start": dt.datetime(datetime_picker.value.year, 7, 23, 0, 0, 0),
        "end": dt.datetime(datetime_picker.value.year, 8, 23, 23, 59, 59),
        "element": "fire",
        "color": "red",
        },
        {"name": "virgo",
        "start": dt.datetime(datetime_picker.value.year, 8, 24, 0, 0, 0),
        "end": dt.datetime(datetime_picker.value.year, 9, 22, 23, 59, 59),
        "element": "earth",
        "color": "green",
        },
        {"name": "libra",
        "start": dt.datetime(datetime_picker.value.year, 9, 23, 0, 0, 0),
        "end": dt.datetime(datetime_picker.value.year, 10, 22, 23, 59, 59),
        "element": "air",
        "color": "cyan",
        },
        {"name": "scorpio",
        "start": dt.datetime(datetime_picker.value.year, 10, 23, 0, 0, 0),
        "end": dt.datetime(datetime_picker.value.year, 11, 22, 23, 59, 59),
        "element": "water",
        "color": "blue",
        },
        {"name": "sagittarius",
        "start": dt.datetime(datetime_picker.value.year, 11, 23, 0, 0, 0),
        "end": dt.datetime(datetime_picker.value.year, 12, 21, 23, 59, 59),
        "element": "fire",
        "color": "red",
        },
        {"name": "capricorn",
        "start": dt.datetime(datetime_picker.value.year, 12, 22, 0, 0, 0),
        "end": dt.datetime(datetime_picker.value.year, 1, 20, 23, 59, 59),
        "element": "earth",
        "color": "green",
        },
        {"name": "aquarius",
        "start": dt.datetime(datetime_picker.value.year, 1, 21, 0, 0, 0),
        "end": dt.datetime(datetime_picker.value.year, 2, 19, 23, 59, 59),
        "element": "air",
        "color": "cyan",
        },
        {"name": "pisces",
        "start": dt.datetime(datetime_picker.value.year, 2, 20, 0, 0, 0),
        "end": dt.datetime(datetime_picker.value.year, 3, 20, 23, 59, 59),
        "element": "water",
        "color": "blue",
        }
    ]

    ref_zodiac = pd.DataFrame(ref_zodiac)

    ref_zodiac["radius_norm"] = 100

    ref_zodiac["lon_rad_start"] = ref_zodiac["start"].apply(
            lambda t: get_body("sun", time=Time(t), location=None).spherical.lon.to(u.rad).value
        )

    ref_zodiac["lon_rad_end"] = ref_zodiac["end"].apply(
            lambda t: get_body("sun", time=Time(t), location=None).spherical.lon.to(u.rad).value
        )

    ref_zodiac.loc[ref_zodiac["name"] == "aries", "lon_rad_start"] = 0
    ref_zodiac.loc[ref_zodiac["name"] == "pisces", "lon_rad_end"] = 2*np.pi

    ref_zodiac["lon_rad_delta"] = ref_zodiac["lon_rad_end"] - ref_zodiac["lon_rad_start"]

    # ref_zodiac["x_norm"] = ref_zodiac["radius_norm"] * np.cos(ref_zodiac["lon_rad_start"])
    # ref_zodiac["y_norm"] = ref_zodiac["radius_norm"] * np.sin(ref_zodiac["lon_rad_start"])

    #ref_zodiac
    return (ref_zodiac,)


@app.cell
def _(Time, datetime_picker):
    obs_time = Time(datetime_picker.value)
    return (obs_time,)


@app.cell
def _(solar_system_ephemeris):
    bodies = list(solar_system_ephemeris.bodies)
    bodies.remove("earth-moon-barycenter")
    bodies.append("pluto")

    colors = ["blue", "gold", "silver", "gray", "yellow", "red", "khaki", "purple", "cyan", "navy", "black"]

    body_color_map = dict(zip(bodies, colors))

    #body_color_map
    return (body_color_map,)


@app.cell
def _(
    body_color_map,
    get_body,
    np,
    obs_time,
    pd,
    ref_zodiac,
    solar_system_ephemeris,
    u,
):
    tmp_data = []
    with solar_system_ephemeris.set('de430'):
        for body in body_color_map.keys():
            skycoord = get_body(body, time=obs_time, location=None)
    
            tmp_data.append(
                {
                    "body": body.capitalize(),
                    "skycoord": skycoord,
                    "x_au": skycoord.cartesian.x.to(u.AU).value,
                    "y_au": skycoord.cartesian.y.to(u.AU).value,
                    "z_au": skycoord.cartesian.z.to(u.AU).value,
                    "radius_au": skycoord.spherical.distance.to(u.AU).value,
                    "lat_rad": skycoord.spherical.lat.to(u.rad).value,
                    "lon_rad": skycoord.spherical.lon.to(u.rad).value,
                    "color": body_color_map[body]
                }
            )

    df_geocentric = pd.DataFrame(tmp_data)
    df_geocentric = df_geocentric.sort_values(by='radius_au',ascending=True)
    df_geocentric = df_geocentric.reset_index(drop=True)
    df_geocentric.insert(value=pd.Series(range(0, len(df_geocentric)+1, 1)), loc=1, column="radius_norm")
    df_geocentric["radius_norm"] = df_geocentric["radius_norm"] *2
    df_geocentric["x_norm"] = df_geocentric["radius_norm"] * np.cos(df_geocentric["lon_rad"])
    df_geocentric["y_norm"] = df_geocentric["radius_norm"] * np.sin(df_geocentric["lon_rad"])

    def find_zodiac(lon_rad):
        for _, row in ref_zodiac.iterrows():
            if row["lon_rad_start"] < row["lon_rad_end"]:
                if row["lon_rad_start"] <= lon_rad < row["lon_rad_end"]:
                    return row["name"]
            else:
                if lon_rad >= row["lon_rad_start"] or lon_rad < row["lon_rad_end"]:
                    return row["name"]
        return None

    df_geocentric["zodiac_sign"] = df_geocentric["lon_rad"].apply(find_zodiac)
    df_geocentric.loc[df_geocentric["body"] == "Earth", "zodiac_sign"] = ""

    #df_geocentric
    return (df_geocentric,)


@app.cell
def _(alt, body_color_map, df_geocentric, np, ref_zodiac):
    chart_gc = (
        alt.Chart(df_geocentric)
        .mark_circle(size=50)
        .encode(
            # x=alt.X("x_au", scale=alt.Scale(domain=[-3, 3], clamp=True)),
            # y=alt.Y("y_au", scale=alt.Scale(domain=[-3, 3], clamp=True)),
            x=alt.X("x_norm", scale=alt.Scale(domain=[-25, 25], clamp=True)).axis(None),
            y=alt.Y("y_norm", scale=alt.Scale(domain=[-25, 25], clamp=True)).axis(None),
            color=alt.Color(
                "body:N",
                scale=alt.Scale(
                    domain=[b.capitalize() for b in body_color_map.keys()],
                    range=body_color_map.values(),
                ),
                legend=alt.Legend(title="Body"),
            ),
            tooltip=["body", "zodiac_sign"],
        )
        .properties(width=400, height=400)
    )

    chart_gc_zodiac = (
        alt.Chart(ref_zodiac)
        .transform_calculate(
            neg_lon_rad_start="-datum.lon_rad_start",
            neg_lon_rad_end="-datum.lon_rad_end",
        )
        .mark_arc(thetaOffset=np.pi / 2, theta2Offset=np.pi / 2, opacity=0.1)
        .encode(
            theta=alt.Theta("neg_lon_rad_start:Q", sort=None, scale=None),
            theta2=alt.Theta("neg_lon_rad_end:Q", sort=None, scale=None),
            color=alt.Color(
                "element:N",
                sort=None,
                scale=alt.Scale(
                    domain=ref_zodiac["element"].tolist(),
                    range=ref_zodiac["color"].tolist(),
                ),
                legend=None,
            ),
        )
        .properties(width=400, height=400)
    )

    chart_gc_zodiac_text = (
        alt.Chart(ref_zodiac)
        .transform_calculate(
            neg_lon_rad_start="-datum.lon_rad_start",
            neg_lon_rad_end="-datum.lon_rad_end",
        )
        .encode(
            theta=alt.Theta("neg_lon_rad_start:Q", sort=None, scale=None),
            theta2=alt.Theta("neg_lon_rad_end:Q", sort=None, scale=None),
            color=alt.Color(
                "element:N",
                sort=None,
                scale=alt.Scale(
                    domain=ref_zodiac["element"].tolist(),
                    range=ref_zodiac["color"].tolist(),
                ),
                # legend=
            ),
        )
        .mark_text(
            thetaOffset=np.pi / 2 - np.pi / 12,
            theta2Offset=np.pi / 2 - np.pi / 12,
            radius=200,
            size=20,
        )
        .encode(text="name:N")
        .properties(width=400, height=400)
    )

    alt.layer(
        chart_gc_zodiac,
        chart_gc_zodiac_text,
        chart_gc,
        resolve={"scale": {"color": "independent"}},
    ).configure_axis(grid=False).configure_view(stroke=None).configure_legend(
        padding=50,
    )
    return


@app.cell
def _(df_geocentric, mo, obs_time):
    mo.md(
        f"""
    On date {obs_time} this is your astral chart:   
            - Sun ☉: {df_geocentric.loc[df_geocentric["body"] == "Sun", "zodiac_sign"].values[0].capitalize()}  
            - Moon ☽: {df_geocentric.loc[df_geocentric["body"] == "Moon", "zodiac_sign"].values[0].capitalize()}  
            - Mercury ☿: {df_geocentric.loc[df_geocentric["body"] == "Mercury", "zodiac_sign"].values[0].capitalize()}  
            - Venus ♀: {df_geocentric.loc[df_geocentric["body"] == "Venus", "zodiac_sign"].values[0].capitalize()}  
            - Mars ♂: {df_geocentric.loc[df_geocentric["body"] == "Mars", "zodiac_sign"].values[0].capitalize()}  
            - Jupiter ♃: {df_geocentric.loc[df_geocentric["body"] == "Jupiter", "zodiac_sign"].values[0].capitalize()}  
            - Saturn ♄: {df_geocentric.loc[df_geocentric["body"] == "Saturn", "zodiac_sign"].values[0].capitalize()}  
            - Uranus ♅: {df_geocentric.loc[df_geocentric["body"] == "Uranus", "zodiac_sign"].values[0].capitalize()}  
            - Neptune ♆: {df_geocentric.loc[df_geocentric["body"] == "Neptune", "zodiac_sign"].values[0].capitalize()}  
            - Pluto ♇: {df_geocentric.loc[df_geocentric["body"] == "Pluto", "zodiac_sign"].values[0].capitalize()}
    """
    )
    return


if __name__ == "__main__":
    app.run()
