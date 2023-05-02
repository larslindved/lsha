from typing import List
from it.polimi.hri_learn.domain.sigfeatures import (
    ChangePoint,
    Event,
    SampledSignal,
    Timestamp,
    SignalPoint,
)
from sandbox.EventHardcoded import event_func


def label_event(events: List[Event], signals: List[SampledSignal], t: Timestamp):
    for i, pt in enumerate(signals.points):
        if pt.timestamp == t:
            index_curr = i
            break
    index_prev = index_curr - 1

    curr = [signals.points[index_curr].value]
    prev = [signals.points[index_prev].value]

    flag, event = event_func(curr, prev)

    while not flag:
        curr = [signals.points[index_curr + 1].value]
        prev = [signals.points[index_prev + 1].value]
        flag, event = event_func(curr, prev)

    return event
