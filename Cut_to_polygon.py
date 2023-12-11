
import os
from osgeo import gdal
from osgeo import ogr
import pyproj


path_wektor = 'D:/NN_builder/wektory/sosna_58_BMSW_B.shp'
path_raster = 'D:/NN_builder/raster/N_33_131_A_c_4_1.tif'


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
    out_file = 'D:/NN_builder/output/sosna_58/{}.tif'.format(name)
    gdal.Warp(out_file, path_raster, options=warp_options)