import os
import sys
import time

import traci.constants as tc

from Credits import CreditSystem, CreditPolicy
from FirstToReach import DistanceFromJunctionNoPolicy
from Random import RandomPolicy
import Graphs

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci.constants

sumoCmd = ["sumo-gui", "-c", "SUMOFiles/sumomain.sumo.cfg", "--start"]
traci.start(sumoCmd)

print("Starting SUMO")
traci.gui.setSchema("View #0", "real world")

# loads vehicles loaded into simulation
vehicles = traci.simulation.getLoadedIDList()
df = CreditSystem.read_reputation()

iii = traci.simulation.getLoadedIDList()


for veh in range(0, len(vehicles)):
    # subscribes to check for neighbours 60m away
    traci.vehicle.subscribeContext(vehicles[veh], tc.CMD_GET_VEHICLE_VARIABLE, 100, [tc.VAR_SPEED])

j = 0

while j < 300:
    # this runs one simulation step
    time.sleep(0.2)
    traci.simulationStep()
    vehicles = traci.vehicle.getIDList()
    # df = CreditPolicy.credit_policy(vehicles, df)
    # RandomPolicy.random_policy(vehicles)
    # DistanceFromJunctionNoPolicy.Distance(vehicles)
    Graphs.sim_time()
    j = j + 1


traci.close()

# for car in range(0, len(iii)):
#     car_rep = iii[car] + ".reputation"
#     car_policy = iii[car] + ".policy"
#     car_credits = iii[car] + ".credits"
#     print(iii[car])
#     print(df[car_rep][0])
#     print(df[car_policy][0])
#     print(df[car_credits][0])
