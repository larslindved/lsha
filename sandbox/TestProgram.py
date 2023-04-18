from typing import List, Dict
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from it.polimi.hri_learn.domain.sigfeatures import ChangePoint, Event, SampledSignal, Timestamp, SignalPoint
from sandbox.EventFuncHard import event_func


all_data = [[0, 0], [2, 0], [0.5, 0], [1, 0], [0.5, 0], [-0.5, 0], [1.5, 0], [2, 0]]
data_with_events = []
for index, data in enumerate(all_data):
	data_with_events.append([data, event_func(all_data, index)])

print(data_with_events)