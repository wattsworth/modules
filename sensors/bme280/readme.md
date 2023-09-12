# BME280 Temperature Humidity Pressure Sensor

This sensor is available from Adafruit. See https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout for full documentation. This code is based on a [ReaderModule](https://wattsworth.net/joule/modules.html#reader-modules) which provides a single output stream and is the simplest module type.

## Usage
1. Install the Adafruit BME280 library system-wide: https://github.com/adafruit/Adafruit_CircuitPython_BME280
```shell
sudo pip3 install adafruit-circuitpython-bme280
```

2. (*Optional*) Run ``reader.py`` directly to display sensor values on stdout:
```shell
./reader.py
# Timestamp ,  Temperature, Relative Humidity, Pressure, Altitude
# Ctrl-C to exit
```
   
3. Replace the **exec_cmd** parameter in ``module.conf`` with the full path to ``reader.py`` and change any other
   settings to customize your configuration.
   
```ini
[Main]
name = BME280 Reader
# set this to the absolute path of reader.py
exec_cmd = /path/to/reader.py <=== change this

...more configuration...
```
  
5. Copy ``module.conf`` to ``/etc/joule/module_configs`` to add this module to Joule. 

```shell
    sudo cp module.conf /etc/joule/module_configs/bme280.conf
    sudo service joule restart
    joule module list # ensure BME280 Reader is listed in the output
```
