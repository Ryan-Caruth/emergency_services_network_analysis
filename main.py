import shapefiles
import utils
# Import instance of QGIS project
from qgis.core import *

# Create a variable for containing the project instance
# get a reference to the project instance
project = QgsProject.instance()


class LoadSHP:

    def __init__(self, iface):
        self.iface = iface

    def load_layer(self):
        self.iface.addVectorLayer(shapefiles.alberta_shp, 'alberta', 'ogr')
        self.iface.addVectorLayer(shapefiles.city_boundary_shp, 'calgary_boundary', 'ogr')

    def load_clipped_layer(self):
        self.iface.addVectorLayer(shapefiles.clipped_to_calgary, "Calgary", "ogr")


class GeoProcessing:

    def __init__(self, processing):
        self.processing = processing

    def clip_processing(self):
        self.processing.run("native:clip", utils.clip_dictionary)


def remove_vector_layers():
    removed_layers = ['alberta', 'calgary_boundary']
    for layer in project.mapLayers().values():
        if layer in removed_layers:
            project.removeMapLayer(layer)





