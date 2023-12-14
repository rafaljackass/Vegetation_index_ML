from osgeo import gdal
import numpy as np
import tkinter as tk
from tkinter import filedialog
import time

def calculate_ndvi(input_image, output_ndvi):
    # Zarejestruj czas początkowy
    start_time = time.time()

    # Otwórz obraz za pomocą GDAL
    input_ds = gdal.Open(input_image)

    # Odczytaj dane jako tablice numpy
    image_array = input_ds.ReadAsArray().astype(np.float32)

    # Zabezpiecz przed dzieleniem przez zero
    np.seterr(divide='ignore', invalid='ignore')

    # Odczytaj kanaly
    nir_array = image_array[0, :, :]
    red_array = image_array[1, :, :]

    # Oblicz NDVI
    ndvi_array = (nir_array - red_array) / (nir_array + red_array)

    # Ustaw NaN dla pikseli, gdzie mianownik jest równy zero
    ndvi_array[np.isnan(ndvi_array)] = 0

    # Zapisz wynik do nowego pliku
    driver = gdal.GetDriverByName("GTiff")
    ndvi_ds = driver.Create(output_ndvi, input_ds.RasterXSize, input_ds.RasterYSize, 1, gdal.GDT_Float32)
    ndvi_ds.GetRasterBand(1).WriteArray(ndvi_array)

    # Skopiuj informacje o georeferencji z oryginalnego obrazu
    ndvi_ds.SetProjection(input_ds.GetProjection())
    ndvi_ds.SetGeoTransform(input_ds.GetGeoTransform())

    # Zamknij obrazy i wynikowy plik
    input_ds = None
    ndvi_ds = None

    # Zarejestruj czas zakończenia i wydrukuj różnicę
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Czas trwania operacji: {elapsed_time:.2f} sekundy")

# Tworzymy GUI z pomocą tkinter
root = tk.Tk()
root.withdraw()  # Ukrywamy główne okno, ponieważ nie potrzebujemy pełnej aplikacji GUI

while True:
    # Wybierz plik wejściowy
    input_file_path = filedialog.askopenfilename(title="Wybierz plik wejściowy", filetypes=[("TIFF Files", "*.tif")])

    # Sprawdź, czy użytkownik wybrał plik
    if not input_file_path:
        print("Anulowano wybór pliku wejściowego.")
        break  # Zakończ pętlę, jeśli użytkownik anuluje wybór

    # Wybierz plik wyjściowy
    output_file_path = filedialog.asksaveasfilename(title="Wybierz miejsce zapisu pliku", defaultextension=".tif", filetypes=[("TIFF Files", "*.tif")])

    # Sprawdź, czy użytkownik wybrał miejsce zapisu
    if not output_file_path:
        print("Anulowano wybór miejsca zapisu pliku.")
        break  # Zakończ pętlę, jeśli użytkownik anuluje wybór

    # Wywołaj funkcję przetwarzania z wybranymi ścieżkami
    calculate_ndvi(input_file_path, output_file_path)

    # Zapytaj użytkownika, czy chce przeliczyć kolejny plik
    answer = input("Czy chcesz przeliczyć kolejny plik? (tak/nie): ").lower()
    if answer != 'tak':
        break  # Zakończ pętlę, jeśli użytkownik nie chce przeliczać kolejnego pliku
