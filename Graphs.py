import traci
import json
import pandas as pd


def create_object(vehicles):
    speed = {}
    waiting = {}
    credit = {}
    for car in range(0, len(vehicles)):
        waiting[vehicles[car]] = {}
        credit[vehicles[car]] = {}
        speed[vehicles[car]] = []

    return speed, waiting, credit


def speed_record(speed_data, vehicles):
    for car in range(0, len(vehicles)):
        speed_data[vehicles[car]].append(traci.vehicle.getSpeed(vehicles[car]))

    return speed_data


def export_speed(speed_data):
    with open('./PolicyRecording/CreditPolicyAllPriority1Speed75m.json', 'w', encoding='utf-8') as f:
        json.dump(speed_data, f, ensure_ascii=False, indent=4)


def export_wait(wait_time):
    with open('./PolicyRecording/CreditPolicyAllPriority1wait75m.json', 'w', encoding='utf-8') as f:
        json.dump(wait_time, f, ensure_ascii=False, indent=4)


def export_credits(credit):
    with open('./PolicyRecording/CreditPolicyAllPriority1Credits75m.json', 'w') as f:
        json.dump(credit, f, indent=4)


def waiting_time(wait_time, vehicles):
    for car in range(0, len(vehicles)):
        wait_time[vehicles[car]][traci.simulation.getTime()] = traci.vehicle.getStopState(vehicles[car])

    return wait_time


def credit_track(credit, data, vehicles):
    for car in range(0, len(vehicles)):
        credit = time_init(credit, vehicles[car])
        car_pol = vehicles[car] + ".policy"
        car_rep = vehicles[car] + ".reputation"
        car_cred = vehicles[car] + ".credits"
        credit[vehicles[car]][traci.simulation.getTime()]["Policy"] = data[car_pol][0]
        credit[vehicles[car]][traci.simulation.getTime()]["Reputation"] = int(data[car_rep][0])
        credit[vehicles[car]][traci.simulation.getTime()]["Credits"] = int(data[car_cred][0])

    return credit


def time_init(credit, vehicle):
    credit[vehicle][traci.simulation.getTime()] = {}

    return credit
