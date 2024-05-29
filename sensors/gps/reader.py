#!/usr/bin/env python3

from joule.client import ReaderModule
from joule.utilities import time_now
import asyncio
import numpy as np
import time
import pdb

import adafruit_gps
import serial

class GPSReader(ReaderModule):
    "Read Lat/Long data from GPS "

    def custom_args(self, parser):
        grp = parser.add_argument_group("module",
                                        "module specific arguments")
        grp.add_argument("--serial",
                         required=True,
                         help="GPS serial interface")

    async def setup(self, parsed_args, app, output):
        uart = serial.Serial(parsed_args.serial, baudrate=9600, timeout=3000)
        # Create a GPS module instance.
        self.gps = adafruit_gps.GPS(uart, debug=False)
                
        # Turn on the basic GGA and RMC info 
        self.gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        
        # Set update rate to once a second (1hz)
        self.gps.send_command(b'PMTK220,1000')
        
    async def run(self, parsed_args, output):
        while True:
            await asyncio.sleep(0.5)
            self.gps.update()

            if not self.gps.has_fix:
                print('Waiting for fix...')
                await asyncio.sleep(1)
                continue

            await output.write(np.array([[time_now(),
                                          self.gps.latitude,
                                          self.gps.longitude]]))
            print("data")


def main():
    r = GPSReader()
    r.start()


if __name__ == "__main__":
    main()
