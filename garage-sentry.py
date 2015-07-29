#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import logging as log


log.basicConfig(filename='/var/log/garage.log', level=log.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")
GPIO.setmode(GPIO.BOARD)

def sensor_event(chan):
    name = input_channels[chan]
    position = 'open' if GPIO.input(chan) else 'closed'
    if chan not in last_status or last_status['chan'] != position:
        last_status[chan] = position
        log.info("%s's door is %s", name, position)


if __name__ == '__main__':
    input_channels = {
        15: 'Dan',
        11: 'Victoria'
    }
    last_status = {}

    log.info('script started, setting up handlers')
    for chan, name in input_channels.iteritems():
        GPIO.setup(chan, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(chan, GPIO.BOTH, callback=sensor_event)
        log.info("set up handler for %s's door", name)
        sensor_event(chan)
    log.info('setup complete')

    while 1:
        time.sleep(2)
