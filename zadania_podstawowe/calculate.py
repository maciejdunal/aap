# Napisz program, który oblicza wartości funkcji dla𝑓(𝑥) = 𝑐𝑜𝑠(𝑥)+𝑙𝑛(𝑥+1)2
# dużego zestawu wartości (np. od 1 do 1e6 z krokiem 0.01). Podziel zakres na𝑥𝑥
# fragmenty i wykorzystaj moduł multiprocessing, aby równolegle obliczyć wartości
# funkcji dla każdego fragmentu

import multiprocessing
import numpy as np
from math import cos, log
import logging

logging.basicConfig(level=logging.INFO)

def calculate_values(x_values):
    """Oblicza wartości funkcji cos(x) + ln(x + 1) dla przekazanego zakresu x."""
    return [cos(x) + log(x + 1) for x in x_values]

def main():
    x = np.arange(1, 1e6, 0.01)
    num_processes = multiprocessing.cpu_count()
    segment_size = len(x) // num_processes  # Zmieniona nazwa zamiast chunk_size

    x_segments = [x[i * segment_size:(i + 1) * segment_size] for i in range(num_processes)]
    
    with multiprocessing.Pool(num_processes) as pool:
        results = pool.map(calculate_values, x_segments)

    logging.info("Computation finished.")

if __name__ == "__main__":
    main()
