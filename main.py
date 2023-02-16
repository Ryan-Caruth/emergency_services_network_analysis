import shapefiles
import utils
# Import instance of QGIS project
from qgis.core import QgsProject

# Create a variable for containing the project instance
# get a reference to the project instance
project = QgsProject.instance()


class LoadSHP:

    def __init__(self, iface):
        self.iface = iface

    def load_layer(self):
        self.iface.addVectorLayer(shapefiles.alberta_shp, 'alberta', 'ogr')
        self.iface.addVectorLayer(shapefiles.city_boundary_shp, 'calgary_boundary', 'ogr')
        self.iface.addVectorLayer(shapefiles.roads_shp, 'calgary_roads', 'ogr')
        self.iface.addVectorLayer(shapefiles.ems_stations_shp, 'calgary_ems_stations', 'ogr')
        self.iface.addVectorLayer(shapefiles.fire_stations_shp, 'calgary_fire_stations', 'ogr')
        self.iface.addVectorLayer(shapefiles.addresses_shp, 'calgary_addresses', 'ogr')

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
        if layer.name() in removed_layers:
            project.removeMapLayer(layer)


def change_layer_order():
    rearrange_layer = project.mapLayersByName("Calgary")[0]
    root_layer = project.layerTreeRoot()
    rearrange_layer_1 = root_layer.findLayer(rearrange_layer.id())
    clone = rearrange_layer_1.clone()
    parent = rearrange_layer_1.parent()
    parent.insertChildNode(5, clone)
    parent.removeChildNode(rearrange_layer_1)


remove_vector_layers()
change_layer_order()



