import os
from dataclasses import dataclass
from pathlib import Path
import csv
from typing import List, Tuple

from it.polimi.hri_learn.domain.sigfeatures import (
    ChangePoint,
    Event,
    SampledSignal,
    Timestamp,
    SignalPoint,
)


def not_input(input_line):
    if input_line[0] == "#" or input_line[0] == " ":
        return True


def is_data_path(input_line):
    if input_line.split()[0] == "data_path:":
        return True


def is_method_selection(input_line):
    if input_line.split()[0] == "method_selection:":
        return True


def is_data_column_index(input_line):
    if input_line.split()[0] == "data_column_index:":
        return True


def is_range_list(input_line):
    if input_line.split()[0] == "range_list:":
        return True


def is_name_list(input_line):
    if input_line.split()[0] == "name_list:":
        return True


def is_distance(input_line):
    if input_line.split()[0] == "distance:":
        return True


@dataclass
class ConfigParser:
    data_path: os.path
    method_selection: str
    data_column_index: int
    range_list: list
    name_list: list
    distance: int

    @classmethod
    def parse_config(cls, config_path: Path):
        with open(config_path) as conf:
            for i, line in enumerate(conf):
                if not_input(line):
                    continue
                elif is_data_path(line):
                    data_path = line.split()[1]
                    continue
                elif is_method_selection(line):
                    method_selection = line.split()[1]
                    continue
                elif is_data_column_index(line):
                    data_column_index = int(line.split()[1])
                    continue
                elif is_range_list(line):
                    range_list_temp = line.split()
                    del range_list_temp[::2]
                    range_list_temp = [float(i) for i in range_list_temp]
                    range_list = []
                    for i in range(0, len(range_list_temp), 2):
                        range_list.append([range_list_temp[i], range_list_temp[i + 1]])
                    continue
                elif is_name_list(line):
                    name_list = line.split()
                    name_list.pop(0)
                    continue
                elif is_distance(line):
                    distance = int(line.split()[1])
                    continue
                else:
                    raise Exception("Sorry, ConfigFile.txt has a wrong format")

            if len(range_list) < 1:
                # TODO: Figure out is this should be a feature.
                pass
            elif len(name_list) != len(range_list):
                i = 1
                while len(name_list) != len(range_list):
                    name_list.append(f"range{i}")
                    i += 1

            return cls(
                data_path=data_path,
                method_selection=method_selection,
                data_column_index=data_column_index,
                range_list=range_list,
                name_list=name_list,
                distance=distance,
            )


@dataclass
class CsvParser:
    @classmethod
    def parse_csv(cls, csv_path: Path, data_column_index: int):
        data_points: SampledSignal = SampledSignal([], label="dp")
        with open(csv_path) as csv_file:
            reader = csv.reader(csv_file, delimiter=",")

            for i, row in enumerate(reader):
                if i < 1:
                    continue
                ts = parse_ts(row[2])

                try:
                    field = float(row[data_column_index].replace(",", "."))
                except ValueError:
                    field = None
                data_points.points.append(SignalPoint(ts, field))

        return data_points


def parse_ts(ts: str):
    time = ts.split(" ")[0].split(":")

    return Timestamp(1970, 1, 1, int(time[0]), int(time[1]), int(time[2]))
