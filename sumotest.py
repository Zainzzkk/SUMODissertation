import os, sys
import time
import traci.constants as tc
from random import randrange

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci
import traci.constants

sumoCmd = ["sumo-gui", "-c", "sumotest.sumo.cfg", "--start"]
traci.start(sumoCmd)

print("Starting SUMO")
traci.gui.setSchema("View #0", "real world")

vehicles = traci.simulation.getLoadedIDList()
for veh in range(0, len(vehicles)):
    traci.vehicle.subscribeContext(vehicles[veh], tc.CMD_GET_VEHICLE_VARIABLE, 100, [tc.VAR_SPEED])


# def random_go(vehicle):
#     for k in range(0, len(vehicle)):
#         if traci.vehicle.getSpeed(vehicle[k]) == 0:
#             togo = randrange(0, len(vehicle))
#             traci.vehicle.setSpeed(vehicle[togo], -1)

def random_go(vehicle):
    togo = randrange(0, len(vehicle))
    if traci.vehicle.getStopState(vehicle[togo]) == 1:
        traci.vehicle.resume(vehicle[togo])


j = 0

while j < 80:
    # this runs one simulation step
    time.sleep(0.25)
    traci.simulationStep()

    vehicles = traci.vehicle.getIDList()
    for car in range(0, len(vehicles)):
        neighbours = traci.vehicle.getContextSubscriptionResults(vehicles[car])

        if neighbours:
            neighbourcar = list(neighbours)
            for i in range(0, len(neighbourcar)):
                currentEdge = traci.vehicle.getRoadID(vehicles[car])
                if traci.vehicle.getRoadID(neighbourcar[i]) != currentEdge:
                    currentEdge = traci.vehicle.getRoadID(vehicles[car])
                    fullCurrentEdge = currentEdge + "_0"
                    distance = traci.lane.getLength(fullCurrentEdge)
                    if traci.vehicle.getDistance(vehicles[car]) < distance:
                        try:
                            traci.vehicle.setStop(vehicles[car], traci.vehicle.getRoadID(vehicles[car]), distance, 0,
                                                  10, 0)
                        except traci.exceptions.TraCIException:
                            pass
            random_go(neighbourcar)

    j = j + 1

traci.close()
