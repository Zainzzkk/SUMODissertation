import traci

# list for direction of neighbouring cars
direction = []


# main function for direction
def direction_check(neighbours):
    for neighbour in range(0, len(neighbours)):
        # checks direction for each vehicle
        route_direction(neighbours[neighbour])
    # checks if clash after adding to direction list
    check_clash(neighbours)


def route_direction(neighbour):
    if neighbour in traci.vehicle.getIDList():
        # returns route ID which is direction
        direc = traci.vehicle.getRouteID(neighbour)
        # adds to direction list if not in list
        if direc not in direction:
            direction.append(direc)


# checks if there is a clash in direction
def check_clash(neighbours):
    # east and south clash so will set stop
    if ('E' in direction) and ('S' in direction):
        set_stop(neighbours)
        return
    # east and north clash so will set stop
    if ('E' in direction) and ('N' in direction):
        set_stop(neighbours)
        return
    # west and south clash so sets stop
    if ('W' in direction) and ('S' in direction):
        set_stop(neighbours)
        return
    # west and north clash so sets stop
    if ('W' in direction) and ('N' in direction):
        set_stop(neighbours)
        return


# function to set the stop
def set_stop(neighbours):
    for i in range(0, len(neighbours)):
        if neighbours[i] in traci.vehicle.getIDList():
            # returns current edge that car is on
            current_edge = traci.vehicle.getRoadID(neighbours[i])
            # adds _0 to obtain lane of car
            full_current_edge = current_edge + "_0"
            # gets distance of lane that car is on
            distance = traci.lane.getLength(full_current_edge)
            # only sets stop if car has not reached junction, else no need for stop
            if passed_junction(neighbours[i]):
                try:
                    traci.vehicle.setStop(neighbours[i], traci.vehicle.getRoadID(neighbours[i]), distance, 0,
                                          10, 0)
                except traci.exceptions.TraCIException:
                    pass


# checks if car passed junction
def passed_junction(vehicle):
    # gets route of vehicle and checks if current edge same as first edge on route
    if traci.vehicle.getRouteID(vehicle) == "E":
        if (traci.vehicle.getRoadID(vehicle) == "11E") or (
                traci.vehicle.getRoadID(vehicle) == "11W") or other_junction_ids(vehicle):
            if traci.vehicle.getRouteID(vehicle) in direction:
                direction.remove(traci.vehicle.getRouteID(vehicle))
            return False

    if traci.vehicle.getRouteID(vehicle) == "W":
        if (traci.vehicle.getRoadID(vehicle) == "11W") or (
                traci.vehicle.getRoadID(vehicle) == "11E") or other_junction_ids(vehicle):
            if traci.vehicle.getRouteID(vehicle) in direction:
                direction.remove(traci.vehicle.getRouteID(vehicle))
            return False

    if traci.vehicle.getRouteID(vehicle) == "N":
        if (traci.vehicle.getRoadID(vehicle) == "11N") or (
                traci.vehicle.getRoadID(vehicle) == "11S") or other_junction_ids(vehicle):
            if traci.vehicle.getRouteID(vehicle) in direction:
                direction.remove(traci.vehicle.getRouteID(vehicle))
            return False

    if traci.vehicle.getRouteID(vehicle) == "S":
        if (traci.vehicle.getRoadID(vehicle) == "11S") or (
                traci.vehicle.getRoadID(vehicle) == "11N") or other_junction_ids(vehicle):
            if traci.vehicle.getRouteID(vehicle) in direction:
                direction.remove(traci.vehicle.getRouteID(vehicle))
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
