shapefile_path = '../../data/postal_codes/alberta.shp'


class LoadSHP:

    def __init__(self, iface):
        self.iface = iface

    def load_layer(self):
        self.iface.addVectorLayer(shapefile_path, 'alberta', 'ogr')
