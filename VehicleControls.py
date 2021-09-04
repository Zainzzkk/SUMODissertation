import traci
from random import randrange

import CreditPolicy
import Default
import Generous
import Priority


# removes the stop for a single vehicle
def remove_stop(vehicle, policy_list, data):
    # if vehicle has stopped
    if traci.vehicle.getStopState(vehicle[0]) == 1:
        # get current edge car is on
        current_edge = traci.vehicle.getRoadID(vehicle[0])
        # full edge stored with _0
        full_current_edge = current_edge + "_0"
        # distance car has travelled
        distance = traci.lane.getLength(full_current_edge)
        try:
            # removes the stop set on car
            traci.vehicle.setStop(vehicle[0], traci.vehicle.getRoadID(vehicle[0]), distance, 0,
                                  0, 0)
        except traci.exceptions.TraCIException:
            # pass if no stop
            pass
        #traci.vehicle.resume(vehicle[0])
        # changes the reputation for car based on policy
        data = reputation_change(vehicle[0], data)
        # removes car from stopped list
        CreditPolicy.stopped_list.remove(vehicle[0])
        # removes from stop list
        CreditPolicy.stop_list.remove(vehicle[0])
        # if not empty, removes from policy list
        if policy_list:
            policy_list.remove(vehicle[0])
        print("removed stop veh ", vehicle[0])
        # transfers credits to other vehicles
        data = credit_transfer(vehicle[0], data)
        # removes from list
        vehicle.remove(vehicle[0])
        # check if any vehicles are generous
        data = Generous.generous_check(data)
    # returns list and also data
    return vehicle, data


# when randomly have to choose car to go
def random_go(highest_credit, policy_list, data):
    # generates random number between 0 and cars in vehicle list
    togo = randrange(0, len(highest_credit))
    # checks if vehicle at random index is stopped and if stopped then resume
    if traci.vehicle.getStopState(highest_credit[togo]) == 1:
        # get current edge car is on
        current_edge = traci.vehicle.getRoadID(highest_credit[togo])
        # full edge stored with _0
        full_current_edge = current_edge + "_0"
        # distance car has travelled
        distance = traci.lane.getLength(full_current_edge)
        try:
            # removes the stop set on car
            traci.vehicle.setStop(highest_credit[togo], traci.vehicle.getRoadID(highest_credit[togo]), distance, 0,
                                  0, 0)
        except traci.exceptions.TraCIException:
            # pass if no stop
            pass
        # changes reputation
        data = reputation_change(highest_credit[togo], data)
        # checks for generous cars credit
        data = Generous.generous_check(data)
        print("resumed rand car: ", highest_credit[togo])
        # removes car from stopped list
        CreditPolicy.stopped_list.remove(highest_credit[togo])
        # removes car from stop list
        CreditPolicy.stop_list.remove(highest_credit[togo])
        # transfers credit based on policy
        data = credit_transfer(highest_credit[togo], data)
        # removes from policy list
        policy_list.remove(highest_credit[togo])
        # removes from highest credit list
        highest_credit.remove(highest_credit[togo])

    # returns credit list and dataframe
    return highest_credit, data


# checks what reputation change required
def reputation_change(vehicle, data):
    # string for car reputation
    car_rep = vehicle + ".reputation"
    # string for car policy
    car_policy = vehicle + ".policy"
    # stores reputation as int
    reputation = int(data[car_rep][0])

    # if policy is priority
    if data[car_policy][0] == "priority":
        # takes 2 away from reputation
        new_rep = reputation - 2
        # changes car reputation
        data[car_rep] = data[car_rep].replace([reputation], new_rep)
        print(vehicle, " rep changed to ", data[car_rep][0])

    # if policy is default
    if data[car_policy][0] == "default":
        # if max rep then no change
        if reputation == 10:
            new_rep = reputation
        else:
            # else adds 1 to reputation
            new_rep = reputation + 1
        # changes reputation
        data[car_rep] = data[car_rep].replace([reputation], new_rep)
        print(vehicle, " rep changed to ", data[car_rep][0])

    # if generous policy
    if data[car_policy][0] == "generous":
        # if already max rep then no change
        if reputation == 10:
            new_rep = reputation
        else:
            # adds 2 to reputation
            new_rep = reputation + 2
        data[car_rep] = data[car_rep].replace([reputation], new_rep)
        print(vehicle, " rep changed to ", data[car_rep][0])

    return data


# transfers credits
def credit_transfer(vehicle, data):
    #string for policy
    car_policy = vehicle + ".policy"

    # if priority
    if data[car_policy][0] == "priority":
        # then transfer sorted by Priority function
        data = Priority.priority_credit_transfer(vehicle, data)

    # if default
    if data[car_policy][0] == "default":
        # transfer sorted by Default function
        data = Default.default_credit_transfer(vehicle, data)

    return data
