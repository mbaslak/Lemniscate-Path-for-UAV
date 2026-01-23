import asyncio
import cmath
import math
from mavsdk import System

R = 6371000 # The radius of the World.

async def indicate_deflaction_angle(drone):

    try:
        print("The deflection angle is being detected...")
        async for heading in drone.telemetry.heading():
            degree = heading.heading_deg
            print(f"The deflection angle : {degree}")
            return math.radians(degree)
    
    except:
        print("The deflection angle could not be detected.")
        return False
    
def define_center_and_angle(coordinate, degree):

    theta = degree

    if degree < math.radians(90):
        degree = math.radians(90) - degree
        d_lat = 150 * math.sin(theta) / R * 180 / math.pi
        d_lon = 150 * math.cos(theta) / (R * math.cos(math.radians(coordinate[0]))) * 180 / math.pi
        lat = coordinate[0] + d_lat
        lon = coordinate[1] - d_lon
    
    elif degree >= math.radians(90) and degree < math.radians(180) :
        degree = math.radians(450) - degree
        theta = math.radians(180) - theta
        d_lat = 150 * math.sin(theta) / R * 180 / math.pi
        d_lon = 150 * math.cos(theta) / (R * math.cos(math.radians(coordinate[0]))) * 180 / math.pi
        lat = coordinate[0] + d_lat
        lon = coordinate[1] + d_lon
    
    elif degree >= math.radians(180) and degree < math.radians(270) :
        degree = math.radians(450) - degree
        theta = theta - math.radians(180)
        d_lat = 150 * math.sin(theta) / R * 180 / math.pi
        d_lon = 150 * math.cos(theta) / (R * math.cos(math.radians(coordinate[0]))) * 180 / math.pi
        lat = coordinate[0] - d_lat
        lon = coordinate[1] + d_lon
    
    elif degree >= math.radians(270) and degree < math.radians(360) :
        degree = math.radians(450) - degree
        theta = math.radians(360) - theta
        d_lat = 150 * math.sin(theta) / R * 180 / math.pi
        d_lon = 150 * math.cos(theta) / (R * math.cos(math.radians(coordinate[0]))) * 180 / math.pi
        lat = coordinate[0] - d_lat
        lon = coordinate[1] - d_lon

    return [lat, lon, degree]

def cis_alpha(x, y, theta):

    comp = complex(x, y) * complex(math.cos(theta), math.sin(theta))

    x = comp.real
    y = comp.imag

    return [x, y]