import rasterio
import pandas as pd
import glob
import numpy as np
import os
import time  # Dodaj ten import!

import tkinter as tk
from tkinter import filedialog

def calculate_raster_statistics(input_folder, output_csv):
    # Lista rastrów do przetworzenia
    raster_list = glob.glob(os.path.join(input_folder, '*.tif'))

    # Tworzenie pustego dataframe'u do przechowywania wyników
    results_df = pd.DataFrame()

    # Pętla przez rastry
    start_time = time.time()  # Początkowy czas
    for raster_path in raster_list:
        with rasterio.open(raster_path) as src:
            raster = src.read(1)

            # Obliczanie statystyk
            min_val = np.min(raster)
            max_val = np.max(raster)
            mean_val = np.mean(raster)
            std_val = np.std(raster)
            count_val = np.count_nonzero(~np.isnan(raster))

            # Tworzenie dataframe'u ze statystykami
            df = pd.DataFrame({
                'Raster': [raster_path],
                'Min': [min_val],
                'Max': [max_val],
                'Mean': [mean_val],
                'Std': [std_val],
                'Count': [count_val]
            })

            # Łączenie wyniku z dataframe'em wyników
            results_df = pd.concat([results_df, df])

    # Zapisanie wyników do pliku CSV
    results_df.to_csv(output_csv, index=False)
    elapsed_time = time.time() - start_time  # Czas trwania obliczeń
    print(f"Wyniki zostały zapisane do: {output_csv}")
    print(f"Czas trwania obliczeń: {elapsed_time:.2f} sekundy")

# Tworzymy GUI z pomocą tkinter
root = tk.Tk()
root.withdraw()  # Ukrywamy główne okno, ponieważ nie potrzebujemy pełnej aplikacji GUI

# Wybierz folder z rastrami
input_folder = filedialog.askdirectory(title="Wybierz folder z rastrami")

# Sprawdź, czy użytkownik wybrał folder
if not input_folder:
    print("Anulowano wybór folderu z rastrami.")
else:
    # Wybierz ścieżkę do zapisu pliku CSV
    output_csv = filedialog.asksaveasfilename(
        title="Wybierz miejsce zapisu pliku CSV",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    # Sprawdź, czy użytkownik wybrał miejsce zapisu
    if not output_csv:
        print("Anulowano wybór miejsca zapisu pliku CSV.")
    else:
        # Wywołaj funkcję przetwarzania z wybranymi ścieżkami
        calculate_raster_statistics(input_folder, output_csv)
