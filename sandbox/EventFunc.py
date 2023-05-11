def event_func(curr, prev):
    cur_data = curr[0]
    prev_data = prev[0]
    # cur_data is in range 0.
    if (-1.0 < cur_data <= 5.0):
        # prev was not in range 0.
        if not (-1.0 < prev_data <= 5.0):
            return True, 'stopped'

    # cur_data is in range 1.
    elif 5.0 < cur_data <= 1000.0:
        # prev_data was not in range 1.
        if not (5.0 < prev_data <= 1000.0):
            return True, 'slow'

    # cur_data is in range 2.
    elif 1000.0 < cur_data <= 3000.0:
        # prev_data was not in range 2.
        if not (1000.0 < prev_data <= 3000.0):
            return True, 'medium'

    # cur_data is in range 3.
    elif 3000.0 < cur_data <= 4000.0:
        # prev_data was not in range 3.
        if not (3000.0 < prev_data <= 4000.0):
            return True, 'fast'

    # cur_data is not in any range.
    else:
        raise Exception(f"current field with value: {cur_data} does not belong to any range")

    return False, 'No event'