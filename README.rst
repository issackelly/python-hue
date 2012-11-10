==========
Python-Hue
==========

Python client for the Philips Hue lighting system. I figured out almost all of
this by monitoring the traffic on my router. I then found https://github.com/alistairg/IndigoHue/blob/master/Hue.indigoPlugin/Contents/Server%20Plugin/plugin.py
which gave some clues about RGB support and the magic strings (select, lselect)
to send alerts.

Sample Usage is not docs::

    from hue import Hue;
    h = Hue(); # Initialize the class
    h.station_ip = "192.168.1.222"  # Your base station IP
    h.get_state(); # Authenticate, bootstrap your lighting system
    l = h.lights.get('l3') # get bulb #3
    l.bri(0) # Dimmest
    l.bri(255) # Brightest
    l.rgb(120, 120, 0) # [0-255 rgb values]
    l.rgb("#9af703") # Hex string
    l.on()
    l.off()
    l.toggle()
    l.alert() # short alert
    l.alert("lselect") # long alert
    l.setState({"bri": 220, "alert": "select"}) # Complex send

Have fun! Let me know how you're using it.

