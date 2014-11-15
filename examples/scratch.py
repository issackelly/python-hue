from hue import Hue
import requests
import json
import time
import logging

h = Hue()
resp = requests.get('https://www.meethue.com/api/nupnp')
ip = json.loads(resp.content)[0]["internalipaddress"]

h = Hue()
h.station_ip = ip
h.get_state()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('scratch')



SECS_PER_FRAME = 6

frames = [
    {                                                   # Frame 1
    "l1": {"on": True, "xy": [0.21, 0.04], "bri": 255},
    "l2": {"on": True, "xy": [0.21, 0.04], "bri": 255},
    "l3": {"on": True, "xy": [0.21, 0.04], "bri": 255},
    "l4": {"on": True, "xy": [0.21, 0.04], "bri": 255},
    "l5": {"on": True, "xy": [0.21, 0.04], "bri": 255},
    "l6": {"on": True, "xy": [0.21, 0.04], "bri": 255},
    },{                                                 # Frame 2
    "l1": {"on": True, "xy": [0.4, 0.4], "bri": 205},
    "l2": {"on": True, "xy": [0.4, 0.4], "bri": 205},
    "l3": {"on": True, "xy": [0.4, 0.4], "bri": 205},
    "l4": {"on": True, "xy": [0.4, 0.4], "bri": 205},
    "l5": {"on": True, "xy": [0.4, 0.4], "bri": 205},
    "l6": {"on": True, "xy": [0.4, 0.4], "bri": 205},
    },{                                                 # Frame 3
    "l1": {"on": True, "xy": [0.4, 0.5], "bri": 255},
    "l2": {"on": True, "xy": [0.4, 0.5], "bri": 255},
    "l3": {"on": True, "xy": [0.4, 0.5], "bri": 255},
    "l4": {"on": True, "xy": [0.4, 0.5], "bri": 255},
    "l5": {"on": True, "xy": [0.4, 0.5], "bri": 255},
    "l6": {"on": True, "xy": [0.4, 0.5], "bri": 255},
    },{                                                 # Frame 4
    "l1": {"on": True, "xy": [0.2, 0.05], "bri": 255},
    "l2": {"on": True, "xy": [0.2, 0.05], "bri": 255},
    "l3": {"on": True, "xy": [0.2, 0.05], "bri": 255, "transitiontime": 3 * SECS_PER_FRAME},
    "l4": {"on": True, "xy": [0.2, 0.35], "bri": 255, "transitiontime": 3 * SECS_PER_FRAME},
    "l5": {"on": True, "xy": [0.2, 0.05], "bri": 255, "transitiontime": 3 * SECS_PER_FRAME},
    "l6": {"on": True, "xy": [0.2, 0.35], "bri": 255, "transitiontime": 3 * SECS_PER_FRAME},
    },{                                                 # Frame 5
    "l1": {"on": True, "xy": [0.6, 0.15], "bri": 255},
    "l2": {"on": True, "xy": [0.6, 0.15], "bri": 255},
    "l3": None,
    "l4": None,
    "l5": None,
    "l6": {"on": True, "xy": [0.6, 0.15], "bri": 255},
    },{                                                 # Frame 6
    "l1": {"on": True, "xy": [0.6, 0.15], "bri": 255},
    "l2": {"on": True, "xy": [0.6, 0.15], "bri": 255},
    "l3": None,
    "l4": None,
    "l5": None,
    "l6": {"on": True, "xy": [0.6, 0.15], "bri": 255},
    }
]



for i, frame in enumerate(frames):
    logger.debug(i)
    for l, state in frame.iteritems():
        if isinstance(state, 'dict'):
            if not state.get("transitiontime"):
                state["transitiontime"] = SECS_PER_FRAME
            h.lights[l].set_state(state)
        elif isinstance(state, 'int'):
            time.sleep(state)
    time.sleep(SECS_PER_FRAME)
