from datetime import date
import requests
import json
import matplotlib.pyplot as plt


def get_data():
    """Retrieve the earthquake data from USGS API."""
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )
    data = response.json()
    return data


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    year = date.fromtimestamp(timestamp / 1000).year
    return year


def get_magnitude(earthquake):
    """Retrieve the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


def get_magnitudes_per_year(earthquakes):
    """Return a dictionary with years as keys and lists of magnitudes as values."""
    magnitudes_by_year = {}
    for quake in earthquakes:
        year = get_year(quake)
        mag = get_magnitude(quake)
        if mag is None:
            continue  # skip missing magnitudes
        if year not in magnitudes_by_year:
            magnitudes_by_year[year] = []
        magnitudes_by_year[year].append(mag)
    return magnitudes_by_year


def plot_number_per_year(earthquakes):
    """Plot number of earthquakes per year."""
    magnitudes_by_year = get_magnitudes_per_year(earthquakes)
    years = sorted(magnitudes_by_year.keys())
    counts = [len(magnitudes_by_year[y]) for y in years]

    plt.figure(figsize=(8, 4))
    plt.bar(years, counts, color='skyblue')
    plt.xlabel("Year")
    plt.ylabel("Number of Earthquakes")
    plt.title("Number of Earthquakes per Year")
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.savefig("number_per_year.png")
    plt.show()


def plot_average_magnitude_per_year(earthquakes):
    """Plot average magnitude of earthquakes per year."""
    magnitudes_by_year = get_magnitudes_per_year(earthquakes)
    years = sorted(magnitudes_by_year.keys())
    avg_magnitudes = [sum(magnitudes_by_year[y]) / len(magnitudes_by_year[y]) for y in years]

    plt.figure(figsize=(8, 4))
    plt.plot(years, avg_magnitudes, marker='o', color='orange')
    plt.xlabel("Year")
    plt.ylabel("Average Magnitude")
    plt.title("Average Earthquake Magnitude per Year")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig("average_magnitude_per_year.png")
    plt.show()


# --- Main execution ---
if __name__ == "__main__":
    quakes = get_data()['features']
    plot_number_per_year(quakes)
    plt.clf()
    plot_average_magnitude_per_year(quakes)
