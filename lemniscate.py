import math
from rotation import cis_alpha, R
from mavsdk.mission import MissionItem
import conversion


def lemniscate_shape(central_coordinate, distance, alpha, coordinate):

    steps = 50
    c_lat = central_coordinate[0]
    c_lon = central_coordinate[1]
    mission_items = []
    a = (distance / 4 * 3) * 2
    initial_angle = -math.radians(30)


    for i in range(steps):

        theta = (i / steps) * 2 * math.pi + initial_angle

        if theta >= (7 * math.pi / 4):
            break

        x = a * math.cos(theta)
        y = a * math.sin(theta) * math.cos(theta)

        [new_x, new_y] = cis_alpha(x, y, alpha)

        d_lat = (new_y / R) * 180 / math.pi
        lat = c_lat + d_lat

        d_lon = (new_x /(R * math.cos(math.radians(lat)))) * 180 / math.pi
        lon = c_lon + d_lon

        mission_item = MissionItem(
            latitude_deg=lat,
            longitude_deg=lon,
            relative_altitude_m=20,
            speed_m_s=15,
            is_fly_through=True,
            gimbal_pitch_deg=0.0,
            gimbal_yaw_deg=0.0,
            camera_action=MissionItem.CameraAction.NONE,
            loiter_time_s=0.0,
            camera_photo_interval_s=0.0,
            acceptance_radius_m=4.0,
            yaw_deg=float('nan'),
            camera_photo_distance_m=0.0,
            vehicle_action=MissionItem.VehicleAction.NONE
        )


        mission_items.append(mission_item)

    mission_items.extend(mission_items)

    land_mission = landing_pattern(central_coordinate, [lat, lon], coordinate, alpha)

    mission_items.extend(land_mission)


    return mission_items

def landing_pattern(central_coordinate, current_position, takeoff_position, alpha):

    points = []
    mission_items = []

    [x1, y1] = conversion.conversion_to_cart(current_position, central_coordinate, alpha)
    [t1, t2] = conversion.conversion_to_cart(takeoff_position, central_coordinate, alpha)
    
    x = x1
    y = y1 - 60
    alt = 20
    speed = 15.0
    j = 0
    i = x
    while(True):
        alt = alt - 1.5
        i = i - 20
        speed = speed - 1.5
        points.append((i, y, alt, speed))
        j = j + 1
        if alt <= 5:
            break
       

    for i in range(j - 1):
        [lat, lon] = conversion.conversion_to_GPS(points[i], central_coordinate, alpha)
        speed = points[i][3]
        alt = points[i][2]
        mission_items.append(
            MissionItem(
                latitude_deg=lat,
                longitude_deg=lon,
                relative_altitude_m=alt,
                speed_m_s=speed,
                is_fly_through=True,
                gimbal_pitch_deg=0.0,
                gimbal_yaw_deg=0.0,
                camera_action=MissionItem.CameraAction.NONE,
                loiter_time_s=0.0,
                camera_photo_interval_s=0.0,
                acceptance_radius_m=4.0,
                yaw_deg=float('nan'),
                camera_photo_distance_m=0.0,
                vehicle_action=MissionItem.VehicleAction.NONE
            )
        )
    [lat, lon] = conversion.conversion_to_GPS(points[-1], central_coordinate, alpha)
    speed = points[-1][3]
    alt = points[-1][2]
    mission_items.append(
        MissionItem(
            latitude_deg=lat,
            longitude_deg=lon,
            relative_altitude_m=alt,
            speed_m_s=speed,
            is_fly_through=True,
            gimbal_pitch_deg=0.0,
            gimbal_yaw_deg=0.0,
            camera_action=MissionItem.CameraAction.NONE,
            loiter_time_s=0.0,
            camera_photo_interval_s=0.0,
            acceptance_radius_m=4.0,
            yaw_deg=float('nan'),
            camera_photo_distance_m=0.0,
            vehicle_action=MissionItem.VehicleAction.LAND
        )
    )
    
    
    
    return mission_items
