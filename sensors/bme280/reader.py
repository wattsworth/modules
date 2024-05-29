#!/usr/bin/env python3

from joule.client import ReaderModule
from joule.utilities import time_now
import asyncio
import numpy as np

import board
from adafruit_bme280 import basic as adafruit_bme280

# Create sensor object, using the board's default I2C bus.
i2c = board.I2C()  # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

class BME280Reader(ReaderModule):
    "Example reader: generates random values"

    def custom_args(self, parser):
            grp = parser.add_argument_group("module",
                                            "module specific arguments")
            grp.add_argument("--sea-level", type=float,
                             default=1013.25,
                            help="pressure at sea level (hPa)")
            
    async def run(self, parsed_args, output):
        bme280.sea_level_pressure = parsed_args.sea_level
        while True:
            await output.write(np.array([
                 [time_now(), 
                  bme280.temperature, 
                  bme280.relative_humidity, 
                  bme280.pressure, 
                  bme280.altitude]]))
            await asyncio.sleep(2)

def main():
    r = BME280Reader()
    r.start()


if __name__ == "__main__":
    main()
