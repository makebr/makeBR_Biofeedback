#makebr_Demo Philips Hue Control via phue library

import logging
from phue import Bridge, PhueRequestTimeout

def hue_attempt_connect(bridge, group_id):

    bridge_found = False

    print('hue.py | Attempting to Connect to Phillips Hue')
    command = {'transitiontime': None,
               'bri': 255,
               'xy': [0, 0]}

    while True:
        try:
            bridge.set_group(group_id, command)
            bridge_found = True
        except PhueRequestTimeout:
            break

    return bridge_found

def hue_control(bridge, group_id, state, mood=None, bri=None, tt=None):

    # if state == "on":
    #     hue_state = True
    # elif state == "off":
    #     hue_state = False

    xy = [0, 0]

    # ToDo: Maybe a named tuple to handle scenario
    # command = {'transitiontime': tt,
    #            'on': hue_state,
    #            'bri': bri,
    #            'xy': xy}

    command = {'transitiontime': tt,
               'bri': bri,
               'xy': xy}

    bridge.set_group(group_id, command)
    # result = "Turned lights " + state + "."
    # if state == "on":
    #     result = result + " (Brightess = " + str(bri) + ", Mood = " + str(mood) + ")"
    #
    # return result

def hue_dont_log():
    logger = logging.getLogger('phue')
    logger.setLevel(logging.ERROR)
    logger.propagate = False
