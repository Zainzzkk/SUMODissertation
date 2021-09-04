import traci

import RandomDirection

# global list of vehicles to be stopped
stop_list = []


def Distance(vehicles):
    for car in range(0, len(vehicles)):
        # gets neighbour of each car
        neighbours = traci.vehicle.getContextSubscriptionResults(vehicles[car])
        if neighbours:
            neighbourcar = list(neighbours)
            # returns id of the car which is first to junction
            neighbour_id = closest_to_junction(neighbourcar)
            # goes through neighbours
            for to_stop in range(0, len(neighbourcar)):
                # checks that neighbour not already in stop_list
                if neighbourcar[to_stop] not in stop_list:
                    # checks that ID not the same as first car
                    # checks that car has not already passed junction
                    if to_stop != neighbour_id and passed_junction(neighbourcar[to_stop]):
                        # adds to stop list
                        stop_list.append(neighbourcar[to_stop])

    # checks if stop_list is empty or not
    if stop_list:
        # only stops if clashing direction
        RandomDirection.direction_check(stop_list)
        # resumes based on when reached junction
        to_go(stop_list)


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
    if traci.vehicle.getRoute(vehicle)[0] != traci.vehicle.getRoadID(vehicle):
        return False

    return True


def to_go(stopped):
    # resumes in order of reaching junction
    for resume in range(0, len(stopped)):
        # checks if vehicle still in simulation
        vehicles = traci.vehicle.getIDList()
        if stopped[resume] in vehicles:
            if traci.vehicle.getStopState(stopped[resume]) == 1:
                traci.vehicle.resume(stopped[resume])