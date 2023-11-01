import os
import argparse
from pathlib import Path
import numpy as np

from sandbox.ParserClass import ConfigParser

parser = argparse.ArgumentParser()
parser.add_argument("--config_dir", "-c", type=Path, required=True, help="absolute path to directory with config file(s)")

args = parser.parse_args()
if not args.config_dir.exists():
    raise ValueError(f"{args.config_dir} does not exist")

config_files = [os.path.join(args.config_dir, conf_file) for conf_file in os.listdir(args.config_dir) if '~' not in conf_file]
config_files.sort()

INDENT = 4 * " "

if os.path.isfile("sandbox/EventFunc.py"):
    os.remove("sandbox/EventFunc.py")

def file_start(signal_index: int):
    return_str = (
        f"range_list = {config_fields.range_list}\n"
        + f"name_list = {name_list}\n"
        + "def event_func(curr, prev):\n"
        # + INDENT + f"cur_data = curr[{signal_index}]\n"
        # + INDENT + f"prev_data = prev[{signal_index}]\n"
        + INDENT + "events_found = []\n"

    )
    return return_str

# def update_names_list():
#     return_str = (
#         INDENT + f"name_list.append({config_fields.name_list})\n"

#     )
#     return return_str
    
def no_range():
    return_str = (
        INDENT
        + "# cur_data is not in any range.\n"
        + INDENT
        + "else:\n"
        + INDENT * 2
        + 'raise Exception(f"current field with value: {cur_data} does not belong to any range")\n\n'
    )
    return return_str

def file_end():
    return_str = (
        # no_range()
        INDENT + "if len(events_found) == 0:\n"
        + INDENT * 2 + "status_list = [False, ['No event']]\n"
        + INDENT + "else:\n"
        + INDENT * 2 + "status_list = [True, events_found]\n"
        + INDENT + "return status_list\n\n"
        + "def get_range_list():\n"
        + INDENT + f"return range_list\n\n"
        + "def get_name_list():\n"
        + INDENT + f"return name_list"

    )
    return return_str

def unordered_wo_ranges(first: bool, last:bool, signal_index: int):

    def wo_range():
        return_str = (
            INDENT
            + "# curr[{signal_index}] not equal to prev[{signal_index}].\n"
            + INDENT
            + f"if (curr[{signal_index}] != prev[{signal_index}]):\n"
            + INDENT * 2
            + f"events_found.append(curr[{signal_index}])\n\n"
            + INDENT * 2
            + f"if curr[{signal_index}] not in name_list:\n"
            + INDENT * 3
            + f"name_list.append(curr[{signal_index}])\n\n"
        )
        return return_str

    with open("sandbox/EventFunc.py", "a") as file:
        if first:
            file.write(file_start(signal_index))
        file.write(wo_range())
        if last:
            file.write(file_end())

def pick(first: bool, last: bool, signal_index: int):
    def w_names_only():
        return_str = (
            INDENT
            + "# curr[{signal_index}] not equal to prev[{signal_index}].\n"
            + INDENT
            + f"if (curr[{signal_index}] != prev[{signal_index}]):\n"
            + INDENT * 2
            + f"if curr[{signal_index}] in name_list:\n"
            + INDENT * 3
            + f"events_found.append(curr[{signal_index}])\n\n"
            # + INDENT * 3
            # + f"name_list.append(curr[{signal_index}])\n\n"
        )
        return return_str

    with open("sandbox/EventFunc.py", "a") as file:
        if first:
            file.write(file_start(signal_index))
        file.write(w_names_only())
        if last:
            file.write(file_end())
        

def unordered(first: bool, last: bool, signal_index: int):
    def first_range():
        return_str = (
            INDENT
            + "# curr is in range 0.\n"
            + INDENT
            + f"if ({config_fields.range_list[0][0]} <= curr[{signal_index}] <= {config_fields.range_list[0][1]}):\n"
            + INDENT * 2
            + "# prev was not in range 0.\n"
            + INDENT * 2
            + f"if not ({config_fields.range_list[0][0]} <= prev[{signal_index}] <= {config_fields.range_list[0][1]}):\n"
            + INDENT * 3
            + f"events_found.append('{config_fields.name_list[0]}')\n\n"
        )
        return return_str

    def mid_ranges(ri):
        return_str = (
            INDENT
            + f"# cur_data is in range {ri}.\n"
            + INDENT
            + f"elif {config_fields.range_list[ri][0]} < curr[{signal_index}] <= {config_fields.range_list[ri][1]}:\n"
            + INDENT * 2
            + f"# prev_data was not in range {ri}.\n"
            + INDENT * 2
            + f"if not ({config_fields.range_list[ri][0]} < prev[{signal_index}] <= {config_fields.range_list[ri][1]}):\n"
            + INDENT * 3
            + f"events_found.append('{config_fields.name_list[ri]}')\n\n"
        )
        return return_str

    with open("sandbox/EventFunc.py", "a") as file:
        if first:
            file.write(file_start(signal_index))
        file.write(first_range())
        if num_ranges > 1:
            for nr in range(1, num_ranges):
                file.write(mid_ranges(nr))
        if last:
            file.write(file_end())


def ordered(first: bool, last:bool, signal_index: int):
    def range_check():
        return_str = (
            INDENT
            + "for i, r in enumerate(range_list):"
            + "\n"
            + INDENT * 2
            + "if not found_cur_range and r[0] < cur_data <= r[1]:"
            + "\n"
            + INDENT * 3
            + "found_cur_range = True"
            + "\n"
            + INDENT * 3
            + "cur_range = name_list[i]"
            + "\n"
            + INDENT * 2
            + "if not found_prev_range and r[0] < prev_data <= r[1]:"
            + "\n"
            + INDENT * 3
            + "found_prev_range = True"
            + "\n"
            + INDENT * 3
            + "prev_range = name_list[i]"
            + "\n"
            + INDENT * 2
            + "if found_cur_range and found_prev_range:"
            + "\n"
            + INDENT * 3
            + "if cur_range != prev_range:"
            + "\n"
            + INDENT * 4
            + "return True, f'{cur_range}_from_{prev_range}'"
            + "\n"
            + INDENT * 3
            + "else:"
            + "\n"
            + INDENT * 4
            + "break"
            + "\n"
            + INDENT
            + "return False, 'No event'"
            + "\n"
        )
        return return_str

    with open("sandbox/EventFunc.py", "a") as file:
        if first:
            file.write(file_start())
        file.write(INDENT + "found_cur_range = False\n")
        file.write(INDENT + "found_prev_range = False\n")
        file.write(range_check())

name_list_list = []
for i, config_file in enumerate(config_files):
    config_fields = ConfigParser.parse_config(config_file)
    name_list_list.append(config_fields.name_list)

name_list = [item for sublist in name_list_list for item in sublist]

for i, config_file in enumerate(config_files):
    config_fields = ConfigParser.parse_config(config_file)
    num_ranges = len(config_fields.range_list)
    num_names = len(config_fields.name_list)

    if i == 0:
        first = True
    else:
        first = False
        
    if i == len(config_files)-1:
        last = True
    else:
        last = False

    if config_fields.method_selection == "U":
        if num_ranges > 1: # TODO: 1 or 0?
            unordered(first, last, i)
        else:
            unordered_wo_ranges(first, last, i)

    elif config_fields.method_selection == "P":

        pick(first, last, i)
    elif config_fields.method_selection == "O":
        ordered()
