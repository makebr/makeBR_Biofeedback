"""
makeBR Demonstration
NeuroSky EEG Control of Philips Hue Lights via eSense(r) Attention reading
January 10th, 2018
Brandon Taylor, PE
"""
import sys, signal, time
from hue import hue_dont_log, hue_attempt_connect
from phue import Bridge
from neurosky import get_eeg_addresses, attempt_connect, process_esense_value, process_poorsignal, process_datapt


def print_header():
    print('--------------------------')
    print('         EEGWork          ')
    print('--------------------------')


def main():
    print_header()

    debug = True

    hue_dont_log()            # Philips Hue
    hue_attempt_connect()     # Philips Hue

    eegs = get_eeg_addresses()

    eeg1, eeg1_connected = attempt_connect(eegs[0])
    eeg2, eeg2_connected = attempt_connect(eegs[1])

    while debug:
        if eeg1_connected:
            datapt = eeg1.readNextDataPoint()
            process_datapt(1, datapt)

        if eeg2_connected:
            datapt = eeg2.readNextDataPoint()
            process_datapt(2, datapt)


if __name__ == '__main__':
    main()
