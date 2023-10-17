def event_func(curr, prev):
    cur_data = curr[0]
    prev_data = prev[0]
    # cur_data is equal to prev_data.
    if (cur_data != prev_data):
        return True, cur_data 

    return False, 'No event'