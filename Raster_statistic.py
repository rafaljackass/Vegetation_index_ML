import rasterio
import pandas as pd
import glob
import numpy as np
import time

# Lista rastrów do przetworzenia
raster_list = glob.glob('D:/NN_builder/output/sosna_58/*.tif')

# Tworzenie pustego dataframe'u do przechowywania wyników
results_df = pd.DataFrame()

# Rozpoczęcie pomiaru czasu
start_time = time.time()

# Pętla przez rastry
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

# Zakończenie pomiaru czasu
end_time = time.time()

# Obliczenie czasu wykonania
execution_time = end_time - start_time

print(f"Czas wykonania: {execution_time} sekund")

# Zapisanie wyników do pliku CSV
results_df.to_csv('D:/NN_builder/output/sosna_58/wyniki_statystyk.csv', index=False)