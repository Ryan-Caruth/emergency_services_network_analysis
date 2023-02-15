

class LoadSHP:

    def __init__(self, iface):
        self.iface = iface

    def load_layer(self):
        self.iface.addVectorLayer('C:/Users/Ryan/Documents/programming/data_for_good/calgary_emergency_response_times'
                                  '/data/postal_codes/alberta.shp', 'alberta', 'ogr')

    