import shapefiles


class LoadSHP:

    def __init__(self, iface):
        self.iface = iface

    def load_layer(self):
        self.iface.addVectorLayer(shapefiles.alberta_shp, 'alberta', 'ogr')
