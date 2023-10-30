def event_func(curr, prev):
    cur_data = curr[0]
    prev_data = prev[0]
    # cur_data is in range 0.
    if (0.0 <= cur_data <= 1000.0):
        # prev was not in range 0.
        if not (0.0 <= prev_data <= 1000.0):
            return True, 'm_0'

    # cur_data is in range 1.
    elif 1000.0 < cur_data <= 2000.0:
        # prev_data was not in range 1.
        if not (1000.0 < prev_data <= 2000.0):
            return True, 'm_1'

    # cur_data is in range 2.
    elif 2000.0 < cur_data <= 3000.0:
        # prev_data was not in range 2.
        if not (2000.0 < prev_data <= 3000.0):
            return True, 'm_2'

    # cur_data is in range 3.
    elif 3000.0 < cur_data <= 4000.0:
        # prev_data was not in range 3.
        if not (3000.0 < prev_data <= 4000.0):
            return True, 'm_3'

    # cur_data is not in any range.
    else:
        raise Exception(f"current field with value: {cur_data} does not belong to any range")

    return False, 'No event'

def get_range_list():
    return [[0.0, 1000.0], [1000.0, 2000.0], [2000.0, 3000.0], [3000.0, 4000.0]]

def get_name_list():
    return ['m_0', 'm_1', 'm_2', 'm_3']