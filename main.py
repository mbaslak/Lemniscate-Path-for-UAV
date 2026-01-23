import rotation
import conversion
import task
import control
import lemniscate
from mavsdk import System
import asyncio


# Research FAIL-SAFE mode.

async def return_home(drone):

    try:
        print("The drone is going to launch...")
        await drone.action.return_to_launch()
        return True

    except Exception as error:
        print(f"The drone does not return to launch {error}.")
        drone_disarm(drone)
        
        
        
async def drone_disarm(drone):

    try:
        print("Disarm is starting...")
        await drone.action.disarm()
    except:
        print("The disarming process is unsuccessful.")
        print("Manual intervention is required.")
    
    exit()

async def main_run():


    drone = System()

    value = await control.Connection_UAV(drone)
    if not value:
        print("The program is being closed...")
        exit()

    alpha = await rotation.indicate_deflaction_angle(drone)
    if alpha == False:
        print("The program is being closed...")
        exit()

    coordinate = await control.available_position(drone)
    if coordinate == False:
        print("The program is being closed...")
        exit()

    [lat, lon, alpha] = rotation.define_center_and_angle(coordinate, alpha)

    mission_items = lemniscate.lemniscate_shape([lat, lon], 100, alpha, coordinate)

    value = await task.uploading_task(drone, mission_items)
    if value == False:
        print("The program is being closed...")
        exit()

    values = await task.starting_task(drone, mission_items)
    if values[0] == False:
        if value[1] == "arm":
            await drone_disarm(drone)
        elif value[1] == "disarm":
            print("The program is being closed...")
            exit()

    value = await task.progress_task(drone)
    if value == False:
        await return_home(drone)
        await drone_disarm(drone)
    

if __name__ == "__main__":

    asyncio.run(main_run())