range_list = [[0.0, 1000.0], [1000.0, 2000.0], [2000.0, 3000.0], [3000.0, 4000.0]]
name_list = ['r_0', 'r_1', 'r_2', 'r_3', 'LOAD', 'UNLOAD']
def event_func(curr, prev):
    events_found = []
    # curr is in range 0.
    if (0.0 <= curr[0] <= 1000.0):
        # prev was not in range 0.
        if not (0.0 <= prev[0] <= 1000.0):
            events_found.append('r_0')

    # cur_data is in range 1.
    elif 1000.0 < curr[0] <= 2000.0:
        # prev_data was not in range 1.
        if not (1000.0 < prev[0] <= 2000.0):
            events_found.append('r_1')

    # cur_data is in range 2.
    elif 2000.0 < curr[0] <= 3000.0:
        # prev_data was not in range 2.
        if not (2000.0 < prev[0] <= 3000.0):
            events_found.append('r_2')

    # cur_data is in range 3.
    elif 3000.0 < curr[0] <= 4000.0:
        # prev_data was not in range 3.
        if not (3000.0 < prev[0] <= 4000.0):
            events_found.append('r_3')

    # curr[{signal_index}] not equal to prev[{signal_index}].
    if (curr[1] != prev[1]):
        if curr[1] in name_list:
            events_found.append(curr[1])

    if len(events_found) == 0:
        status_list = [False, ['No event']]
    else:
        status_list = [True, events_found]
    return status_list

def get_range_list():
    return range_list

def get_name_list():
    return name_list