import os
import sys
import time

import traci.constants as tc

from Credits import CreditSystem, CreditPolicy
from FirstToReach import DistanceFromJunctionNoPolicy
from Random import RandomPolicy
import Graphs
import released

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

all_vehicles = traci.simulation.getLoadedIDList()

speed_data, waiting_time, credit = Graphs.create_object(vehicles)

for veh in range(0, len(vehicles)):
    # subscribes to check for neighbours 75m away
    traci.vehicle.subscribeContext(vehicles[veh], tc.CMD_GET_VEHICLE_VARIABLE, 65, [tc.VAR_SPEED])

# CreditSystem.random_rep(df, vehicles)

traci.simulationStep()
df = CreditPolicy.credit_policy(vehicles, df)
# RandomPolicy.random_policy(vehicles)
# DistanceFromJunctionNoPolicy.Distance(vehicles)
speed_data = Graphs.speed_record(speed_data, vehicles)
waiting_time = Graphs.waiting_time(waiting_time, vehicles)
credit = Graphs.credit_track(credit, df, vehicles)
# runs until no cars left in simulation
while traci.vehicle.getIDList():
    # this runs one simulation step
    time.sleep(0.01)
    traci.simulationStep()
    vehicles = traci.vehicle.getIDList()
    df = CreditPolicy.credit_policy(vehicles, df)
    # RandomPolicy.random_policy(vehicles)
    # DistanceFromJunctionNoPolicy.Distance(vehicles)
    speed_data = Graphs.speed_record(speed_data, vehicles)
    waiting_time = Graphs.waiting_time(waiting_time, vehicles)
    credit = Graphs.credit_track(credit, df, vehicles)

traci.close()

print(released.released)

# Graphs.export_speed(speed_data)
# Graphs.export_wait(waiting_time)
# Graphs.export_credits(credit)
