import os
import argparse
from pathlib import Path
import numpy as np

from sandbox.ParserClass import ConfigParser

parser = argparse.ArgumentParser()
parser.add_argument("--config_file_path", type=Path)

args = parser.parse_args()
if not args.config_file_path.exists():
    raise ValueError(f"{args.config_file_path} does not exist")

config_fields = ConfigParser.parse_config(args.config_file_path)

num_ranges = len(config_fields.range_list)
indent = "    "


def first_range():
    return_str = (
        indent
        + "# cur_data is in range 0.\n"
        + indent
        + f"if ({config_fields.range_list[0][0]} < cur_data <= {config_fields.range_list[0][1]}):\n"
        + indent * 2
        + "# prev was not in range 0.\n"
        + indent * 2
        + f"if not ({config_fields.range_list[0][0]} < prev_data <= {config_fields.range_list[0][1]}):\n"
        + indent * 3
        + f"return True, '{config_fields.name_list[0]}'\n\n"
    )
    return return_str


def mid_ranges(ri):
    return_str = (
        indent
        + f"# cur_data is in range {ri}.\n"
        + indent
        + f"elif {config_fields.range_list[ri][0]} < cur_data <= {config_fields.range_list[ri][1]}:\n"
        + indent * 2
        + f"# prev_data was not in range {ri}.\n"
        + indent * 2
        + f"if not ({config_fields.range_list[ri][0]} < prev_data <= {config_fields.range_list[ri][1]}):\n"
        + indent * 3
        + f"return True, '{config_fields.name_list[ri]}'\n\n"
    )
    return return_str


def no_range():
    return_str = (
        indent
        + "# cur_data is not in any range.\n"
        + indent
        + "else:\n"
        + indent * 2
        + 'raise Exception(f"current field with value: {cur_data} does not belong to any range")\n\n'
    )
    return return_str


file = open("sandbox/EventFunc.py", "w")
file.write("def event_func(curr, prev):\n")
file.write(indent + "cur_data = curr[0]\n")
file.write(indent + "prev_data = prev[0]\n")
file.write(first_range())
if num_ranges > 1:
    for nr in range(1, num_ranges):
        file.write(mid_ranges(nr))
file.write(no_range())
file.write(indent + "return False, 'No event'")


file.close()


# distance_block = CodeBlock(f"if (row_index < distance)", ['return "index too low"'])
# block = CodeBlock(
#     "def event_func(all_data, row_index)",
#     [
#         "data_fields = Parser.parse_config()",
#         distance_block,
#         "cur_data = all_data[row_index, data_fields.dummy_col]",
#         "prev_data = all_data[row_index-data_fields.distance, data_fields.dummy_col]",
#     ],
# )

# MakeFile("EventFunc.py", block)
