import configparser
from typing import List, Dict, Tuple

from it.polimi.hri_learn.domain.lshafeatures import Event, FlowCondition
from it.polimi.hri_learn.domain.sigfeatures import SampledSignal, Timestamp, SignalPoint
from it.polimi.hri_learn.lstar_sha.logger import Logger
from src.ekg_extractor.mgrs.ekg_queries import SCHEMA_NAME

config = configparser.ConfigParser()
config.sections()
config.read('./resources/config/config.ini')
config.sections()

CS_VERSION = int(config['SUL CONFIGURATION']['CS_VERSION'].replace('\n', ''))

LOGGER = Logger('SUL DATA HANDLER')

POV = config['AUTO-TWIN CONFIGURATION']['POV'].lower()


def is_chg_pt(curr, prev):
    return curr[0] != prev[0] and curr[0] > 0.0


def label_event(events: List[Event], signals: List[SampledSignal], t: Timestamp):
    curr_value = [pt.value for pt in signals[0].points if pt.timestamp == t][0]

    identified_event = [e for e in events if int(e.symbol.replace('s', '')) == int(curr_value)][0]

    return identified_event


def parse_ts(ts):
    try:
        return Timestamp(ts.year, ts.month, ts.day, ts.hour, ts.mins, ts.sec)
    except AttributeError:
        return Timestamp(0, 0, 0, 0, 0, ts)


# FIXME should be generic
ACT_TO_SENSORS = {"Entrada Material Sucio": 'S1', "Cargado en carro  L+D": 'S2',
                  "Carga L+D iniciada": 'S3', "Carga L+D liberada": 'S4',
                  "Montaje": 'S5', "Producción  montada": 'S6',
                  "Composición de cargas": 'S7', "Carga de esterilizador liberada": 'S8',
                  "Carga de esterilizadorliberada": 'S9', 'Pass Sensor S1': 'S1', 'Pass Sensor S2': 'S2',
                  'Pass Sensor S3': 'S3', 'Pass Sensor S4': 'S4',
                  'Pass Sensor S5': 'S5', 'Pass Sensor S6': 'S6', 'Pass Sensor S101': 'S101',
                  'Pass Sensor S105': 'S105', 'Pass Sensor S100': 'S100', 'Pass Sensor S7': 'S7',
                  'Pass Sensor S8': 'S8', 'Pass Sensor S102': 'S102', 'Pass Sensor S104': 'S104',
                  'Pass Sensor S9': 'S9', 'Pass Sensor S10': 'S10', 'Pass Sensor S103': 'S103',
                  'Pass Sensor S11': 'S11', 'Pass Sensor S12': 'S12', 'Pass Sensor S13': 'S13',
                  'Pass Sensor S14': 'S14', 'Pass Sensor S15': 'S15',
                  'Pass Sensor S16': 'S16', 'Pass Sensor S17': 'S17',
                  'Start Break': 'S200', 'Stop Break': 'S201',
                  'Read Lock Status': 'S202', 'Read WIP amount': 'S203'}


def update_state_vector(path, state_vector: List[int], sensor_to_station: Dict[str, Tuple[int, str]]):
    if len(path) == 0:
        return
    else:
        last_sensor = ACT_TO_SENSORS[path[0].activity]
        if sensor_to_station[last_sensor][1] is None:
            return update_state_vector(path[1:], state_vector, sensor_to_station)
        elif sensor_to_station[last_sensor][1] == 'IN':
            state_vector[sensor_to_station[last_sensor][0]] += 1
        else:
            state_vector[sensor_to_station[last_sensor][0]] -= 1
        return update_state_vector(path[1:], state_vector, sensor_to_station)


def vec_to_base_x(vector: List[int], x: int):
    res = 0
    for i in range(0, len(vector)):
        res += vector[len(vector) - 1 - i] * x ** i
    return res


