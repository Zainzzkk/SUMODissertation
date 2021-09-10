import traci

from Credits import DistanceFromJunction

# list for direction of neighbouring cars
direction = []


# main function for direction
def direction_check(neighbours):
    for neighbour in range(0, len(neighbours)):
        vehicles = traci.vehicle.getIDList()
        if neighbours[neighbour] in vehicles:
            # checks direction for each vehicle
            route_direction(neighbours[neighbour])
    # checks if clash after adding to direction list

    return check_clash(neighbours)


def route_direction(neighbour):
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
        return True
    # east and north clash so will set stop
    if ('E' in direction) and ('N' in direction):
        set_stop(neighbours)
        return True
    # west and south clash so sets stop
    if ('W' in direction) and ('S' in direction):
        set_stop(neighbours)
        return True
    # west and north clash so sets stop
    if ('W' in direction) and ('N' in direction):
        set_stop(neighbours)
        return True

    return False


# function to set the stop
def set_stop(neighbours):
    for i in range(0, len(neighbours)):
        vehicles = traci.vehicle.getIDList()
        if neighbours[i] in vehicles:
            # returns current edge that car is on
            current_edge = traci.vehicle.getRoadID(neighbours[i])
            # adds _0 to obtain lane of car
            full_current_edge = current_edge + "_0"
            # gets distance of lane that car is on
            distance = traci.lane.getLength(full_current_edge)
            # only sets stop if car has not reached junction, else no need for stop
            if DistanceFromJunction.passed_junction(neighbours[i]):
                try:
                    traci.vehicle.setStop(neighbours[i], traci.vehicle.getRoadID(neighbours[i]), distance, 0,
                                          100, 0)
                except traci.exceptions.TraCIException:
                    pass
