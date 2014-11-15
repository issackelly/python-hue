#!/Users/issackelly/Projects/python/python-hue/env/bin/python

from hue import Hue

def wakemeup():
    h = Hue()
    h.station_ip = '192.168.42.89'
    h.get_state()

    minutes = 15
    transition = minutes * 60 * 10

    h.lights['l1'].off()
    h.lights['l1'].set_state({
        "on": True,
        "bri": 255,
        "transitiontime": transition
    })


if __name__ == "__main__":
    wakemeup()
