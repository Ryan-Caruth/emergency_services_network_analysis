import shapefiles

clip_dictionary = {"INPUT": shapefiles.alberta_shp,
                   "OVERLAY": shapefiles.city_boundary_shp,
                   "OUTPUT": shapefiles.clipped_to_calgary
                   }

join_dictionary = {"INPUT": shapefiles.addresses_shp,
                   "JOIN": shapefiles.clipped_to_calgary,
                   "PREDICATE": [5],
                   "JOIN_FIELDS": ["cfsauid"],
                   "OUTPUT": shapefiles.addresses_within_fsa
                   }
