from sandbox.ParserClass import ConfigParser

def event_func(curr, prev):
    config_fields = ConfigParser.parse_config("/home/lars/git_repo/lsha/sandbox/ConfigFile.txt")

    # if (row_index < config_fields.distance): # TODO(lars): This check is not possible right now. 
    #     return False, "index too low"

    #TODO fix this hack:
    cur_data = curr[0]#[config_fields.data_column_index]
    prev_data = prev[0]#[config_fields.data_column_index]   
    if(config_fields.range_list[0][0] < cur_data <= config_fields.range_list[0][1]):#current is in range
        if not (config_fields.range_list[0][0] < prev_data <= config_fields.range_list[0][1]):# prev was not in range
            return True, config_fields.name_list[0]
    elif(config_fields.range_list[0][0] < prev_data <= config_fields.range_list[0][1]):#current was not in range, but previous is
        return True, config_fields.name_list[-1]
    return False, "no event" 
