import os

import numpy as np

from ParserClass import Parser


# Helper class
class CodeBlock():
    def __init__(self, head, block):
        self.head = head
        self.block = block
    def __str__(self, indent=""):
        result = indent + self.head + ":\n"
        indent += "    "
        for block in self.block:
            if isinstance(block, CodeBlock):
                result += block.__str__(indent)
            else:
                result += indent + block + "\n"
        return result


data_fields = Parser.parse_config()# NOTE: unused for now

# Write function file
def MakeFile(file_name, code):
    file = open(file_name, 'w')
    file.write("from ParserClass import Parser\n")
    file.write(str(code))
    file.close()


distance_block = CodeBlock(f"if (row_index < distance)", ["return \"index too low\""])
block = CodeBlock("def event_func(all_data, row_index)",["data_fields = Parser.parse_config()", distance_block, "cur_data = all_data[row_index, data_fields.dummy_col]", "prev_data = all_data[row_index-data_fields.distance, data_fields.dummy_col]"])

MakeFile("EventFunc.py", block)