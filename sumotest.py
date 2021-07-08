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


# def random_go(vehicle):
#     for k in range(0, len(vehicle)):
#         if traci.vehicle.getSpeed(vehicle[k]) == 0:
#             togo = randrange(0, len(vehicle))
#             traci.vehicle.setSpeed(vehicle[togo], -1)

def random_go(vehicle):
    togo = randrange(0, len(vehicle))
    if traci.vehicle.getStopState(vehicle[togo]) == 1:
        traci.vehicle.resume(vehicle[togo])


# print("lanes", traci.lane.getIDList())
# print("length", traci.lane.getLength("middle2left_0"))
# traci.junction.subscribeContext("2", traci.constants.CMD_GET_VEHICLE_VARIABLE, 0.0)
# print("junctions", traci.junction.getIDList())
traci.junction.subscribeContext("2", tc.CMD_GET_VEHICLE_VARIABLE, 60, [tc.VAR_SPEED, tc.VAR_WAITING_TIME])

j = 0

while j < 80:
    # this runs one simulation step
    time.sleep(0.25)
    traci.simulationStep()

    vehicles = traci.vehicle.getIDList()
    # if (j % 2) == 0:  # every 10 sec....

    neighbours = traci.junction.getContextSubscriptionResults("2")

    if neighbours:
        neighbourcar = list(neighbours)
        for i in range(0, len(neighbourcar)):
            currentEdge = traci.vehicle.getRoadID(neighbourcar[i])
            fullCurrentEdge = currentEdge + "_0"
            distance = traci.lane.getLength(fullCurrentEdge)
            #traci.vehicle.setSpeed(neighbourcar[i], 0)
            if traci.vehicle.getDistance(neighbourcar[i]) < distance:
                #traci.vehicle.setSpeed(neighbourcar[i], 0)
                try:
                    traci.vehicle.setStop(vehicles[i], traci.vehicle.getRoadID(vehicles[i]), distance, 0, 10, 0)
                except traci.exceptions.TraCIException:
                    pass
            random_go(neighbourcar)


    # for i in range(0, len(vehicles)):

    # edge that vehicle is on
    # currentEdge = traci.vehicle.getRoadID(vehicles[i])
    # lane has _0 on end
    # fullCurrentEdge = currentEdge + "_0"
    # get distance of edge to stop at
    # distance = traci.lane.getLength(fullCurrentEdge)
    # stop at junction
    # traci.vehicle.setStop(vehicles[i], currentEdge, distance, 0,10,0,10)


    j = j + 1

traci.close()
