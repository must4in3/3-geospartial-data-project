import pandas as pd
import numpy as np




def transformToGeoPoint(s):
    if np.isnan(s.lat) or np.isnan(s.lng):
        return None
    return {
        "type":"Point",
        "coordinates":[s.lng, s.lat]
    }


