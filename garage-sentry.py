#!/usr/bin/env python
import RPIO
import time
import logging as log

RPIO.setmode(RPIO.BOARD)
log.basicConfig(filename='/var/log/garage.log', level=log.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")


SENSORS = {
    15: 'Dan',
    11: 'Victoria'
}

def sensor_event(chan, msg):
    name = SENSORS[chan]
    position = 'open' if RPIO.input(chan) else 'closed'
    if chan not in last_status or last_status['chan'] != position:
        last_status[chan] = position
        log.info("%s's door is %s: %s", name, position, msg)


if __name__ == '__main__':
    last_status = {}

    log.info('script started, setting up handlers')
    for chan, name in SENSORS.iteritems():
        RPIO.add_interrupt_callback(chan, sensor_event, debounce_timeout_ms=100)
        log.info("set up handler for %s's door", name)
        sensor_event(chan)
    log.info('setup complete')

    RPIO.wait_for_interrupts()
