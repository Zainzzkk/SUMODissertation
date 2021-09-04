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
            if traci.vehicle.getDistance(neighbours[i]) < distance:
                try:
                    traci.vehicle.setStop(neighbours[i], traci.vehicle.getRoadID(neighbours[i]), distance, 0,
                                          10, 0)
                except traci.exceptions.TraCIException:
                    pass