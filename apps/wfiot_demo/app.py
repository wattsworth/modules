#!/usr/bin/env python3

import asyncio
from aiohttp import web
import aiohttp_jinja2
import jinja2
import os
from random import randint

import joule

CSS_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'css')
JS_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'js')
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'templates')


class DemoApp(joule.FilterModule):

    async def setup(self, parsed_args, app, inputs, outputs):
        loader = jinja2.FileSystemLoader(TEMPLATES_DIR)
        aiohttp_jinja2.setup(app, loader=loader)
        self.lat=None
        self.long=None
        self.knob1=None
        self.knob2=None
    async def run(self, parsed_args, inputs, outputs):
        lj_stream = inputs['labjack']
        gps_stream = inputs['gps']
        
        # data processing...
        while True:
            lj_data = await lj_stream.read(flatten=True)
            lj_stream.consume(len(lj_data))
            self.knob1=lj_data[-1,1]
            self.knob2=lj_data[-1,3]
            gps_data = await gps_stream.read(flatten=True)
            gps_stream.consume(len(gps_data))
            self.lat = gps_data[-1,1]
            self.long = gps_data[-1,2]
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
        return web.json_response(data={'lat': self.lat,
                                       'long': self.long,
                                       'knob1': self.knob1,
                                       'knob2': self.knob2})


def create_app(loop):
    r = DemoApp()
    return r.create_dev_app(loop)

def main():
    r = DemoApp()
    r.start()


if __name__ == "__main__":
    main()
