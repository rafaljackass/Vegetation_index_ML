
import os
from osgeo import gdal
from osgeo import ogr
import pyproj


path_wektor = 'D:/input/sosna_54_BMSW_A_test.shp'
path_raster = 'D:/LZD/Rastry/3_ORTOFOTOMAPA_CIR/N_33_131_A_c_2_4.tif'


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
    out_file = 'D:/Output/so_54_A/{}.tif'.format(name)
    gdal.Warp(out_file, path_raster, options=warp_options)