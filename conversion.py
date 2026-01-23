from rotation import cis_alpha, R
import math

def conversion_to_GPS(point, central_coordinate, alpha):

    pt = []
    pt_gps = []

    pt = cis_alpha(point[0], point[1], alpha)

    clat = central_coordinate[0]
    clon = central_coordinate[1]

    x = pt[0]
    y = pt[1]

    lat = y / R * 180 / math.pi + clat
    lon = x / (R * math.cos(math.radians(lat))) * 180 / math.pi + clon

    pt_gps.append(lat)
    pt_gps.append(lon)

    return pt_gps

def conversion_to_cart(point, central_coordinate, alpha):

    lat = point[0]
    lon = point[1]

    new_coordinate = []

    clat = central_coordinate[0]
    clon = central_coordinate[1]

    y = (lat - clat) * R * math.pi / 180
    x = (lon - clon) * R * math.cos(math.radians(lat)) * math.pi / 180

    new_coordinate = cis_alpha(x, y, 2 * math.pi - alpha)

    return new_coordinate