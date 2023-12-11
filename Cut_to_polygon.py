
import os
from osgeo import gdal
from osgeo import ogr
import pyproj


path_wektor = 'D:/NN_builder/wektory/dab_159_LSW.shp'
path_raster = 'D:/NN_builder/raster/N_33_131_A_c_3_2_NDVI.tif'
output_path = 'D:/NN_builder/output/db_159/'

# Otwórz warstwę wektorową z wielokątami
vector_ds = ogr.Open(path_wektor)
layer = vector_ds.GetLayer()

# Przejdź przez każdy wielokąt
for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)

# Pobierz nazwy z tabeli atrybutów
    name = feature.GetField('id')


    # Utwórz warunek przycinania
    geom = feature.GetGeometryRef()
    envelope = geom.GetEnvelope()
    xmin, xmax, ymin, ymax = envelope
    warp_options = gdal.WarpOptions(outputBounds=[xmin, ymin, xmax, ymax], cutlineDSName=path_wektor,
                                    cutlineWhere="id='{}'".format(name),
                                    cropToCutline=True)

    # Przycięcie obrazu rastrowego
    out_file = 'D:/NN_builder/output/db_159/{}.tif'.format(name)
    gdal.Warp(out_file, path_raster, options=warp_options)