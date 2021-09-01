import traci
import pandas as pd


def check_highest_reputation(vehicles, data):
    # stores highest rep values
    highest_rep_value = []
    # stores cars with highest rep
    highest_rep = []
    for car in range(0, len(vehicles)):
        car_rep = vehicles[car] + ".reputation"
        highest_rep_value.append(data[car_rep][0])

    max_rep = max(highest_rep_value)

    for car in range(0, len(vehicles)):
        car_rep = vehicles[car] + ".reputation"
        if data[car_rep][0] == max_rep:
            highest_rep.append(vehicles)

    return highest_rep
