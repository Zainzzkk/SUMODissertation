import traci
import pandas as pd
from random import randrange

import Default
import Direction
import CreditSystem
import DistanceFromJunction
import Generous
import Priority

# list of cars which have to stop
stop_list = []
# list of priority cars
priority_list = []
# list of default cars
default_list = []
# list of generous cars
generous_list = []


# implements credit policy
def credit_policy(vehicles, data):
    # checks who is first and stops rest
    DistanceFromJunction.Distance(vehicles)
    # adds car priority to list
    policy_checker(data)
    # if priority list not empty and if priority cars stopped
    # only want to do these if stopped cars or else wasting resources
    if priority_list and if_p_stopped():
        data = Priority.priority_go(data)
    print(priority_list)
    # if default list not empty and if default cars stopped
    # if default_list and if_d_stopped():
    #     data = Default.default_go(data)
    # # if generous list not empty and if generous cars stopped
    # if generous_list and if_g_stopped():
    #     data = Generous.generous_go(data)
    return data


# checks if any cars in priority list have stopped
def if_p_stopped():
    for car in range(0, len(priority_list)):
        if traci.vehicle.getStopState(priority_list[car]) == 1:
            return True
    return False


# checks if any default cars stopped
def if_d_stopped():
    for car in range(0, len(default_list)):
        if traci.vehicle.getStopState(default_list[car]) == 1:
            return True
    return False


# check if any generous cars have stopped
def if_g_stopped():
    for car in range(0, len(generous_list)):
        if traci.vehicle.getStopState(generous_list[car]) == 1:
            return True
    return False


# checks which cars are which policy
def policy_checker(data):
    # checks which car is priority
    priority_check(data)
    # checks which car is default
    default_check(data)
    # checks which car is generous
    generous_check(data)


def priority_check(data):
    for car in range(0, len(stop_list)):
        # makes string with car reputation in dataframe
        car_rep = stop_list[car] + ".policy"
        # matches if priority for car
        if data[car_rep][0] == "priority":
            # only adds once to list
            if stop_list[car] not in priority_list:
                priority_list.append(stop_list[car])


def default_check(data):
    for car in range(0, len(stop_list)):
        car_rep = stop_list[car] + ".policy"
        # matches if default for car
        if data[car_rep][0] == "default":
            if stop_list[car] not in default_list:
                default_list.append(stop_list[car])


def generous_check(data):
    for car in range(0, len(stop_list)):
        car_rep = stop_list[car] + ".policy"
        # matches if generous for car
        if data[car_rep][0] == "generous":
            if stop_list[car] not in generous_list:
                generous_list.append(stop_list[car])


def random_go(vehicle):
    # generates random number between 0 and cars in vehicle list
    togo = randrange(0, len(vehicle))
    # checks if vehicle at random index is stopped and if stopped then resume
    if traci.vehicle.getStopState(vehicle[togo]) == 1:
        traci.vehicle.resume(vehicle[togo])


