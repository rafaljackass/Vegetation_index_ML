from osgeo import gdal
import numpy as np

def calculate_ndvi(nir_band, red_band, output_ndvi):
    # Otwórz obrazy za pomocą GDAL
    nir_ds = gdal.Open(nir_band)
    red_ds = gdal.Open(red_band)

    # Odczytaj dane jako tablice numpy
    nir_array = nir_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)
    red_array = red_ds.GetRasterBand(1).ReadAsArray().astype(np.float32)

    # Zabezpiecz przed dzieleniem przez zero
    np.seterr(divide='ignore', invalid='ignore')

    # Oblicz NDVI
    ndvi_array = (nir_array - red_array) / (nir_array + red_array)

    # Ustaw NaN dla pikseli, gdzie mianownik jest równy zero
    ndvi_array[np.isnan(ndvi_array)] = 0

    # Zapisz wynik do nowego pliku
    driver = gdal.GetDriverByName("GTiff")
    ndvi_ds = driver.Create(output_ndvi, nir_ds.RasterXSize, nir_ds.RasterYSize, 1, gdal.GDT_Float32)
    ndvi_ds.GetRasterBand(1).WriteArray(ndvi_array)

    # Skopiuj informacje o georeferencji z jednego z obrazów (w tym przypadku z NIR)
    ndvi_ds.SetProjection(nir_ds.GetProjection())
    ndvi_ds.SetGeoTransform(nir_ds.GetGeoTransform())

    # Zamknij obrazy i wynikowy plik
    nir_ds = None
    red_ds = None
    ndvi_ds = None

# Przykładowe użycie
calculate_ndvi("sciezka/do/nir/bandu.tif", "sciezka/do/czerwonego/bandu.tif", "sciezka/do/wynikowego/ndvi.tif")
