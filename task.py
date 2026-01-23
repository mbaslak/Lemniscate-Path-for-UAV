import asyncio
from mavsdk import System
import control
from mavsdk.mission import MissionPlan, MissionItem


async def uploading_task(drone, mission_items):

    try:
        mission_plan = MissionPlan(mission_items)
        await drone.mission.set_return_to_launch_after_mission(False)
        print("The mission is being uploaded...")

        try:
            await drone.mission.upload_mission(mission_plan)
            print("The mission has been uploaded.")
            await asyncio.sleep(50)
            print("Remaining about 50 seconds for the start of the mission.")
            return True
            
        except Exception as error:
            print(f"The mission could not be uploaded. {error}")
            return False
    
    except:
        print("An issue has occured. The mission is aborted.")
        return False
    
   
    
async def starting_task(drone, mission_items):
    try:
        is_convenient = await control.health(drone)
        if not is_convenient:
            print("The mission cannot be started.")
            return [False, "disarm"]
        
    except:
        print("The health cannot be checked.")
        print("The mission cannot be started.")
        return [False, "disarm"]
    
    try:
        print("The mission is being started...")

        await drone.action.arm()
        print("The drone is armed.")

        await drone.mission.start_mission()
        print("The mission has started.")

        return [True, "arm"]

    except:
        print("A problem has emerged during the starting of the mission")
        return [False, "arm"]
    
    

async def progress_task(drone):    
    try:
        print("Mission Progress:")
        async for progress in drone.mission.mission_progress():
            print(f"{progress.current / progress.total}")
            if progress.current == progress.total:
                print("Mission has completed.")
                return True
    
    except:
        print("The mission progress has a problem.")
        return False

        
