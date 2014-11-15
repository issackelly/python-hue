#!/Users/issackelly/Projects/python/python-hue/env/bin/python

from hue import Hue

def sleepytime():
    h = Hue()
    h.station_ip = '192.168.42.89'
    h.get_state()

    minutes = 30
    transition = minutes * 60 * 10

    h.lights['l3'].off()
    h.lights['l3'].set_state({
        "bri": 50,
        "colormode": "xy",
        "xy": [0.5, 0.4],
        "transitiontime": transition,
    })

    h.lights['l1'].off()
    h.lights['l1'].set_state({
        "bri": 50,
        "colormode": "xy",
        "xy": [0.5, 0.4]
        "transitiontime": transition
    })

    h.lights['l2'].off()
    h.lights['l3'].set_state({
        "bri": 50,
        "colormode": "xy",
        "xy": [0.5, 0.4]
        "transitiontime": transition
    })


if __name__ == "__main__":
    sleepytime()
