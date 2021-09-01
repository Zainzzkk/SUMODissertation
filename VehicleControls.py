import traci
from random import randrange

import CreditPolicy


def remove_stop(vehicle, policy_list):
    if traci.vehicle.getStopState(vehicle[0]) == 1:
        traci.vehicle.resume(vehicle[0])
        print("removed stop stoppedlist ", CreditPolicy.stopped_list)
        CreditPolicy.stopped_list.remove(vehicle[0])
        CreditPolicy.stop_list.remove(vehicle[0])
        if policy_list:
            policy_list.remove(vehicle[0])
        print("removed stop veh ", vehicle[0])
        vehicle.remove(vehicle[0])


    return vehicle


def random_go(highest_credit, policy_list):
    # generates random number between 0 and cars in vehicle list
    togo = randrange(0, len(highest_credit))
    # checks if vehicle at random index is stopped and if stopped then resume
    print("removed stop rand ", CreditPolicy.stopped_list)
    if traci.vehicle.getStopState(highest_credit[togo]) == 1:
        traci.vehicle.resume(highest_credit[togo])
        print("resumed rand car: ", highest_credit[togo])
        CreditPolicy.stopped_list.remove(highest_credit[togo])
        CreditPolicy.stop_list.remove(highest_credit[togo])
        policy_list.remove(highest_credit[togo])

    return highest_credit
