#!/usr/bin/env python3

import asyncio
from aiohttp import web
import aiohttp_jinja2
import jinja2
import os
import numpy as np

import joule
from joule.api import Event

CSS_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'css')
JS_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'js')
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'templates')


class AMAfloatApp(joule.FilterModule):

    def custom_args(self, parser):
                grp = parser.add_argument_group("module",
                                                "module specific arguments")
                grp.add_argument("--event_stream",
                                 required=True,
                                 help="high vibration events")
                
    async def setup(self, parsed_args, app, inputs, outputs):
        loader = jinja2.FileSystemLoader(TEMPLATES_DIR)
        aiohttp_jinja2.setup(app, loader=loader)
        self.humidity=0
        self.temperature=0
        self.rms_vibration=0
        self.event_stream = await self.node.event_stream_get(parsed_args.event_stream,
                                                             create=True,
                                                             event_fields={"RMS Vibration":"numeric"})

    async def run(self, parsed_args, inputs, outputs):
        accel_stream = inputs['accelerometer']
        bme280_stream = inputs['bme280']
        # data processing...
        while True:
            # Vibration Data:
            accel_data = await accel_stream.read()
            if len(accel_data) == 0:
                print("warning: no data in accelerometer stream")
                await asyncio.sleep(1)
                continue # no data yet
            accel_stream.consume(len(accel_data)-1) # leave last sample to keep timestamps continuous
            # 1.) Remove gravity (DC component)
            vibe_data =  accel_data['data'] - np.mean(accel_data['data'],axis=0)
            # 2.) Compute RMS value
            self.rms_vibration = float(np.mean(np.sqrt(np.sum(vibe_data**2, axis=1))))
            # 3.) If vibration is higher than 1m/s^2 log the event
            if self.rms_vibration > 1:
                high_vibe_event = Event(content={'RMS Vibration': self.rms_vibration},
                                        start_time=accel_data['timestamp'][0],
                                        end_time = accel_data['timestamp'][-1])
                await self.node.event_stream_write(self.event_stream,
                                                    [high_vibe_event])
                print(f"High vibration: {self.rms_vibration} m/s^2")
            # Environment Data:
            bme280_data = await bme280_stream.read()
            bme280_stream.consume(len(bme280_data))
            self.temperature,self.humidity,_,_ = np.mean(bme280_data['data'],axis=0)
            await asyncio.sleep(1)

    def routes(self):
        return [
            web.get('/', self.index),
            web.get('/data.json', self.data),
            web.static('/assets/css', CSS_DIR),
            web.static('/assets/js', JS_DIR)
        ]

    @aiohttp_jinja2.template('index.jinja2')
    async def index(self, request):
        return {}

    # json end point for AJAX requests
    async def data(self, request):
        return web.json_response(data={'vibration': float(self.rms_vibration),
                                       'temperature': float(self.temperature),
                                       'humidity': float(self.humidity)})


def create_app(loop):
    r = AMAfloatApp()
    return r.create_dev_app(loop)

def main():
    r = AMAfloatApp()
    r.start()


if __name__ == "__main__":
    main()
