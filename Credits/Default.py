from Credits import CreditPolicy, Reputation, Credit, VehicleControls, Priority


def default_go(data):
    # list for highest reputation
    highest_rep = []
    # list for highest credit
    highest_credit = []
    # CreditPolicy.stopped_cars()
    # CreditPolicy.policy_checker(data)
    # while CreditPolicy.priority_list_unstop:
    #     CreditPolicy.stopped_cars()
    #     CreditPolicy.policy_checker(data)
    #     data = Priority.priority_go(data)
    # if only 1 car in default list
    if len(CreditPolicy.default_list) == 1:
        # CreditPolicy.stopped_cars()
        # CreditPolicy.policy_checker(data)
        # then remove stop for that car (blank highest rep list)
        highest_rep, data = VehicleControls.remove_stop(CreditPolicy.default_list, highest_rep, data)
        return data

    # whilst still cars in default list
    while CreditPolicy.default_list:
        # CreditPolicy.stopped_cars()
        # CreditPolicy.policy_checker(data)
        # checks for highest reputation
        highest_rep = Reputation.check_highest_reputation(CreditPolicy.default_list, data)
        # if more than 1 car with highest rep
        if len(highest_rep) > 1:
            # then check for highest credit
            highest_credit = Credit.check_highest_credit(CreditPolicy.default_list, data)
            # if more than 1 with highest credit then random cars go
            if len(highest_credit) > 1:
                highest_credit, data = VehicleControls.random_go(highest_credit, CreditPolicy.default_list, data)
            else:
                # else highest credit goes first
                highest_credit, data = VehicleControls.remove_stop(highest_credit, CreditPolicy.default_list, data)
        else:
            # else highest rep goes first
            highest_rep, data = VehicleControls.remove_stop(highest_rep, CreditPolicy.default_list, data)

    return data


# transfers credits for default policy
def default_credit_transfer(vehicle, data):
    # makes string for credit
    car_credit = vehicle + ".credits"
    # goes through stop list
    for car in range(0, len(CreditPolicy.stop_list)):
        # string for each cars credit
        stop_cred = CreditPolicy.stop_list[car] + ".credits"
        # int stores credit
        stop_credits = int(data[stop_cred][0])
        # adds 1 to credit
        new_stop_credits = stop_credits + 1
        # changes credits for car
        data[stop_cred] = data[stop_cred].replace([stop_credits], new_stop_credits)
        #print(CreditPolicy.stop_list[car], " credit changed to ", data[stop_cred][0])
        # removes credits from car which goes
        data = default_moving_car(car_credit, data)
        #print(vehicle, " credit changed to ", data[car_credit][0])

    return data


def default_moving_car(car_credit, data):
    # integer with car credit
    car_credit_int = int(data[car_credit][0])
    # if not 0 then removes 1, else stays on 0
    if car_credit_int != 0:
        new_car_credit = car_credit_int - 1
        data[car_credit] = data[car_credit].replace([car_credit_int], new_car_credit)

    return data
