import traci
import pandas as pd
from random import randrange

import CreditPolicy
import Reputation
import Credit
import VehicleControls


def default_go(data):
    highest_rep = []
    highest_credit = []

    if len(CreditPolicy.default_list) == 1:
        VehicleControls.remove_stop(CreditPolicy.default_list, highest_rep)
        return data
    while CreditPolicy.if_d_stopped():
        highest_rep = Reputation.check_highest_reputation(CreditPolicy.default_list, data)
        if len(highest_rep) > 1:
            highest_credit = Credit.check_highest_credit(CreditPolicy.default_list, data)
            if len(highest_credit) > 1:
                VehicleControls.random_go(highest_credit, CreditPolicy.default_list)
            else:
                highest_credit = VehicleControls.remove_stop(highest_credit, CreditPolicy.default_list)
        else:
            highest_rep = VehicleControls.remove_stop(highest_rep, CreditPolicy.default_list)

    return data
