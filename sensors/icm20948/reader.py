#!/usr/bin/env python3

from joule.client import FilterModule
from joule.utilities import time_now
import asyncio
import numpy as np

import board
import adafruit_icm20x

# Create sensor object, using the board's default I2C bus.
i2c = board.I2C()  # uses board.SCL and board.SDA
icm = adafruit_icm20x.ICM20948(i2c)

class ICM20948Reader(FilterModule):
            
    async def run(self, parsed_args, inputs, outputs):
        # data pipes (specified in configuration file)
        accel = outputs["acceleration"]
        gyro = outputs["gyro"]
        mag = outputs["magnetometer"]
        while True:
            await accel.write(np.array([[time_now()]+list(icm.acceleration)]))
            await gyro.write(np.array([[time_now()]+list(icm.gyro)]))
            await mag.write(np.array([[time_now()]+list(icm.magnetic)]))
            await asyncio.sleep(0.5)

def main():
    f = ICM20948Reader()
    f.start()


if __name__ == "__main__":
    main()
