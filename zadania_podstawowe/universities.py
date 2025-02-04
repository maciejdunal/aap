# Za pomocą API zwracającego informacje dot. uniwersytetów w danym państwie:
# http://universities.hipolabs.com/search?country=<nazwa_kraju_eng> wyświetl
# nazwy uniwersytetów z 20 wybranych krajów w postaci: {<nazwa_kraju>:
# [<nazwa_uniwersytet1>, <nazwa_uniwersytet2>,...], ...}. W celu przyspieszenia
# pobierania danych, wykorzystaj moduł threading do realizacji wielowątkowego
# pobierania informacji

import threading
import requests
import logging

logging.basicConfig(level=logging.INFO)

def fetch_universities(country, result):
    url = f"http://universities.hipolabs.com/search?country={country}"
    response = requests.get(url)
    if response.status_code == 200:
        universities = [uni["name"] for uni in response.json()]
        result[country] = universities
        logging.info(f"Fetched {len(universities)} universities from {country}")

def main():
    countries = ["United States", "Canada", "Australia", "United Kingdom", "Germany"]
    threads = []
    result = {}

    for country in countries:
        thread = threading.Thread(target=fetch_universities, args=(country, result))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    logging.info(result)

if __name__ == "__main__":
    main()
