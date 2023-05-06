from sandbox.ParserClass import ConfigParser


def event_func(curr, prev):
    config_fields = ConfigParser.parse_config(
        "/home/lars/git_repo/lsha/sandbox/ConfigFile.txt"
    )
    cur_data = curr[0]
    prev_data = prev[0]

    # current is in range 0.
    if config_fields.range_list[0][0] < cur_data <= config_fields.range_list[0][1]:
        # prev was not in range 0.
        if not (
            config_fields.range_list[0][0] < prev_data <= config_fields.range_list[0][1]
        ):
            return True, config_fields.name_list[0]

    # current is in range 1.
    elif config_fields.range_list[1][0] < cur_data <= config_fields.range_list[1][1]:
        # prev was not in range 1.
        if not (
            config_fields.range_list[1][0] < prev_data <= config_fields.range_list[1][1]
        ):
            return True, config_fields.name_list[1]

    # current is in range 2.
    elif config_fields.range_list[2][0] < cur_data <= config_fields.range_list[2][1]:
        # prev was not in range 2.
        if not (
            config_fields.range_list[2][0] < prev_data <= config_fields.range_list[2][1]
        ):
            return True, config_fields.name_list[2]
    # current is not in any range.
    else:
        raise Exception(
            f"current field with value: {cur_data} does not belong to any range"
        )

    # current was in a range, but prevois was in the same.
    return False, "No event"
