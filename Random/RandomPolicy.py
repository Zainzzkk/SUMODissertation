import traci
import traci.constants
from random import randrange
from Random import RandomDirection


def random_policy(vehicles):
    for car in range(0, len(vehicles)):
        # generates neighbours to current vehicle within 100m
        neighbours = traci.vehicle.getContextSubscriptionResults(vehicles[car])
        if neighbours:
            # converts to a list
            neighbourcar = list(neighbours)
            # imported direction file checks direction
            RandomDirection.direction_check(neighbourcar)
            # random policy for going
            random_go(neighbourcar)


def random_go(vehicle):
    # generates random number between 0 and cars in vehicle list
    togo = randrange(0, len(vehicle))
    # checks if vehicle at random index is stopped and if stopped then resume
    if traci.vehicle.getStopState(vehicle[togo]) == 1:
        traci.vehicle.resume(vehicle[togo])
