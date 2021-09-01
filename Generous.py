import traci
import pandas as pd
from random import randrange

import CreditPolicy


def generous_go(data):
    highest_rep = []
    highest_credit = []

    if len(CreditPolicy.generous_list) == 1:
        remove_stop(CreditPolicy.generous_list)
        return data

    while CreditPolicy.if_g_stopped():
        highest_rep = check_highest_reputation(data)
        if len(highest_rep) > 1:
            highest_credit = check_highest_credit(data)
            if len(highest_credit) > 1:
                random_go(highest_credit)
            else:
                highest_credit = remove_stop(highest_credit)
        else:
            highest_rep = remove_stop(highest_rep)

    return data


def check_highest_reputation(data):
    highest_rep_value = []
    highest_rep = []
    for car in range(0, len(CreditPolicy.generous_list)):
        car_rep = CreditPolicy.generous_list[car] + ".reputation"
        highest_rep_value.append(data[car_rep][0])

    max_rep = max(highest_rep_value)

    for car in range(0, len(CreditPolicy.generous_list)):
        car_rep = CreditPolicy.generous_list[car] + ".reputation"
        if data[car_rep][0] == max_rep:
            highest_rep.append(CreditPolicy.generous_list[car])

    return highest_rep


def check_highest_credit(data):
    highest_credit_value = []
    highest_credit = []

    for car in range(0, len(CreditPolicy.generous_list)):
        car_rep = CreditPolicy.generous_list[car] + ".credits"
        highest_credit_value.append(data[car_rep][0])

    max_credit = max(highest_credit_value)

    for car in range(0, len(CreditPolicy.generous_list)):
        car_rep = CreditPolicy.generous_list[car] + ".credits"
        if data[car_rep][0] == max_credit:
            highest_credit.append(CreditPolicy.generous_list[car])

    return highest_credit


def remove_stop(vehicle):
    if traci.vehicle.getStopState(vehicle[0]) == 1:
        traci.vehicle.resume(vehicle[0])
        CreditPolicy.stop_list.remove(vehicle[0])
        vehicle.remove(vehicle[0])

    return vehicle


def random_go(vehicle):
    # generates random number between 0 and cars in vehicle list
    togo = randrange(0, len(vehicle))
    # checks if vehicle at random index is stopped and if stopped then resume
    if traci.vehicle.getStopState(vehicle[togo]) == 1:
        traci.vehicle.resume(vehicle[togo])
        CreditPolicy.stop_list.remove(vehicle[togo])
        CreditPolicy.generous_list.remove(vehicle[togo])
