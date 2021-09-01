import traci
import pandas as pd
from random import randrange

import CreditPolicy
import Reputation
import Credit
import VehicleControls


def generous_go(data):
    highest_rep = []
    highest_credit = []

    if len(CreditPolicy.generous_list) == 1:
        VehicleControls.remove_stop(CreditPolicy.generous_list, highest_rep)
        return data

    while CreditPolicy.generous_list():
        highest_rep = Reputation.check_highest_reputation(CreditPolicy.generous_list, data)
        if len(highest_rep) > 1:
            highest_credit = Credit.check_highest_credit(CreditPolicy.generous_list, data)
            if len(highest_credit) > 1:
                VehicleControls.random_go(highest_credit, CreditPolicy.generous_list)
            else:
                highest_credit = VehicleControls.remove_stop(highest_credit, CreditPolicy.generous_list)
        else:
            highest_rep = VehicleControls.remove_stop(highest_rep, CreditPolicy.generous_list)

    return data
