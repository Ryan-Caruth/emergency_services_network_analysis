

class LoadSHP:

    def __init__(self, iface):
        self.iface = iface

    def load_layer(self):
        self.iface.addVectorLayer('/data/postal_codes/alberta.shp', 'alberta', 'ogr')


# def run_script(iface):
#     fs = LoadSHP(iface)
#     fs.load_layer()
    