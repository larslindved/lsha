import configparser
import os
from typing import List

from it.polimi.hri_learn.case_studies.energy_sim.sul_functions import parse_data, get_power_param
from sandbox.EventWrap import label_event
from sandbox.EventFunc import get_range_list, get_name_list # Note: Not pretty.
from sandbox.ChgWrap import is_chg_pt
from it.polimi.hri_learn.domain.lshafeatures import Event, NormalDistribution, Trace
from it.polimi.hri_learn.domain.sigfeatures import Timestamp, SampledSignal
from it.polimi.hri_learn.domain.sulfeatures import SystemUnderLearning, RealValuedVar, FlowCondition
from it.polimi.hri_learn.lstar_sha.teacher import Teacher
# from it.polimi.hri_learn.pltr.energy_pltr import double_plot

def pwr_model(interval: List[Timestamp], P_0):
    interval = [ts.to_secs() for ts in interval]
    AVG_PW = 1.0
    return [AVG_PW] * len(interval)

# define flow conditions
on_fc: FlowCondition = FlowCondition(0, pwr_model)

# define distributions
off_distr = NormalDistribution(0, 0.0, 0.0)

model2distr = {0: []}
power = RealValuedVar([on_fc], [], model2distr, label='P')
# define events
events: List[Event] = []

config = configparser.ConfigParser()
config.sections()
config.read('./resources/config/config.ini')
config.sections()
DRIVER_SIG = config['ENERGY CS']['DRIVER_SIG']
###########################
for e in get_range_list():
    if e !=get_range_list()[-1]:
        new_guard = '{}<=w<{}'.format(e[0], e[1])
    else:
        new_guard = '{}<=w'.format(e[0])
    events.append(Event(new_guard, 'start', 'm_{}'.format(len(events))))
###########################
# for n in get_name_list():
#     events.append(Event('', 'pressure', f'p_{n}'))
spindle_off = Event('', 'stop', 'i_0')

events.append(Event('', 'load', 'l'))
events.append(Event('', 'unload', 'u'))
events.append(spindle_off)


DEFAULT_M = 0
DEFAULT_DISTR = 0

args = {'name': 'energy', 'driver': DRIVER_SIG, 'default_m': DEFAULT_M, 'default_d': DEFAULT_DISTR}
energy_sim_cs = SystemUnderLearning([power], events, parse_data, label_event, get_power_param, is_chg_pt, args=args)

# test = False
# if test:
#     TEST_PATH = '/Users/lestingi/PycharmProjects/lsha/resources/traces/simulations/ENERGY/'
#     traces_files = os.listdir(TEST_PATH)
#     traces_files = [file for file in traces_files if file.startswith('_')]

#     for file in traces_files:
#         # testing data to signals conversion
#         new_signals: List[SampledSignal] = parse_data(TEST_PATH + file)
#         # testing chg pts identification
#         chg_pts = energy_sim_cs.find_chg_pts([sig for sig in new_signals if sig.label in DRIVER_SIG])
#         # testing event labeling
#         id_events = [label_event(events, new_signals, pt.t) for pt in chg_pts[:10]]
#         # testing signal to trace conversion
#         energy_sim_cs.process_data(TEST_PATH + file)
#         trace = energy_sim_cs.timed_traces[-1]
#         print(Trace(tt=trace))
#         power_pts = new_signals[0].points
#         speed_pts = new_signals[1].points
#         pressure_pts = new_signals[2].points
#         double_plot([pt.timestamp for pt in power_pts], [pt.value for pt in power_pts],
#                     [pt.timestamp for pt in speed_pts], [pt.value for pt in speed_pts],
#                     trace, title=file, filtered=True,
#                     timestamps3=[pt.timestamp for pt in pressure_pts],
#                     v3=[pt.value for pt in pressure_pts])

#     # test segment identification
#     test_trace = Trace(energy_sim_cs.traces[0][:1])
#     segments = energy_sim_cs.get_segments(test_trace)

#     # test model identification
#     TEACHER = Teacher(energy_sim_cs)
#     identified_model: FlowCondition = TEACHER.mi_query(test_trace)
#     print(identified_model)

#     # test distr identification
#     for i, trace in enumerate(TEACHER.timed_traces):
#         for j, event in enumerate(trace.e):
#             test_trace = Trace(energy_sim_cs.traces[i][:j])
#             identified_distr = TEACHER.ht_query(test_trace, identified_model, save=True)

#             segments = energy_sim_cs.get_segments(test_trace)
#             avg_metrics = sum([TEACHER.sul.get_ht_params(segment, identified_model)
#                                for segment in segments]) / len(segments)

#             try:
#                 print('{}:\t{:.3f}->{}'.format(test_trace.events[-1].symbol, avg_metrics, identified_distr.params))
#             except IndexError:
#                 print('{}:\t{:.3f}->{}'.format(test_trace, avg_metrics, identified_distr.params))
