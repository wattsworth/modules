#!/usr/bin/env python3

import asyncio
from aiohttp import web
import aiohttp_jinja2
import jinja2
import os
import numpy as np

import joule

CSS_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'css')
JS_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'js')
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'templates')


class AMAfloatApp(joule.FilterModule):

    async def setup(self, parsed_args, app, inputs, outputs):
        loader = jinja2.FileSystemLoader(TEMPLATES_DIR)
        aiohttp_jinja2.setup(app, loader=loader)
        self.humidity=None
        self.temperature=None
        self.rms_vibration=None

    async def run(self, parsed_args, inputs, outputs):
        accel_stream = inputs['accelerometer']
        bme280_stream = inputs['bme280']
        
        # data processing...
        while True:
            # Vibration Data:
            accel_data = await accel_stream.read()
            accel_stream.consume(len(accel_data))
            # 1.) Remove gravity (DC component)
            vibe_data =  accel_data['data'] - np.mean(accel_data['data'],axis=0)
            # 2.) Compute RMS value
            self.rms_vibration = np.mean(np.sqrt(np.sum(vibe_data**2, axis=1)))
            
            # Environment Data:
            bme280_data = await bme280_stream.read()
            bme280_stream.consume(len(bme280_data))
            self.temperature,self.humidity,_,_ = np.mean(bme280_data['data'],axis=0)
            await asyncio.sleep(0.1)

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
