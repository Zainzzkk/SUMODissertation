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

j = 0

while j < 80:
    # this runs one simulation step
    time.sleep(0.1)
    traci.simulationStep()

    vehicles = traci.vehicle.getIDList()

    j = j + 1

traci.close()
