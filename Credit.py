import traci
import pandas as pd


def check_highest_credit(vehicles, data):
    highest_credit_value = []
    highest_credit = []

    for car in range(0, len(vehicles)):
        car_rep = vehicles + ".credits"
        highest_credit_value.append(data[car_rep][0])

    max_credit = max(highest_credit_value)

    for car in range(0, len(vehicles)):
        car_rep = vehicles[car] + ".credits"
        if data[car_rep][0] == max_credit:
            highest_credit.append(vehicles)

    return highest_credit
