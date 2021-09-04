import traci
import pandas as pd


def check_highest_credit(vehicles, data):
    highest_credit_value = []
    highest_credit = []

    for car in range(0, len(vehicles)):
        car_rep = vehicles[car] + ".credits"
        # adds each credit value to list
        highest_credit_value.append(data[car_rep][0])

    # checks for highest credit value
    max_credit = max(highest_credit_value)

    # goes through policy list
    for car in range(0, len(vehicles)):
        car_rep = vehicles[car] + ".credits"
        # if == to max credit then add to list
        if data[car_rep][0] == max_credit:
            highest_credit.append(vehicles[car])

    return highest_credit
