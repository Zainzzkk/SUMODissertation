import traci
import pandas as pd
from random import randrange

import Credit
import CreditPolicy
import Reputation
import VehicleControls


def priority_go(data):
    # list for highest reputation cars
    highest_rep = []
    # list for highest credit cars
    highest_credit = []
    # if only 1 car on priority list, then it goes
    if len(CreditPolicy.priority_list) == 1:
        VehicleControls.remove_stop(CreditPolicy.priority_list, highest_rep)
        return data

    # loop checking for next highest until list cleared
    while CreditPolicy.priority_list:
        # checks which car has highest reputation
        highest_rep = Reputation.check_highest_reputation(CreditPolicy.priority_list, data)
        # if more than 1 on same highest rep
        if len(highest_rep) > 1:
            # check for highest credit
            highest_credit = Credit.check_highest_credit(CreditPolicy.priority_list, data)
            # if more than 1 on highest credit
            if len(highest_credit) > 1:
                # random car goes from those with highest
                VehicleControls.random_go(highest_credit, CreditPolicy.priority_list)
            else:
                # else car with highest credit goes first
                highest_credit = VehicleControls.remove_stop(highest_credit, CreditPolicy.priority_list)
        else:
            # or car with highest reputation goes first
            highest_rep = VehicleControls.remove_stop(highest_rep, CreditPolicy.priority_list)

    return data

