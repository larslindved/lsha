from typing import List
from it.polimi.hri_learn.domain.sigfeatures import ChangePoint, Event, SampledSignal, Timestamp, SignalPoint
from sandbox.EventHardcoded import event_func

def label_event(events: List[Event], signals: List[SampledSignal], t: Timestamp):

    index_curr = signals.points.timestamp.index(t)#TODO: FIX
    index_prev = index_curr - 1

    curr = signals[index_curr]
    prev = signals[index_prev]

    _, event = event_func(curr, prev)

    return event
