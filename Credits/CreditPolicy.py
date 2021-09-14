import traci
from random import randrange

from Credits import Default, DistanceFromJunction, Generous, Priority

# list of cars which have to stop
stop_list = []
# list of cars which have stopped
stopped_list = []
# list of priority cars
priority_list = []
# list of default cars
default_list = []
# list of generous cars
generous_list = []
# list of unstopped priority cars
priority_list_unstop = []
# list of unstopped default cars
default_list_unstop = []
# list of unstopped generous cars
generous_list_unstop = []


# implements credit policy
def credit_policy(vehicles, data):
    # checks who is first and stops rest
    DistanceFromJunction.Distance(vehicles)
    stopped_cars()
    # adds car priority to list
    policy_checker(data)
    # if priority list not empty and if priority cars stopped
    # only want to do these if stopped cars or else wasting resources
    if priority_list:
        data = Priority.priority_go(data)
    # if default list not empty and if default cars stopped
    if default_list and not priority_list_unstop and not priority_list:
        data = Default.default_go(data)
    # if generous list not empty and if generous cars stopped
    if generous_list and not priority_list_unstop and not default_list_unstop and not priority_list and not default_list:
        data = Generous.generous_go(data)
    return data


def stopped_cars():
    remove = []
    for car in range(0, len(stop_list)):
        if traci.vehicle.isStopped(stop_list[car]):
            if stop_list[car] not in stopped_list:
                stopped_list.append(stop_list[car])
                remove.append(stop_list[car])
    remove_stop_list(remove)


def remove_stop_list(vehicles):
    for vehicle in vehicles:
        if vehicle in stop_list:
            stop_list.remove(vehicle)


# checks which cars are which policy
def policy_checker(data):
    # checks which car is priority
    priority_check(data)
    # checks which car is default
    default_check(data)
    # checks which car is generous
    generous_check(data)


def priority_check(data):
    for car in range(0, len(stop_list)):
        if (stop_list[car] not in stopped_list) and (traci.vehicle.getSpeed(stop_list[car]) != 0):
            car_rep = stop_list[car] + ".policy"
            if data[car_rep][0] == "priority":
                traci.vehicle.setColor(stop_list[car], (0, 225, 0))
                # only adds once to list
                current_edge = traci.vehicle.getRoadID(stop_list[car])
                # adds _0 to obtain lane of car
                full_current_edge = current_edge + "_0"
                # gets distance of lane that car is on
                distance = traci.lane.getLength(full_current_edge) * 0.75
                distance_travelled = traci.vehicle.getLanePosition(stop_list[car])
                if stop_list[car] not in priority_list_unstop:
                    if distance_travelled > distance:
                        priority_list_unstop.append(stop_list[car])

    for car in range(0, len(stopped_list)):
        # makes string with car reputation in dataframe
        car_rep = stopped_list[car] + ".policy"
        # matches if priority for car
        if data[car_rep][0] == "priority":
            # only adds once to list
            if stopped_list[car] not in priority_list:
                priority_list.append(stopped_list[car])
                if stopped_list[car] in priority_list_unstop:
                    priority_list_unstop.remove(stopped_list[car])


def default_check(data):
    for car in range(0, len(stop_list)):
        if (stop_list[car] not in stopped_list) and (traci.vehicle.getSpeed(stop_list[car]) != 0):
            car_rep = stop_list[car] + ".policy"
            if data[car_rep][0] == "default":
                traci.vehicle.setColor(stop_list[car], (0, 0, 225))
                # only adds once to list
                current_edge = traci.vehicle.getRoadID(stop_list[car])
                # adds _0 to obtain lane of car
                full_current_edge = current_edge + "_0"
                # gets distance of lane that car is on
                distance = traci.lane.getLength(full_current_edge) * 0.75
                distance_travelled = traci.vehicle.getLanePosition(stop_list[car])
                if stop_list[car] not in default_list_unstop:
                    if distance_travelled > distance:
                        default_list_unstop.append(stop_list[car])

    for car in range(0, len(stopped_list)):
        car_rep = stopped_list[car] + ".policy"
        # matches if default for car
        if data[car_rep][0] == "default":
            if stopped_list[car] not in default_list:
                default_list.append(stopped_list[car])
                if stopped_list[car] in default_list_unstop:
                    default_list_unstop.remove(stopped_list[car])
    default_checker()


def generous_check(data):
    for car in range(0, len(stop_list)):
        if (stop_list[car] not in stopped_list) and (traci.vehicle.getSpeed(stop_list[car]) != 0):
            car_rep = stop_list[car] + ".policy"
            if data[car_rep][0] == "generous":
                traci.vehicle.setColor(stop_list[car], (255, 0, 0))
                # only adds once to list
                current_edge = traci.vehicle.getRoadID(stop_list[car])
                # adds _0 to obtain lane of car
                full_current_edge = current_edge + "_0"
                # gets distance of lane that car is on
                distance = traci.lane.getLength(full_current_edge) * 0.75
                distance_travelled = traci.vehicle.getLanePosition(stop_list[car])
                if stop_list[car] not in generous_list_unstop:
                    if distance_travelled > distance:
                        generous_list_unstop.append(stop_list[car])

    for car in range(0, len(stopped_list)):
        car_rep = stopped_list[car] + ".policy"
        # matches if generous for car
        if data[car_rep][0] == "generous":
            if stopped_list[car] not in generous_list:
                generous_list.append(stopped_list[car])
                if stopped_list[car] in generous_list_unstop:
                    generous_list_unstop.remove(stopped_list[car])
    generous_checker()


def default_checker():
    prior_remover = []
    for default in default_list:
        default_edge = traci.vehicle.getRoadID(default)
        for priority in priority_list_unstop:
            priority_edge = traci.vehicle.getRoadID(priority)
            if priority_edge == default_edge:
                if priority not in prior_remover:
                    prior_remover.append(priority)

    for remove in prior_remover:
        if remove in priority_list_unstop:
            priority_list_unstop.remove(remove)


def generous_checker():
    prior_remover = []
    default_remover = []

    for generous in generous_list:
        generous_edge = traci.vehicle.getRoadID(generous)
        for priority in priority_list_unstop:
            priority_edge = traci.vehicle.getRoadID(priority)
            if priority_edge == generous_edge:
                if priority not in prior_remover:
                    prior_remover.append(priority)

        for default in default_list_unstop:
            default_edge = traci.vehicle.getRoadID(default)
            if default_edge == generous_edge:
                if default not in default_remover:
                    default_remover.append(default)

    for remove in prior_remover:
        if remove in priority_list_unstop:
            priority_list_unstop.remove(remove)

    for def_remove in default_remover:
        if def_remove in default_list_unstop:
            default_list_unstop.remove(def_remove)
