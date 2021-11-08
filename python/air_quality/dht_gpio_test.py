import time
import adafruit_dht
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import adafruit_rgb_display.ili9341 as ili9341
import Adafruit_BBIO.GPIO as GPIO

GPIO_BASE_PATH               = "/sys/class/gpio"

# GPIO direction
IN                           = True
OUT                          = False

# GPIO output state
LOW                          = "0"
HIGH                         = "1"

# Button GPIO values
BUTTON0                      = (2, 0)           # gpio64

#set screen dimensions
WIDTH = 128
HEIGHT = 160
SPEED_HZ = 4000000

# BeagleBone Black configuration.
DC = 'P2_33'
RST = 'P2_35'
        
# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor1 = adafruit_dht.DHT11
sensor2 = adafruit_dht.DHT11

#set the temperature data pins
pin1 = "GPIO1_58"

# ------------------------------------------------------------------------
# GPIO / ADC access library
# ------------------------------------------------------------------------
import os


def gpio_setup(gpio, direction, default_value=False):
    """Setup GPIO pin
    
      * Test if GPIO exists; if not create it
      * Set direction
      * Set default value
    """
    gpio_number = str((gpio[0] * 32) + gpio[1])
    path        = "{0}/gpio{1}".format(GPIO_BASE_PATH, gpio_number)
    
    if not os.path.exists(path):
        # "echo {gpio_number} > {GPIO_BASE_PATH}/export"
        print("Create GPIO: {0}".format(gpio_number))
        with open("{0}/export".format(GPIO_BASE_PATH), 'w') as f:
            f.write(gpio_number)
    
    if direction:
        # "echo in > {path}/direction"
        with open("{0}/direction".format(path), 'w') as f:
            f.write("in")
    else:
        # "echo out > {path}/direction"
        with open("{0}/direction".format(path), 'w') as f:
            f.write("out")
        
    if default_value:
        # "echo {default_value} > {path}/value"
        with open("{0}/value".format(path), 'w') as f:
            f.write(default_value)
    
# End def


def gpio_set(gpio, value):
    """Set GPIO ouptut value."""
    gpio_number = str((gpio[0] * 32) + gpio[1])
    path        = "{0}/gpio{1}".format(GPIO_BASE_PATH, gpio_number)
    
    # "echo {value} > {path}/value"
    with open("{0}/value".format(path), 'w') as f:
        f.write(value)

# End def


def gpio_get(gpio):
    """Get GPIO input value."""
    gpio_number = str((gpio[0] * 32) + gpio[1])
    path        = "{0}/gpio{1}".format(GPIO_BASE_PATH, gpio_number)
    
    # "cat {path}/value"
    with open("{0}/value".format(path), 'r') as f:
        out = f.read()
    
    return float(out)

def show_temp():

    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = adafruit_dht.read_retry(sensor1, pin1)

    print(
            "Temp: {:.1f} C    Humidity: {}% ".format(
                temperature, humidity
            )
        )


show_temp()