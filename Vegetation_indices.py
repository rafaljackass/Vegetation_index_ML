import os
from osgeo import gdal
import tkinter as tk
from tkinter import filedialog, simpledialog
import numpy as np
import time

def calculate_ndvi(nir_array, red_array):
    return (nir_array - red_array) / (nir_array + red_array)

def calculate_msavi(nir_array, red_array):
    return 0.5 * (2 * nir_array + 1 - np.sqrt((2 * nir_array + 1)**2 - 8 * (nir_array - red_array)))

def calculate_atsavi(nir_array, red_array):
    X = 0.08
    a = 1.22
    b = 0.03

    return (nir_array - a * red_array - b * (nir_array + red_array) + a * b) / (1 + a**2)

def choose_vegetation_index():
    root = tk.Tk()
    root.withdraw()

    index_type = simpledialog.askstring("Typ indeksu", "Podaj typ indeksu (np. NDVI, MSAVI, ATSAVI):").upper()
    root.destroy()
    return index_type

def calculate_vegetation_index(input_image, output_index, index_calculator):
    start_time = time.time()

    input_ds = gdal.Open(input_image)
    image_array = input_ds.ReadAsArray().astype(np.float32)

    np.seterr(divide='ignore', invalid='ignore')

    nir_array = image_array[0, :, :]
    red_array = image_array[1, :, :]

    index_array = index_calculator(nir_array, red_array)
    index_array[np.isnan(index_array)] = 0

    driver = gdal.GetDriverByName("GTiff")
    index_ds = driver.Create(output_index, input_ds.RasterXSize, input_ds.RasterYSize, 1, gdal.GDT_Float32)
    index_ds.GetRasterBand(1).WriteArray(index_array)

    index_ds.SetProjection(input_ds.GetProjection())
    index_ds.SetGeoTransform(input_ds.GetGeoTransform())

    input_ds = None
    index_ds = None

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Czas trwania operacji: {elapsed_time:.2f} sekundy")

def main():
    input_image = filedialog.askopenfilename(title="Wybierz plik wejściowy", filetypes=[("TIFF Files", "*.tif")])

    if not input_image:
        print("Anulowano wybór pliku wejściowego.")
        return

    output_index = filedialog.asksaveasfilename(title="Zapisz wynikowy plik", defaultextension=".tif", filetypes=[("TIFF Files", "*.tif")])

    if not output_index:
        print("Anulowano wybór pliku wynikowego.")
        return

    index_type = choose_vegetation_index()

    if not index_type:
        print("Anulowano wybór typu indeksu.")
        return

    if index_type == 'NDVI':
        index_calculator = calculate_ndvi
    elif index_type == 'MSAVI':
        index_calculator = calculate_msavi
    elif index_type == 'ATSAVI':
        index_calculator = calculate_atsavi
    else:
        print("Nieobsługiwany typ indeksu wegetacji.")
        return

    calculate_vegetation_index(input_image, output_index, index_calculator)

if __name__ == "__main__":
    main()

