import traci
import pandas as pd
from random import randrange

import Credit
import CreditPolicy
import Reputation


def priority_go(data):
    # list for highest reputation cars
    highest_rep = []
    # list for highest credit cars
    highest_credit = []
    # if only 1 car on priority list, then it goes
    if len(CreditPolicy.priority_list) == 1:
        remove_stop(CreditPolicy.priority_list)
        return data

    # loop checking for next highest until list cleared
    while CreditPolicy.if_p_stopped():
        # checks which car has highest reputation
        highest_rep = Reputation.check_highest_reputation(CreditPolicy.priority_list, data)
        # if more than 1 on same highest rep
        if len(highest_rep) > 1:
            # check for highest credit
            highest_credit = Credit.check_highest_credit(CreditPolicy.priority_list, data)
            # if more than 1 on highest credit
            if len(highest_credit) > 1:
                # random car goes from those with highest
                random_go(highest_credit)
            else:
                # else car with highest credit goes first
                highest_credit = remove_stop(highest_credit)
        else:
            # or car with highest reputation goes first
            highest_rep = remove_stop(highest_rep)

    return data


# def check_highest_reputation(data):
#     # stores highest rep values
#     highest_rep_value = []
#     # stores cars with highest rep
#     highest_rep = []
#     for car in range(0, len(CreditPolicy.priority_list)):
#         car_rep = CreditPolicy.priority_list[car] + ".reputation"
#         highest_rep_value.append(data[car_rep][0])
#
#     max_rep = max(highest_rep_value)
#
#     for car in range(0, len(CreditPolicy.priority_list)):
#         car_rep = CreditPolicy.priority_list[car] + ".reputation"
#         if data[car_rep][0] == max_rep:
#             highest_rep.append(CreditPolicy.priority_list[car])
#
#     return highest_rep


# def check_highest_credit(data):
#     highest_credit_value = []
#     highest_credit = []
#
#     for car in range(0, len(CreditPolicy.priority_list)):
#         car_rep = CreditPolicy.priority_list[car] + ".credits"
#         highest_credit_value.append(data[car_rep][0])
#
#     max_credit = max(highest_credit_value)
#
#     for car in range(0, len(CreditPolicy.priority_list)):
#         car_rep = CreditPolicy.priority_list[car] + ".credits"
#         if data[car_rep][0] == max_credit:
#             highest_credit.append(CreditPolicy.priority_list[car])
#
#     return highest_credit


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
        CreditPolicy.priority_list.remove(vehicle[togo])
