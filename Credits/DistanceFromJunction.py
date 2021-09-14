import traci

import Direction
from Credits import CreditPolicy


def Distance(vehicles):
    for car in range(0, len(vehicles)):
        # gets neighbour of each car
        neighbours = traci.vehicle.getContextSubscriptionResults(vehicles[car])
        if neighbours:
            neighbourcar = list(neighbours)
            # returns id of the car which is first to junction
            # neighbour_id = closest_to_junction(neighbourcar)
            # goes through neighbours
            for to_stop in range(0, len(neighbourcar)):
                if passed_junction(neighbourcar[to_stop]):
                    # checks that neighbour not already in stop_list
                    if neighbourcar[to_stop] not in CreditPolicy.stop_list:
                        # checks that ID not the same as first car
                        # checks that car has not already passed junction
                        if passed_junction(neighbourcar[to_stop]):
                            # adds to stop list
                            CreditPolicy.stop_list.append(neighbourcar[to_stop])

    # checks if stop_list is empty or not
    if CreditPolicy.stop_list:
        # only stops if clashing direction
        if not Direction.direction_check(CreditPolicy.stop_list):
            CreditPolicy.stop_list.clear()


# checks which car closest to junction
def closest_to_junction(neighbours):
    # list of distances of each car
    distances = []

    for vehicle in range(0, len(neighbours)):
        # returns how far car has travelled in current lane
        distance_travelled = traci.vehicle.getLanePosition(neighbours[vehicle])
        # calculates how long left till at junction : length of junction - distanced travelled
        distance_left = traci.lane.getLength(traci.vehicle.getLaneID(neighbours[vehicle])) - distance_travelled
        distances.append(distance_left)
    # returns the index of minimum distance left
    return distances.index(min(distances))


# checks if car passed junction
def passed_junction(vehicle):

    # gets route of vehicle and checks if current edge same as first edge on route

    if traci.vehicle.getRouteID(vehicle) == "E":
        if (traci.vehicle.getRoadID(vehicle) == "11E") or (traci.vehicle.getRoadID(vehicle) == "11W") or other_junction_ids(vehicle):
            if vehicle in CreditPolicy.stop_list:
                CreditPolicy.stop_list.remove(vehicle)
            return False

    if traci.vehicle.getRouteID(vehicle) == "W":
        if (traci.vehicle.getRoadID(vehicle) == "11W") or (traci.vehicle.getRoadID(vehicle) == "11E") or other_junction_ids(vehicle):
            if vehicle in CreditPolicy.stop_list:
                CreditPolicy.stop_list.remove(vehicle)
            return False

    if traci.vehicle.getRouteID(vehicle) == "N":
        if (traci.vehicle.getRoadID(vehicle) == "11N") or (traci.vehicle.getRoadID(vehicle) == "11S") or other_junction_ids(vehicle):
            if vehicle in CreditPolicy.stop_list:
                CreditPolicy.stop_list.remove(vehicle)
            return False

    if traci.vehicle.getRouteID(vehicle) == "S":
        if (traci.vehicle.getRoadID(vehicle) == "11S") or (traci.vehicle.getRoadID(vehicle) == "11N") or other_junction_ids(vehicle):
            if vehicle in CreditPolicy.stop_list:
                CreditPolicy.stop_list.remove(vehicle)
            return False

    return True


def other_junction_ids(vehicle):
    road_id = traci.vehicle.getRoadID(vehicle)

    if road_id == ":01_0":
        return True
    if road_id == ":10_0":
        return True
    if road_id == ":11_0":
        return True
    if road_id == ":11_1":
        return True
    if road_id == ":11_10":
        return True
    if road_id == ":11_11":
        return True
    if road_id == ":11_13":
        return True
    if road_id == ":11_14":
        return True
    if road_id == ":11_15":
        return True
    if road_id == ":11_16":
        return True
    if road_id == ":11_18":
        return True
    if road_id == ":11_19":
        return True
    if road_id == ":11_20":
        return True
    if road_id == ":11_21":
        return True
    if road_id == ":11_22":
        return True
    if road_id == ":11_23":
        return True
    if road_id == ":11_3":
        return True
    if road_id == ":11_4":
        return True
    if road_id == ":11_5":
        return True
    if road_id == ":11_6":
        return True
    if road_id == ":11_8":
        return True
    if road_id == ":11_9":
        return True
    if road_id == ":12_0":
        return True
    if road_id == ":21_0":
        return True

    return False

