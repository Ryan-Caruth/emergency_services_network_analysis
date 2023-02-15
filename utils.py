import shapefiles

clip_dictionary = {"INPUT": shapefiles.alberta_shp,
                   "OVERLAY": shapefiles.city_boundary_shp,
                   "OUTPUT": shapefiles.clipped_to_calgary
                   }

