import os
import pandas as pd
import traci
import json
from random import randrange


def read_reputation():
    with open('policy.json') as data_file:
        data = json.load(data_file)

    df = pd.json_normalize(data)
    return df


def random_rep(data, vehicles):
    for car in range(0, len(vehicles)):
        car_policy = vehicles[car] + ".policy"
        random_num = randrange(0, 3)
        if random_num == 0:
            data[car_policy][0] = "priority"
        if random_num == 1:
            data[car_policy][0] = "default"
        if random_num == 2:
            data[car_policy][0] = "generous"


# def write_credit_to_json(data, filename="credits.json"):
#     with open(filename, "w") as f:
#         json.dump(data, f, indent=4)
#
#
# def write_policy_to_json(data, filename="policy.json"):
#     with open(filename, "w") as f:
#         json.dump(data, f, indent=4)


# def starting_credits(vehicles):
#     vehicle_list = list(vehicles)
#     credit_data = {}
#
#     filesize = os.path.getsize("credits.json")
#     if filesize == 2 or filesize == 0:
#         for car in range(0, len(vehicle_list)):
#             credit_data[str(vehicle_list[car])] = int(100)
#
#         write_credit_to_json(credit_data)

#
# def starting_policy(vehicles):
#     vehicle_list = list(vehicles)
#     policy_data = {}
#
#     for car in range(0, len(vehicle_list)):
#         policy_data[str(vehicle_list[car])] = "neutral"
#
#     write_policy_to_json(policy_data)


# def update_credits(credit_policy):
#     write_credit_to_json(credit_policy)
#
#
# def update_policy(veh_policy):
#     write_policy_to_json(veh_policy)
#
#
# def open_credits_file():
#     with open('credits.json') as data_file:
#         data = json.load(data_file)
#
#     return data
