# ICM20948 9 DoF IMU
This sensor is available from Adafruit. See https://learn.adafruit.com/adafruit-tdk-invensense-icm-20948-9-dof-imu/overview. This module
is based on the [FilterModule](https://wattsworth.net/joule/modules.html#filter-modules) class in order to support multiple output streams.

## Usage
1. Install the Adafruit ICM20X library system-wide: https://github.com/adafruit/Adafruit_CircuitPython_ICM20X
```shell
sudo pip3 install adafruit-circuitpython-icm20x
```

2. This module produces multiple output streams so while it can be run directly in the shell there are no
   values displayed on stdout. This configuration is mostly useful during module development or for temporary data capture:
```shell
./reader.py --module_config=./module.conf --stream_configs=./streams --live
# nothing displayed unless an error occurs
# Ctrl-C to exit
```
   
3. Replace the **exec_cmd** parameter in ``module.conf`` with the full path to ``reader.py`` and change any other
   settings to customize your configuration:
   
```ini
[Main]
name = ICM20948 Reader
# set this to the absolute path of reader.py
exec_cmd = /path/to/reader.py <=== change this

...more configuration...
```
  
5. Copy ``module.conf`` to ``/etc/joule/module_configs`` and all of the stream ``*.conf`` files to ``/etc/joule/stream_configs``
   to add this module to Joule. Modify the stream paths to match your desired configuration:

```shell
    sudo cp module.conf /etc/joule/module_configs/icm20948.conf
    sudo cp streams/*.conf /etc/joule/stream_configs
    sudo service joule restart
    joule module list # ensure ICM20948 Reader is listed in the output
```
