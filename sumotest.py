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

j = 0

while j < 80:
    # this runs one simulation step
    time.sleep(0.2)
    traci.simulationStep()

    vehicles = traci.vehicle.getIDList()

    neighbour = []

    for car in range(0, len(vehicles)):
        neighbours = traci.vehicle.getContextSubscriptionResults(vehicles[car])

        if neighbours:
            neighbourcar = list(neighbours)
            for i in range(0, len(neighbourcar)):
                if len(neighbourcar) != 0:
                    currentEdge = traci.vehicle.getRoadID(vehicles[car])
                    if (traci.vehicle.getRoadID(neighbourcar[i]) != currentEdge) and (neighbourcar[i] != vehicles[car]):
                        if neighbourcar[i] not in neighbour:
                            neighbour.append(neighbourcar[i])

        if (traci.lane.getLength("left2middle_0") - 10) == traci.vehicle.getDistance(vehicles[car]):
            if len(neighbour) == 0:
                currentEdge = traci.vehicle.getRoadID(vehicles[car])
                fullCurrentEdge = currentEdge + "_0"
                distance = traci.lane.getLength(fullCurrentEdge)
                try:
                    traci.vehicle.setStop(vehicles[car], traci.vehicle.getRoadID(vehicles[car]), distance, 0,
                                          0, 0)
                except traci.exceptions.TraCIException:
                    pass

    j = j + 1

traci.close()
