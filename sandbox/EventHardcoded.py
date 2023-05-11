from sandbox.ParserClass import ConfigParser


def event_func(curr, prev):
    config_fields = ConfigParser.parse_config(
        "/home/lars/git_repo/lsha/sandbox/ConfigFile.txt"
    )
    cur_data = curr[0]
    prev_data = prev[0]
    found_cur_range = False
    found_prev_range = False
    for i, r in enumerate(config_fields.range_list):
        if not found_cur_range and r[0] < cur_data <= r[1]:
            found_cur_range = True
            cur_range = config_fields.name_list[i]
        if not found_prev_range and r[0] < prev_data <= r[1]:
            found_prev_range = True
            prev_range = config_fields.name_list[i]

        if found_cur_range and found_prev_range:
            if cur_range != prev_range:
                return True, f"{cur_range}_from_{prev_range}"
            else:
                break

    # No event was found.
    return False, "No event"
