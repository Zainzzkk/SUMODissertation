from Credits import Credit, CreditPolicy, Reputation, VehicleControls


def priority_go(data):
    # list for highest reputation cars
    highest_rep = []
    # list for highest credit cars
    highest_credit = []
    # checks if enough reputation
    data = reputation_check(data)
    # checks if enough credits
    data = credit_check(data)
    # if only 1 car on priority list, then it goes
    if len(CreditPolicy.priority_list) == 1:
        highest_rep, data = VehicleControls.remove_stop(CreditPolicy.priority_list, highest_rep, data)
        return data

    # loop checking for next highest until list cleared
    while CreditPolicy.priority_list:
        # checks which car has highest reputation
        highest_rep = Reputation.check_highest_reputation(CreditPolicy.priority_list, data)
        # if more than 1 on same highest rep
        if len(highest_rep) > 1:
            # check for highest credit
            highest_credit = Credit.check_highest_credit(CreditPolicy.priority_list, data)
            # if more than 1 on highest credit
            if len(highest_credit) > 1:
                # random car goes from those with highest
                highest_credit, data = VehicleControls.random_go(highest_credit, CreditPolicy.priority_list, data)
            else:
                # else car with highest credit goes first
                highest_credit, data = VehicleControls.remove_stop(highest_credit, CreditPolicy.priority_list, data)
        else:
            # or car with highest reputation goes first
            highest_rep, data = VehicleControls.remove_stop(highest_rep, CreditPolicy.priority_list, data)

    return data


# checks if enough reputation to be priority
def reputation_check(data):
    # list to store cars to remove so always in index
    to_remove = []
    # goes through priority list
    for car in range(0, len(CreditPolicy.priority_list)):
        # string for car rep
        car_rep = CreditPolicy.priority_list[car] + ".reputation"
        # if less than 3, then not enough reputation
        if data[car_rep][0] < 3:
            # add to removal list
            to_remove.append(CreditPolicy.priority_list[car])
    # move from priority to default
    data = remove_prior_list(to_remove, data)

    return data


def remove_prior_list(to_remove, data):
    # goes through priority to remove list
    for car in range(0, len(to_remove)):
        # get car policy
        car_policy = to_remove[car] + ".policy"
        # change policy to default
        data[car_policy] = data[car_policy].replace(["priority"], "default")
        print("policy changed on: ", to_remove[car], " ", data[car_policy][0])
        # add to default list
        CreditPolicy.default_list.append(to_remove[car])
        print("removed ", to_remove[car])
        # remove from priority
        CreditPolicy.priority_list.remove(to_remove[car])

    return data


def credit_check(data):
    # list to remove from priority
    to_remove = []
    # goes through priority list
    for car in range(0, len(CreditPolicy.priority_list)):
        # makes credit string
        car_cred = CreditPolicy.priority_list[car] + ".credits"
        # makes reputation string
        car_rep = CreditPolicy.priority_list[car] + ".reputation"
        # stores the value for credit
        car_cred_int = int(data[car_cred][0])
        # stores int for reputation
        car_rep_int = int(data[car_rep][0])

        # low reputation
        if 1 <= car_rep_int <= 4:
            # gets list of stop_list as they will have credits transferred to them
            stop_list_len = len(CreditPolicy.stop_list)
            # 6 credits per car so 6 * length
            if car_cred_int < 6 * stop_list_len:
                # if less than 6 * car then removes
                to_remove.append(CreditPolicy.priority_list[car])

        # average reputation
        if 5 <= car_rep_int <= 7:
            stop_list_len = len(CreditPolicy.stop_list)
            if car_cred_int < 4 * stop_list_len:
                to_remove.append(CreditPolicy.priority_list[car])

        # high reputation
        if 8 <= car_rep_int <= 10:
            stop_list_len = len(CreditPolicy.stop_list)
            if car_cred_int < 2 * stop_list_len:
                to_remove.append(CreditPolicy.priority_list[car])

    # removes from priority list
    data = remove_prior_list(to_remove, data)

    return data


# transfers credits to other cars
def priority_credit_transfer(vehicle, data):
    # reputation string
    car_rep = vehicle + ".reputation"
    # value for reputation
    car_rep_int = int(data[car_rep][0])
    # string for credits
    car_credit = vehicle + ".credits"
    # if low reputation
    if 1 <= car_rep_int <= 4:
        # goes through stop list
        for car in range(0, len(CreditPolicy.stop_list)):
            # transfers 6 credits to each car in stop list
            data = amount_to_transfer(CreditPolicy.stop_list[car], 6, data)
            # gets current car credit
            car_credit_int = int(data[car_credit][0])
            # takes away 6 per car
            new_car_credit_int = car_credit_int - 6
            # changes credit to new credit
            # matches old credit and changes that value
            data[car_credit] = data[car_credit].replace([car_credit_int], new_car_credit_int)
            print(vehicle, " credit changed to ", data[car_credit][0])

    # if average reputation
    if 5 <= car_rep_int <= 7:
        # goes through stop list
        for car in range(0, len(CreditPolicy.stop_list)):
            # transfers 4 credits per car
            data = amount_to_transfer(CreditPolicy.stop_list[car], 4, data)
            # current car credit
            car_credit_int = int(data[car_credit][0])
            # takes away 4 per car
            new_car_credit_int = car_credit_int - 4
            # changes car credit
            data[car_credit] = data[car_credit].replace([car_credit_int], new_car_credit_int)
            print(vehicle, " credit changed to ", data[car_credit][0])

    # good reputation
    if 8 <= car_rep_int <= 10:
        # goes through stop list
        for car in range(0, len(CreditPolicy.stop_list)):
            # transfers 2 credit per car
            data = amount_to_transfer(CreditPolicy.stop_list[car], 2, data)
            car_credit_int = int(data[car_credit][0])
            # takes away 2 credits per car
            new_car_credit_int = car_credit_int - 2
            # changes credit
            data[car_credit] = data[car_credit].replace([car_credit_int], new_car_credit_int)
            print(vehicle, " credit changed to ", data[car_credit][0])

    return data


# transfers amount
def amount_to_transfer(vehicle, credit, data):
    # makes credit string
    stop_cred = vehicle + ".credits"
    # gets current credit for car
    stop_credit = int(data[stop_cred][0])
    # adds amount to credit
    new_stop_credit = stop_credit + credit
    # changes credit on car
    data[stop_cred] = data[stop_cred].replace([stop_credit], new_stop_credit)
    print(vehicle, " credit changed to ", data[stop_cred][0])
    return data
