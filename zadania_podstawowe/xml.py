# Na podstawie danych z IMGW w formacie XML, dostępnych pod adresem
# https://danepubliczne.imgw.pl/api/data/meteo/format/xml, napisz program, który
# odczytuje dane, przetwarza informacje o prędkości wiatru z wybranych stacji i
# wyświetla średnią prędkość wiatru na wykresie słupkowym

import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)

def fetch_wind_data():
    url = "https://danepubliczne.imgw.pl/api/data/meteo/format/xml"
    response = requests.get(url)
    root = ET.fromstring(response.content)
    wind_speeds = {}

    for station in root.findall("station"):
        name = station.find("name").text
        wind_speed = station.find("wind_speed").text
        if wind_speed:
            wind_speeds[name] = float(wind_speed)

    return wind_speeds

def plot_wind_data(wind_speeds):
    stations = list(wind_speeds.keys())
    speeds = list(wind_speeds.values())

    plt.bar(stations[:10], speeds[:10])
    plt.xlabel("Station")
    plt.ylabel("Wind Speed (m/s)")
    plt.title("Average Wind Speed")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    wind_data = fetch_wind_data()
    plot_wind_data(wind_data)

if __name__ == "__main__":
    main()
