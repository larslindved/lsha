import os
import argparse
from pathlib import Path
import numpy as np

from sandbox.ParserClass import ConfigParser

parser = argparse.ArgumentParser()
parser.add_argument("--config_file_path", "-c", type=Path, required=True)

args = parser.parse_args()
if not args.config_file_path.exists():
    raise ValueError(f"{args.config_file_path} does not exist")

config_fields = ConfigParser.parse_config(args.config_file_path)

num_ranges = len(config_fields.range_list)
INDENT = "    "


def unordered_wo_ranges():
    def wo_range():
        return_str = (
            INDENT
            + "# cur_data is equal to prev_data.\n"
            + INDENT
            + f"if (cur_data != prev_data):\n"
            + INDENT * 2
            + f"return True, cur_data \n\n"
        )
        return return_str

    with open("sandbox/EventFunc.py", "w") as file:
        file.write("def event_func(curr, prev):\n")
        file.write(INDENT + "cur_data = curr[0]\n")
        file.write(INDENT + "prev_data = prev[0]\n")
        file.write(wo_range())
        file.write(INDENT + "return False, 'No event'")


def unordered():
    def first_range():
        return_str = (
            INDENT
            + "# cur_data is in range 0.\n"
            + INDENT
            + f"if ({config_fields.range_list[0][0]} <= cur_data <= {config_fields.range_list[0][1]}):\n"
            + INDENT * 2
            + "# prev was not in range 0.\n"
            + INDENT * 2
            + f"if not ({config_fields.range_list[0][0]} <= prev_data <= {config_fields.range_list[0][1]}):\n"
            + INDENT * 3
            + f"return True, '{config_fields.name_list[0]}'\n\n"
        )
        return return_str

    def mid_ranges(ri):
        return_str = (
            INDENT
            + f"# cur_data is in range {ri}.\n"
            + INDENT
            + f"elif {config_fields.range_list[ri][0]} < cur_data <= {config_fields.range_list[ri][1]}:\n"
            + INDENT * 2
            + f"# prev_data was not in range {ri}.\n"
            + INDENT * 2
            + f"if not ({config_fields.range_list[ri][0]} < prev_data <= {config_fields.range_list[ri][1]}):\n"
            + INDENT * 3
            + f"return True, '{config_fields.name_list[ri]}'\n\n"
        )
        return return_str

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

    with open("sandbox/EventFunc.py", "w") as file:
        file.write("def event_func(curr, prev):\n")
        file.write(INDENT + "cur_data = curr[0]\n")
        file.write(INDENT + "prev_data = prev[0]\n")
        file.write(first_range())
        if num_ranges > 1:
            for nr in range(1, num_ranges):
                file.write(mid_ranges(nr))
        file.write(no_range())
        file.write(INDENT + "return False, 'No event'\n\n")
        file.write("def get_range_list():\n")
        file.write(INDENT + f"return {config_fields.range_list}\n\n")
        file.write("def get_name_list():\n")
        file.write(INDENT + f"return {config_fields.name_list}")


def ordered():
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

    with open("sandbox/EventFunc.py", "w") as file:
        file.write("def event_func(curr, prev):\n")
        file.write(INDENT + f"range_list = {config_fields.range_list}\n")
        file.write(INDENT + f"name_list = {config_fields.name_list}\n")
        file.write(INDENT + "cur_data = curr[0]\n")
        file.write(INDENT + "prev_data = prev[0]\n")
        file.write(INDENT + "found_cur_range = False\n")
        file.write(INDENT + "found_prev_range = False\n")
        file.write(range_check())


if config_fields.method_selection == "U":
    if num_ranges > 1:
        unordered()
    else:
        unordered_wo_ranges()

elif config_fields.method_selection == "O":
    ordered()
