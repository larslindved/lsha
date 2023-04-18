import argparse
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

from pathlib import Path
from typing import List, Dict

from it.polimi.hri_learn.domain.sigfeatures import ChangePoint, Event, SampledSignal, Timestamp, SignalPoint
from sandbox.EventHardcoded import event_func
from sandbox.ParserClass import ConfigParser, CsvParser
from sandbox.ChgWrap import is_chg_pt
from sandbox.EventWrap import label_event

def _find_chg_pts(driver: List[SampledSignal]):
    values = [{pt.timestamp: pt.value for pt in driver}]
    chg_pts: List[ChangePoint] = []

    prev = [sig.value for sig in driver]
    for ts in [pt.timestamp for pt in driver]:
        curr = [val_dic[ts] for val_dic in values]
        if is_chg_pt(curr, prev):
            chg_pts.append(ChangePoint(ts))
        prev = curr

    return chg_pts



parser = argparse.ArgumentParser()
parser.add_argument("--config_file_path", type=Path)

args = parser.parse_args()
if not args.config_file_path.exists():
	raise ValueError(f"{args.config_file_path} does not exist")

config_fields = ConfigParser.parse_config(args.config_file_path)

new_signals: List[SampledSignal] = CsvParser.parse_csv(config_fields.data_path, config_fields.data_column_index)

chg_pts = _find_chg_pts([sig for sig in new_signals.points])

dummy_val: List[Event] = []

#id_events = [label_event(dummy_val, new_signals, pt.t) for pt in chg_pts]


#DEBUGGING:
print("Real data: ")
for data_points in new_signals.points:
        print(data_points.value, data_points.timestamp)
print("Found: ")
for data_points in chg_pts:
        print(data_points) 





