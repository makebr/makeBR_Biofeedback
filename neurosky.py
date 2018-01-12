#makeBR_Demo NeuroSky Control via MindwaveMobile library
#https://github.com/robintibor/python-mindwave-mobile

import collections, datetime
from hue import hue_control, hue_dont_log
from phue import Bridge
from mindwavemobile.MindwaveDataPoints import AttentionDataPoint, MeditationDataPoint, PoorSignalLevelDataPoint
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader

EEGReading = collections.namedtuple('EEGReading',
                                    'eegid, type, value')

ESenseValue = collections.namedtuple('ESenseValue',
                                     'timestamp, eegid, type, value')

bridge = Bridge('192.168.1.66')   # Bridge @Shop
# bridge = Bridge('192.168.0.4')      # Bridge @Home




esense_val = []
eeg_readings = []

def get_eeg_addresses():
    eegs = ['74:E5:43:D5:72:31', '20:68:9D:70:BC:23']

    print('EEG Address List:')

    for idx, eeg in enumerate(eegs):
        print('[{}] {}'.format(idx + 1, eeg))
    return eegs


def attempt_connect(eeg_addr):
    # print('EEG Address in Attempt Connect: {}'.format(eeg_addr))
    connect = False

    # Create Mindwave objects
    eeg_obj = MindwaveDataPointReader(eeg_addr)

    # Attempt connection to EEG Object
    try:
        eeg_obj.start()
    except IOError as e:
        pass
        # print('EEG Not Connected: {}'.format(eeg_addr))
    else:
        connect = True
        print('EEG Connected: {}'.format(eeg_addr))

    # return eeg_obj
    return eeg_obj, connect


def process_esense_value(data):
    esense_val.append(data)

    # Print The Reading
    timestamp = str(datetime.datetime.utcnow().strftime("%M:%S"))

    new_bright_lvl = int(round(data.value * 2.55))

    if data.type == 'Attention' and data.value != 0:
        # ToDo: return to main instead of printing and calling hue_control

        # hue_control(bridge, 1, "on", 1, new_bright_lvl)
        hue_control(bridge, 1, "on", 1, new_bright_lvl)
        note = """hue_control(bridge, 1, "on", 1, new_bright_lvl)"""

        print(note)
        print('{} EEG #{} {} {} Brightness: {}'.format(timestamp, data.eegid, data.type,
                                                         data.value, new_bright_lvl))

        # ESenseValue = collections.namedtuple('ESenseValue',
        #                                      'timestamp', 'eegid', 'type',
        #                                      'value')
    return ESenseValue(timestamp, data.eegid, data.type, data.value)

def process_poorsignal(data):
    # Print The Reading
    timestamp = str(datetime.datetime.utcnow().strftime("%M:%S"))
    print('{} EEG #{} {} {}'.format(timestamp, data.eegid, data.type, data.value))


def process_datapt(eegid, datapt):

    new_esense = False

    if datapt.__class__ is AttentionDataPoint:
        eeg_reading = EEGReading(eegid, 'Attention', datapt.attentionValue)
        # process_esense_value(eeg_reading)
        esense_val = process_esense_value(eeg_reading)

    if datapt.__class__ is MeditationDataPoint:
        eeg_reading = EEGReading(eegid, 'Meditation', datapt.meditationValue)
        # process_esense_value(eeg_reading)
        esense_val = process_esense_value(eeg_reading)

    if datapt.__class__ is PoorSignalLevelDataPoint:
        eeg_siglvl = datapt.amountOfNoise

        if eeg_siglvl == 200:
            eeg_reading = EEGReading(eegid, 'PoorSignal', eeg_siglvl)
            process_poorsignal(eeg_reading)
