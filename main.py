import self as self
from qgis.utils import iface

import shapefiles
import utils
# Import instance of QGIS project
from qgis.core import QgsProject, QgsVectorLayer, QgsPoint
# import the analysis module from qgis
from qgis.analysis import *

# Create a variable for containing the project instance
# get a reference to the project instance
project = QgsProject.instance()


# Select the feature you want to extract the coordinates from


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
        self.iface.addVectorLayer(shapefiles.clipped_to_calgary, "municipality", "ogr")

    def load_joined_layer(self):
        self.iface.addVectorLayer(shapefiles.addresses_within_fsa, "Addresses within FSA", "ogr")

    def load_new_addresses(self):
        self.iface.addVectorLayer(shapefiles.addresses_without_null, "address_for_network", "ogr")

    # def load_network_analysis(self):
        # self.iface.addVectorLayer(shapefiles.network_test, "address to station", "ogr")


class GeoProcessing:

    def __init__(self, processing):
        self.processing = processing

    def clip_processing(self):
        self.processing.run("native:clip", utils.clip_dictionary)

    def join_by_location(self):
        self.processing.run("native:joinattributesbylocation", utils.join_dictionary)

    def get_coordinates(self):
        address = project.mapLayersByName("testing_addresses")[0]
        # Retrieve the data provider of the selected feature
        # Get all the attributes of the feature
        features = address.getFeatures()
        fire_station = project.mapLayersByName("testing_fire_stations")[0]
        fire_location = fire_station.getFeatures()
        output_layers = []
        for fire_station_feature in fire_location:
            print('fire_stations')
            # fetch geometry
            #    show some information about the feature geometry
            fire_station_geometry = fire_station_feature.geometry().asPoint()
            fire_station_x, fire_station_y = fire_station_geometry.x(), fire_station_geometry.y()
            for address_feature in features:
                print('addresses')
                # fetch geometry
                address_geometry = address_feature.geometry().asPoint()
                address_x, address_y = address_geometry.x(), address_geometry.y()
                #    show some information about the feature geometry
                params = {
                            'INPUT': '../../Documents/programming/data_for_good/calgary_emergency_response_times/data/calgary'
                                     '-roads/roads.shp',
                            'STRATEGY': 0,
                            'START_POINT': f"{address_x},{address_y}",
                            'END_POINT': f'{fire_station_x},{fire_station_y}',
                            'OUTPUT': 'memory: network_analysis'
                        }
                result = self.processing.run("native:shortestpathpointtopoint", params)
                output_layers.append(result['OUTPUT'])

                print('Output_layer is:', output_layers)

                merged_layer = self.processing.run("qgis:mergevectorlayers", {
                            'LAYERS': output_layers,
                            'CRS': output_layers[0].crs().authid(),
                            # set the CRS of the output layer to the same as the input layers
                            'OUTPUT': "memory: network_analysis"
                })['OUTPUT']

                print('merge is:', merged_layer.featureCount())

        QgsProject.instance().addMapLayer(merged_layer, True)


def remove_vector_layers():
    removed_layers = ['alberta', 'calgary_boundary']
    for layer in project.mapLayers().values():
        if layer.name() in removed_layers:
            project.removeMapLayer(layer)


def remove_addresses_layer():
    removed_layers = ['calgary_addresses']
    for layer in project.mapLayers().values():
        if layer.name() in removed_layers:
            project.removeMapLayer(layer)


# def rearrange():
# layer = iface.activeLayer()
# if layer is not None:
# root = project.layerTreeRoot()
# root.setHasCustomLayerOrder(True)
# order = root.customLayerOrder()
# if layer in order:
# order.insert(5, order.pop(order.index(layer)))
# root.setCustomLayerOrder(order)
# else:
# print("Layer not found in layer order")
# else:
# print("No active layer selected")


remove_vector_layers()
remove_addresses_layer()
# rearrange()
