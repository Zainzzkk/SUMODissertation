import os
import sys
import time

import traci.constants as tc

import RandomPolicy

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci.constants

sumoCmd = ["sumo-gui", "-c", "sumotest.sumo.cfg", "--start"]
traci.start(sumoCmd)

print("Starting SUMO")
traci.gui.setSchema("View #0", "real world")

vehicles = traci.simulation.getLoadedIDList()
for veh in range(0, len(vehicles)):
    traci.vehicle.subscribeContext(vehicles[veh], tc.CMD_GET_VEHICLE_VARIABLE, 60, [tc.VAR_SPEED])

j = 0

while j < 80:
    # this runs one simulation step
    time.sleep(0.25)
    traci.simulationStep()
    vehicles = traci.vehicle.getIDList()
    RandomPolicy.random_policy(vehicles)
    j = j + 1

traci.close()
