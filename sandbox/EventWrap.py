import configparser

from typing import List
from it.polimi.hri_learn.domain.sigfeatures import (
    ChangePoint,
    Event,
    SampledSignal,
    Timestamp,
    SignalPoint,
)
from sandbox.EventFunc import event_func, get_name_list

def label_event(events: List[Event], signals: List[SampledSignal], t: Timestamp) -> Event:
    """
    TODO.

    Args:
        events: List[Event]
            The list of Events, known to the caller of this function.
        signals: List[SampledSignal]
            The list of SampledSignals, that each has a list of all it's SignalPoint.
        t: Timestamp
            The Timestap of an event.

    Returns:
        Event
            Found event at timestamp t.

    Raises:
        KeyError: Raises an exception.
    """
    # Acces DRIVER_SIG in ini config.
    ini_config = configparser.ConfigParser()
    ini_config.sections()
    ini_config.read('./resources/config/config.ini')
    ini_config.sections()
    DRIVER_SIG = ini_config['ENERGY CS']['DRIVER_SIG']
    
    # Make a list of the needed SampledSignal.
    sample_signals = []
    for ss in signals:
        if ss.label in DRIVER_SIG:
            sample_signals.append(ss)
    signals = sample_signals

    # Find the index of t in signals.
    signal = signals[0]
    for i, pt in enumerate(signal.points):
        if pt.timestamp == t:
            index_curr = i
            break
    # Assign the previous index.
    index_prev = index_curr - 1

    # Read the values of current and previus timestamp, for all signals.
    curr = [signal.points[index_curr].value for signal in signals]
    prev = [signal.points[index_prev].value for signal in signals]

    # Look for event, event can be a list of several events.
    flag, event = event_func(curr, prev)

    # There can be more events, for now the last one has top priority.
    top_event = event[-1]

    # # An event was found
    # if flag:
    #         # Check if the found event is of sting type, we for know ignore numerical events, because they are not triggering learning.
    #         cleaned_name_list = [name for name in get_name_list() if not name.isnumeric()]
    #         if top_event not in cleaned_name_list:
    #             flag = False
                
    # Handle timestamp duplicates
    while not flag:
        index_prev = index_curr
        index_curr += 1

        curr = [signal.points[index_curr].value for signal in signals]
        prev = [signal.points[index_prev].value for signal in signals]

        flag, event = event_func(curr, prev)
        # if flag:
        #     cleaned_name_list = [name for name in get_name_list() if not name.isnumeric()]
        #     if top_event not in cleaned_name_list:
        #         flag = False
    # breakpoint()
    print(f"DEBUG: curr = {curr}, prev = {prev}, top_event = {top_event}")
    print("DEBUG", get_name_list())
    return events[get_name_list().index(top_event)]
