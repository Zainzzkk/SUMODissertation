import os

import pandas as pd
import traci
import json


def write_credit_to_json(data, filename="credits.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def write_policy_to_json(data, filename="policy.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def starting_credits(vehicles):
    vehicle_list = list(vehicles)
    credit_data = {}

    filesize = os.path.getsize("credits.json")
    if filesize == 2:
        for car in range(0, len(vehicle_list)):
            credit_data[str(vehicle_list[car])] = int(30)

        write_credit_to_json(credit_data)

    df = pd.read_json('credits.json', typ='series')
    return df


def starting_policy(vehicles):
    vehicle_list = list(vehicles)
    policy_data = {}

    for car in range(0, len(vehicle_list)):
        policy_data[str(vehicle_list[car])] = "normal"

    write_policy_to_json(policy_data)

    df = pd.read_json('policy.json', typ='series')
    return df
