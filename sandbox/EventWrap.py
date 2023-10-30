from typing import List
from it.polimi.hri_learn.domain.sigfeatures import (
    ChangePoint,
    Event,
    SampledSignal,
    Timestamp,
    SignalPoint,
)
from sandbox.EventFunc import event_func, get_name_list

def label_event(events: List[Event], signals: List[SampledSignal], t: Timestamp):
    # speed_sig = signals[1]
    # pressure_sig = signals[2]
    # speed = {pt.timestamp: (i, pt.value) for i, pt in enumerate(speed_sig.points)}
    # pressure = {pt.timestamp: (i, pt.value) for i, pt in enumerate(pressure_sig.points)}

    # NOTE: signals[1] is hardcoded to speed right now.
    signal = signals[1]
    for i, pt in enumerate(signal.points):
        if pt.timestamp == t:
            index_curr = i
            break
    index_prev = index_curr - 1

    curr = [signal.points[index_curr].value]
    prev = [signal.points[index_prev].value]

    flag, event = event_func(curr, prev)

    while not flag:
        index_prev = index_curr
        index_curr += 1

        curr = [signal.points[index_curr].value]
        prev = [signal.points[index_prev].value]
        flag, event = event_func(curr, prev)
    print(f"DEBUG: cur val = {curr}, event = {event}")
    return events[get_name_list().index(event)]
