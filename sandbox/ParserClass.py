import os
from dataclasses import dataclass
from pathlib import Path
import csv
from typing import List, Tuple, Optional
import time
import pandas as pd


from it.polimi.hri_learn.domain.sigfeatures import (
    ChangePoint,
    Event,
    SampledSignal,
    Timestamp,
    SignalPoint,
)


def not_input(input_line):
    try:
        # TODO: make less cowboy.
        blank = input_line.split()[0]
        if input_line[0] == "#":
            return True
    except IndexError:
        return True


def is_this(input_line, line_name):
    if input_line.split()[0] == line_name:
        return True


@dataclass
class ConfigParser:
    data_path: os.path
    clean_input: str
    method_selection: str
    data_column_index: int
    timestamp_index: int
    range_list: List
    name_list: List
    distance: int

    @classmethod
    def parse_config(cls, config_path: Path):
        with open(config_path) as conf:
            for i, line in enumerate(conf):
                if not_input(line):
                    continue
                elif is_this(line, "data_path:"):
                    data_path = line.split()[1]                        
                elif is_this(line, "method_selection:"):
                    method_selection = line.split()[1]
                elif is_this(line, "data_column_index:"):
                    data_column_index = int(line.split()[1])
                elif is_this(line, "timestamp_index:"):
                    timestamp_index = int(line.split()[1])
                elif is_this(line, "clean_input:"):
                    clean_input = line.split()[1]
                    if clean_input == "T":
                        df = pd.read_csv(data_path)
                        now = str(int(time.time()))
                        out_file = f"{now}.csv"
                        df.drop_duplicates(
                            subset=df.columns[timestamp_index-1],            # Which columns to consider 
                            keep='first',           # Which duplicate record to keep
                            inplace=True,          # Whether to drop in place
                            ignore_index=False      # Whether to relabel the index
                        )
                        print(df.to_string())
                        df.to_csv(out_file)
                        data_path=os.path.normpath(out_file)
                elif is_this(line, "range_list:"):
                    range_list_temp = line.split()
                    del range_list_temp[::2]
                    range_list_temp = [float(i) for i in range_list_temp]
                    range_list = []
                    for i in range(0, len(range_list_temp), 2):
                        if i > 0 and range_list_temp[i - 1] != range_list_temp[i]:
                            raise ValueError(
                                f"Ranges in range_list should be continuous, {range_list_temp[i-1]} and {range_list_temp[i]} are not."
                            )
                        range_list.append([range_list_temp[i], range_list_temp[i + 1]])
                    continue
                elif is_this(line, "name_list:"):
                    name_list = line.split()
                    name_list.pop(0)
                    continue
                elif is_this(line, "distance:"):
                    distance = int(line.split()[1])
                    continue
                else:
                    raise Exception(
                        f"Sorry, ConfigFile.txt has a wrong format: {line} is not known, did you remeber the colon sign?."
                    )

            if len(range_list) < 1 and method_selection == "O":
                raise ValueError(
                    "It is not possible to use an empty range_list together with methrod_selection: O"
                )
            elif len(range_list) > 0 and len(name_list) != len(range_list):
                i = 1
                while len(name_list) != len(range_list):
                    name_list.append(f"range{i}")
                    i += 1

            return cls(
                data_path=data_path,
                clean_input=clean_input,
                method_selection=method_selection,
                data_column_index=data_column_index,
                timestamp_index=timestamp_index,
                range_list=range_list,
                name_list=name_list,
                distance=distance,
            )


@dataclass
class CsvParser:
    @classmethod
    def parse_csv(cls, csv_path: Path, data_column_index: int, ts_col: int):
        data_points: SampledSignal = SampledSignal([], label="dp")
        with open(csv_path) as csv_file:
            reader = csv.reader(csv_file, delimiter=",")

            for i, row in enumerate(reader):
                if i < 1:
                    continue
                ts = parse_ts(row[ts_col])

                try:
                    field = float(row[data_column_index].replace(",", "."))
                except ValueError:
                    try:
                        field = str(row[data_column_index].replace(",", "."))
                    except ValueError:
                        field = None
                data_points.points.append(SignalPoint(ts, field))

        return data_points


def parse_ts(ts: str):
    time = ts.split(" ")[0].split(":")
    try:
        return_var = Timestamp(1970, 1, 1, int(time[0]), int(time[1]), int(time[2]))
    except IndexError:
        raise IndexError(
            f"Timestamp seems weird, HH:MM:SS was expected, but: {ts} was read."
        )

    return return_var
