# BME280 Temperature Humidity Pressure Sensor

This sensor is available from Adafruit. See https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout for full documentation. 

## Usage
1. Install the Adafruit BME280 library system-wide: https://github.com/adafruit/Adafruit_CircuitPython_BME280

2. Run ``reader.py`` directly to display sensor values on stdout:
   
3. Replace the **exec_cmd** parameter in ``module.conf`` with the full path to ``reader.py``, then copy ``module.conf`` to ``/etc/joule/module_configs`` to add this module to Joule. 

.. code-block:: shell

    nano module.conf # edit exec_cmd parameter
    sudo cp module.conf /etc/joule/module_configs/bme280.conf
    sudo service joule restart
    joule module list # ensure BME280 Reader is listed in the output
    
