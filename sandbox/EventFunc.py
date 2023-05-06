def event_func(curr, prev):
    cur_data = curr[0]
    prev_data = prev[0]
    # cur_data is in range 0.
    if (-10.0 < cur_data <= 10.0):
        # prev was not in range 0.
        if not (-10.0 < prev_data <= 10.0):
            return True, 'stopped'

    # cur_data is in range 1.
    elif 10.0 < cur_data <= 3500.0:
        # prev_data was not in range 1.
        if not (10.0 < prev_data <= 3500.0):
            return True, 'started'

    # cur_data is not in any range.
    else:
        raise Exception(f"current field with value: {cur_data} does not belong to any range")

    return False, 'No event'