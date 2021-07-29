import traci
import traci.constants
from random import randrange
import Direction

def random_policy(vehicles):
    for car in range(0, len(vehicles)):
        # generates neighbours to current vehicle within 100m
        neighbours = traci.vehicle.getContextSubscriptionResults(vehicles[car])
        if neighbours:
            # converts to a list
            neighbourcar = list(neighbours)
            Direction.direction_check(neighbourcar)
            random_go(neighbourcar)


def random_go(vehicle):
    togo = randrange(0, len(vehicle))
    if traci.vehicle.getStopState(vehicle[togo]) == 1:
        traci.vehicle.resume(vehicle[togo])

