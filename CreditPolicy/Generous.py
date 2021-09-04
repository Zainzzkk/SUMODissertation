import CreditPolicy
import Reputation
from CreditPolicy import Credit
import VehicleControls


def generous_go(data):
    highest_rep = []
    highest_credit = []

    # if only 1 car in generous list
    if len(CreditPolicy.generous_list) == 1:
        highest_rep, data = VehicleControls.remove_stop(CreditPolicy.generous_list, highest_rep, data)
        return data

    # while cars on generous list
    while CreditPolicy.generous_list():
        highest_rep = Reputation.check_highest_reputation(CreditPolicy.generous_list, data)
        if len(highest_rep) > 1:
            highest_credit = Credit.check_highest_credit(CreditPolicy.generous_list, data)
            if len(highest_credit) > 1:
                highest_credit, data = VehicleControls.random_go(highest_credit, CreditPolicy.generous_list, data)
            else:
                highest_credit, data = VehicleControls.remove_stop(highest_credit, CreditPolicy.generous_list, data)
        else:
            highest_rep, data = VehicleControls.remove_stop(highest_rep, CreditPolicy.generous_list, data)

    return data


# checks if any cars in stop list are generous
def generous_check(data):
    for car in range(0, len(CreditPolicy.stopped_list)):
        # string for car policy
        car_policy = CreditPolicy.stopped_list[car] + ".policy"
        # if generous policy
        if data[car_policy][0] == "generous":
            # checks reputation and then gives credits
            data = generous_rep_check(CreditPolicy.stopped_list[car], data)

    return data


def generous_rep_check(vehicle, data):
    # gets cars reputation
    car_rep = vehicle + ".reputation"
    # gets int for car rep
    car_rep_int = int(data[car_rep][0])

    # if low reputation
    if 1 <= car_rep_int <= 4:
        # gain only 1 credit
        data = generous_credit_gained(vehicle, 1, data)
    # if medium reputation
    if 5 <= car_rep_int <= 7:
        # gets 2 credits
        data = generous_credit_gained(vehicle, 2, data)
    # if high reputation
    if 8 <= car_rep_int <= 10:
        # gains 3 credits
        data = generous_credit_gained(vehicle, 3, data)

    return data


# for how transferring credits gained
def generous_credit_gained(vehicle, credit, data):
    # string for car credits
    car_cred = vehicle + ".credits"
    # stores current car credit
    car_cred_int = int(data[car_cred][0])
    # new credit
    new_car_cred_int = car_cred_int + credit
    # changes credits
    data[car_cred] = data[car_cred].replace([car_cred_int], new_car_cred_int)

    return data
