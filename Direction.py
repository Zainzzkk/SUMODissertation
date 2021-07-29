import traci

direction = []


def direction_check(neighbours):
    for neighbour in range(0, len(neighbours)):
        route_direction(neighbours[neighbour])

    check_clash(neighbours)


def route_direction(neighbour):
    direc = traci.vehicle.getRouteID(neighbour)
    if direc not in direction:
        direction.append(direc)


def check_clash(neighbours):
    if ('E' in direction) and ('S' in direction):
        set_stop(neighbours)
    if ('E' in direction) and ('N' in direction):
        set_stop(neighbours)
    if ('W' in direction) and ('S' in direction):
        set_stop(neighbours)
    if ('W' in direction) and ('N' in direction):
        set_stop(neighbours)


def set_stop(neighbours):
    for i in range(0, len(neighbours)):
        currentEdge = traci.vehicle.getRoadID(neighbours[i])
        fullCurrentEdge = currentEdge + "_0"
        distance = traci.lane.getLength(fullCurrentEdge)
        if traci.vehicle.getDistance(neighbours[i]) < distance:
            try:
                traci.vehicle.setStop(neighbours[i], traci.vehicle.getRoadID(neighbours[i]), distance, 0,
                                      10, 0)
            except traci.exceptions.TraCIException:
                pass
