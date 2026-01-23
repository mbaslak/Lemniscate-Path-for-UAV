import asyncio
from mavsdk import System


async def Connection_UAV(drone):

    try:
        print("Drone is being connected...")
        await drone.connect(system_address = "udp://:14540")

    except:
        print("Drone could not be connected.")
        return False
    
    try:
        async for state in drone.core.connection_state():
            if state.is_connected:
                print("Drone has been connected successfully.")
                break
    except:
       print("Drone could not be connected.")
       return False
    
    return True

async def health(drone):

    try:
        for i in range(60):
            async for health in drone.telemetry.health():
                if health.is_global_position_ok and health.is_home_position_ok and health.is_gyrometer_calibration_ok and health.is_accelerometer_calibration_ok:
                    print("Everything is OK for flight")
                    return True
                break
            await asyncio.sleep(1)
        print("The drone health is not convenient (Timeout).")
        return False
    except:
        print("There is no information about drone health.")
        return False

async def available_position(drone):

    position = []

    print("GPS information is expected...")
    
    try:
        for i in  range(60):
            async for gps_info in drone.telemetry.gps_info():
                if gps_info.fix_type.value >= 2:
                    print(f"GPS is fixed. {gps_info.fix_type.value}")
                    flag = 1
                else:
                    flag = 0
                break
            if flag == 1:
                break
            await asyncio.sleep(1)
        if flag == 0:
            print("GPS data is not reliable. (Timeout)")
            return False
    except:
        print("GPS fixing is unsuccessful.")
        return False
    
    try:
        async for post in drone.telemetry.position():
            position.append(post.latitude_deg)
            position.append(post.longitude_deg)
            break
        return position
    except:
        print("GPS info could not be obtained.")
        return False
    
   

    
    
         