def parse_value(path, i):
    if path[i].activity not in ACT_TO_SENSORS:
        s_id = float(int(path[i].activity.replace('S', '')))
    else:
        sensor = ACT_TO_SENSORS[path[i].activity]
        s_id = float(int(sensor.replace('S', '')))

    if POV == 'plant':
        # determine resource state vector
        # TODO this should become system-agnostic
        if SCHEMA_NAME == 'pizzaLineV1':
            state_vector = [0, 0, 0, 0, 0]
            sensor_to_station = {'S1': (0, None), 'S2': (1, 'IN'), 'S3': (1, 'OUT'),
                                 'S7': (2, None), 'S4': (3, 'IN'), 'S5': (3, 'OUT'), 'S6': (4, None)}
        elif SCHEMA_NAME == 'pizzaLineV2':
            state_vector = [0] * 10
            sensor_to_station = {'S1': (0, None), 'S2': (1, 'IN'), 'S3': (1, 'OUT'),
                                 'S16': (2, None), 'S4': (3, 'IN'), 'S5': (3, 'OUT'),
                                 'S6': (4, 'IN'), 'S7': (4, 'OUT'), 'S8': (5, 'IN'), 'S9': (5, 'OUT'),
                                 'S10': (6, 'IN'), 'S11': (6, 'OUT'), 'S12': (6, 'OUT'),
                                 'S17': (7, None), 'S13': (8, 'OUT'), 'S14': (8, 'OUT'),
                                 'S15': (9, None)}
        else:
            state_vector = [0] * 13
            sensor_to_station = {'S1': (0, None), 'S202': (0, None),
                                 'S2': (1, 'IN'), 'S3': (1, 'OUT'), 'S100': (2, None),
                                 'S4': (3, 'IN'), 'S5': (3, 'OUT'),
                                 'S6': (4, 'IN'), 'S7': (4, 'OUT'), 'S105': (4, 'OUT'), 'S101': (5, None),
                                 'S8': (6, 'IN'), 'S9': (6, 'OUT'), 'S104': (6, 'OUT'), 'S102': (7, None),
                                 'S10': (8, 'IN'), 'S11': (8, 'OUT'), 'S12': (8, 'OUT'),
                                 'S103': (9, None), 'S16': (10, None),
                                 'S13': (11, 'IN'), 'S14': (11, 'OUT'), 'S203': (11, None), 'S15': (12, None)}

        update_state_vector(path[:i + 1], state_vector, sensor_to_station)
        idle_busy_vector = [int(v > 0) for v in state_vector]
        # print(path[i].activity, state_vector, vec_to_base_x(idle_busy_vector, 2))

        return s_id, vec_to_base_x(idle_busy_vector, 2)
    else:
        return s_id


def parse_data(path):
    sensor_id: SampledSignal = SampledSignal([], label='s_id')
    sensor_id.points.append(SignalPoint(Timestamp(0, 0, 0, 0, 0, 0), 0))
    DELTA_T = 100
    if POV == 'plant':
        state_signal: SampledSignal = SampledSignal([], label='state_vec')
        state_signal.points.append(SignalPoint(Timestamp(0, 0, 0, 0, 0, 0), 0))
    for i, ekg_event in enumerate(path):
        if ekg_event.date is None:
            ts = parse_ts(ekg_event.timestamp)
            if i < len(path) - 1:
                next_ts = parse_ts(path[i + 1].timestamp)
                new_tss = [Timestamp.from_secs(t) for t in range(ts.to_secs(), next_ts.to_secs(), DELTA_T)]
            else:
                new_tss = [ts]
        else:
            ts = parse_ts(ekg_event.date)
            if i < len(path) - 1:
                next_ts = parse_ts(path[i + 1].date)
                new_tss = [Timestamp.from_secs(t) for t in range(ts.to_secs(), next_ts.to_secs(), DELTA_T)]
            else:
                new_tss = [ts]

        # FIXME: this should be generic.
        if POV == 'plant':
            value, value_v = parse_value(path, i)
        else:
            value = parse_value(path, i)

        if i > 0 and ts == parse_ts(path[i - 1].timestamp):
            # in case there are two events at the same time, the last one overrides.
            sensor_id.points[-1].value = value
            if POV == 'plant':
                state_signal.points[-1].value = value_v
        elif len(new_tss) > 1:
            sensor_id.points.extend([SignalPoint(t, value) for t in new_tss[:-1]])
            sensor_id.points.append(SignalPoint(new_tss[-1], 0.0))
            if POV == 'plant':
                state_signal.points.extend([SignalPoint(t, value_v) for t in new_tss])
        elif len(new_tss) > 0:
            sensor_id.points.append(SignalPoint(new_tss[-1], value))
            if POV == 'plant':
                state_signal.points.append(SignalPoint(new_tss[-1], value_v))
            if i < len(path) - 1:
                next_ts = parse_ts(path[i + 1].timestamp)
                sensor_id.points.append(SignalPoint(Timestamp.from_secs(next_ts.to_secs() - 1), 0.0))
                if POV == 'plant':
                    state_signal.points.append(SignalPoint(Timestamp.from_secs(next_ts.to_secs() - 1), value_v))
        else:
            sensor_id.points.append(SignalPoint(ts, value))
            if POV == 'plant':
                state_signal.points.append(SignalPoint(ts, value_v))

    last_ts = sensor_id.points[-1].timestamp
    sensor_id.points.append(
        SignalPoint(Timestamp(last_ts.year, last_ts.month, last_ts.day, last_ts.hour, last_ts.min, last_ts.sec + 1),
                    sensor_id.points[-1].value))

    if POV == 'plant':
        state_signal.points.append(
            SignalPoint(Timestamp(last_ts.year, last_ts.month, last_ts.day, last_ts.hour, last_ts.min, last_ts.sec + 1),
                        state_signal.points[-1].value))

        return [sensor_id, state_signal]
    else:
        return [sensor_id]


def get_rand_param(segment: List[SignalPoint], flow: FlowCondition):
    return segment[0].value