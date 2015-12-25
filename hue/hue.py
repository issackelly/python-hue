import requests
import socket
import json
import datetime
import logging
from time import sleep
import hashlib
from colorpy import colormodels

logging.basicConfig(filename='hue.log', level=logging.DEBUG)
logger = logging.getLogger('hue')


AUTH_FAILURE_RETRIES = 6
AUTH_FAILURE_SLEEP = 10


class Hue:
    station_ip = "192.168.1.130"

    # Hue appears to expect your username to be a 32 character hash
    client_identifier = hashlib.md5("ph-%s" % socket.getfqdn()).hexdigest()

    devicetype = "python-hue"
    last_update_state = None
    is_allowed = True
    state = {}
    lights = {}
    groups = {}
    schedules = {}
    config = {}

    def request(self, *args, **kwargs):
        path = "http://%s/api/%s%s" % (
            self.station_ip,
            self.client_identifier,
            kwargs.get("path", ""),
        )
        method = kwargs.get("method", "GET")
        data = kwargs.get("data", None)

        ## Needs more error checking, currently assumes connection will work
        ## and that returns proper json.
        resp = requests.request(method, path, data=data)

        logger.debug(resp)
        logger.debug(resp.content)

        resp = json.loads(resp.content)

        logger.debug(resp)

        if isinstance(resp, list) and resp[0].get("error", None):
            error = resp[0]["error"]
            if error["type"] == 1:
                ## Try to authenticate
                if self.authenticate():
                    return self.request(*args, **kwargs)
                else:
                    raise CouldNotAuthenticate()
        else:
            self.is_authenticated = True
            return resp

    def authenticate(self, tries=AUTH_FAILURE_RETRIES):
        path = "http://%s/api" % (
            self.station_ip
        )

        ## Needs more error checking, currently assumes connection will work
        ## and that returns proper json.
        auth = {
            "devicetype": self.devicetype,
            "username": self.client_identifier
        }

        resp = requests.post(path, data=json.dumps(auth))
        logger.debug(resp)
        logger.debug(resp.content)

        resp = json.loads(resp.content)

        logger.debug(resp)

        logger.warn("Time to go press your button!")

        if isinstance(resp, list) and resp[0].get("error", None):
            logger.debug(resp[0]["error"])
            if tries:
                sleep(AUTH_FAILURE_SLEEP)
                self.authenticate()
            else:
                raise TooManyFailures()

        return True

    def get_state(self):
        self.last_resp = self.request()
        state = self.last_resp
        logger.debug(state)

        self.state = state
        self.config = state['config']
        self.schedules = state['schedules']
        self.groups = state['groups']

        for l in state['lights']:
            light = self.lights.get("l%s" % l, None)
            if not light:
                light = ExtendedColorLight(self, l)
                self.lights["l%s" % l] = light
            light.update_state_cache(state['lights'][l])

        self.last_update_state = datetime.datetime.now()

    def get_station_ip(self):
        response = requests.get('https://www.meethue.com/api/nupnp')
        ip = json.loads(response.content)[0]["internalipaddress"]
        self.station_ip = ip


class ExtendedColorLight:
    last_status_time = None
    light_id = None
    state = {}
    hue = None

    def __init__(self, hue, light_id):
        self.hue = hue
        self.light_id = light_id

    def update_state_cache(self, values=None):
        if not values:
            values = self.hue.request(path="/lights/%s" % self.light_id)

        self.state.update(values)
        self.last_status_time = datetime.datetime.now()

    def set_state(self, state):
        self.hue.request(
            path="/lights/%s/state" % self.light_id,
            method="PUT",
            data=json.dumps(state))
        self.update_state_cache()
        return self

    def on(self, transitiontime=5):
        return self.set_state({"on": True, "transitiontime": transitiontime})

    def off(self, transitiontime=5):
        return self.set_state({"on": False, "transitiontime": transitiontime})

    def ct(self, ct, transitiontime=5):
        # set color temp in mired scale
        return self.set_state({"ct": ct, "transitiontime": transitiontime})

    def cct(self, cct, transitiontime=5):
        # set color temp in degrees kelvin
        return self.ct(1000000 / cct, transitiontime)

    def bri(self, level, transitiontime=5):
        # level between 0 and 255
        return self.set_state({"bri": level, "transitiontime": transitiontime})

    def toggle(self, transitiontime=5):
        self.update_state_cache()
        if self.state and self.state.get(
                'state', None) and self.state["state"].get("on", None):
            self.off(transitiontime)
        else:
            self.on(transitiontime)

    def alert(self, type="select"):
        return self.set_state({"alert": type})

    def xy(self, x, y, transitiontime=5):
        return self.set_state({"xy": [x, y], "transitiontime": transitiontime})

    def rgb(self, red, green=None, blue=None, transitiontime=5):
        if isinstance(red, basestring):
            # assume a hex string is passed
            rstring = red
            red = int(rstring[1:3], 16)
            green = int(rstring[3:5], 16)
            blue = int(rstring[5:], 16)

        # We need to convert the RGB value to Yxy.
        redScale = float(red) / 255.0
        greenScale = float(green) / 255.0
        blueScale = float(blue) / 255.0
        colormodels.init(
            phosphor_red=colormodels.xyz_color(0.64843, 0.33086),
            phosphor_green=colormodels.xyz_color(0.4091, 0.518),
            phosphor_blue=colormodels.xyz_color(0.167, 0.04))
        logger.debug("%s, %s, %s" % (redScale, greenScale, blueScale))
        xyz = colormodels.irgb_color(red, green, blue)
        logger.debug(xyz)
        xyz = colormodels.xyz_from_rgb(xyz)
        logger.debug(xyz)
        xyz = colormodels.xyz_normalize(xyz)
        logger.debug(xyz)

        return self.set_state(
            {"xy": [xyz[0], xyz[1]], "transitiontime": transitiontime})


class TooManyFailures(Exception):
    pass


class CouldNotAuthenticate(Exception):
    pass
