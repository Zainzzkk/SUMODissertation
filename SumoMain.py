import os
import sys
import time

import traci.constants as tc

from CreditPolicy import CreditSystem
from FirstToReach import DistanceFromJunctionNoPolicy

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci.constants

sumoCmd = ["sumo-gui", "-c", "sumomain.sumo.cfg", "--start"]
traci.start(sumoCmd)

print("Starting SUMO")
traci.gui.setSchema("View #0", "real world")

# loads vehicles loaded into simulation
vehicles = traci.simulation.getLoadedIDList()
df = CreditSystem.read_reputation()
print(df)


for veh in range(0, len(vehicles)):
    # subscribes to check for neighbours 60m away
    traci.vehicle.subscribeContext(vehicles[veh], tc.CMD_GET_VEHICLE_VARIABLE, 100, [tc.VAR_SPEED])

j = 0

while j < 80:
    # this runs one simulation step
    time.sleep(0.2)
    traci.simulationStep()
    vehicles = traci.vehicle.getIDList()
    # df = CreditPolicy.credit_policy(vehicles, df)
    # RandomPolicy.random_policy(vehicles)
    DistanceFromJunctionNoPolicy.Distance(vehicles)
    j = j + 1

traci.close()
