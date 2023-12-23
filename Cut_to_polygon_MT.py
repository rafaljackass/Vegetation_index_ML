import os
from osgeo import gdal, ogr
import tkinter as tk
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor
import pyproj
import time

import os
from osgeo import gdal, ogr
import tkinter as tk
from tkinter import filedialog
from concurrent.futures import ThreadPoolExecutor
import pyproj
import time

def crop_raster_for_feature(feature, input_raster, output_dir, attribute_column, input_vector):
    # Pobierz wartość z wybranej kolumny tabeli atrybutów
    name = feature.GetField(attribute_column)

    # Utwórz warunek przycinania
    geom = feature.GetGeometryRef()
    envelope = geom.GetEnvelope()
    xmin, xmax, ymin, ymax = envelope

    # Utwórz nazwę pliku wyjściowego na podstawie wartości z tabeli atrybutów
    output_file = os.path.join(output_dir, f"{name}.tif")

    # Utwórz opcje przycinania
    warp_options = gdal.WarpOptions(
        outputBounds=[xmin, ymin, xmax, ymax],
        cutlineDSName=input_vector,
        cutlineWhere=f"{attribute_column}='{name}'",
        cropToCutline=True
    )

    # Przycięcie obrazu rastrowego
    gdal.Warp(output_file, input_raster, options=warp_options)

    print(f"Pomyślnie przycięto i zapisano plik dla {name} do {output_file}")


def crop_raster_with_vector(input_vector, input_raster, output_dir, attribute_column):
    # Otwórz warstwę wektorową z wielokątami
    vector_ds = ogr.Open(input_vector)
    layer = vector_ds.GetLayer()

    # Utwórz executor dla wątków
    with ThreadPoolExecutor() as executor:
        # Uruchom funkcję crop_raster_for_feature dla każdego obiektu w warstwie wektorowej
        futures = [executor.submit(crop_raster_for_feature, feature, input_raster, output_dir, attribute_column, input_vector) for feature in layer]

        # Poczekaj na zakończenie wszystkich wątków
        for future in futures:
            future.result()

def main(input_vector, input_raster, output_dir):
    # Mierz czas wykonania
    start_time = time.time()

    # Wybierz kolumnę z tabeli atrybutów
    attribute_column = input("Podaj nazwę kolumny z tabeli atrybutów, którą chcesz użyć do nazw plików wyjściowych: ")

    # Wywołaj funkcję przycinania rastrowego z wybranymi ścieżkami
    crop_raster_with_vector(input_vector, input_raster, output_dir, attribute_column)

    # Oblicz i wydrukuj czas wykonania
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Całkowity czas wykonania: {elapsed_time} sekund")

if __name__ == "__main__":
    # Tworzymy GUI z pomocą tkinter
    root = tk.Tk()
    root.withdraw()  # Ukrywamy główne okno, ponieważ nie potrzebujemy pełnej aplikacji GUI

    # Wybierz plik wektorowy
    input_vector = filedialog.askopenfilename(title="Wybierz plik wektorowy", filetypes=[("Shapefiles", "*.shp")])

    # Sprawdź, czy użytkownik wybrał plik
    if not input_vector:
        print("Anulowano wybór pliku wektorowego.")
    else:
        # Wybierz plik rastrowy
        input_raster = filedialog.askopenfilename(title="Wybierz plik rastrowy", filetypes=[("TIFF Files", "*.tif")])

        # Sprawdź, czy użytkownik wybrał plik
        if not input_raster:
            print("Anulowano wybór pliku rastrowego.")
        else:
            # Wybierz folder do zapisu plików przyciętych
            output_dir = filedialog.askdirectory(title="Wybierz folder do zapisu plików przyciętych")

            # Sprawdź, czy użytkownik wybrał folder
            if not output_dir:
                print("Anulowano wybór folderu do zapisu plików przyciętych.")
            else:
                # Wywołaj funkcję główną
                main(input_vector, input_raster, output_dir)
