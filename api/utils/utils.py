import math

def calculate_length(long_start, lat_start, long_end, lat_end):
    """
    Calculates the distance between two points on the surface of the Earth.

    The points are given by their longitude and latitude in degrees.

    The function returns the distance in kilometers.
    """
    R = 6371.0

    lat1 = math.radians(lat_start)
    lon1 = math.radians(long_start)
    lat2 = math.radians(lat_end)
    lon2 = math.radians(long_end)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance
