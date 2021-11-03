#Jeremy Palmer
#Rice University 
#ENGI 301 - Spring 2018

#This code will take the temperature and humidity data from two DHT11 sensors
#and display them on a screen. A button is used to initialize the reading.
#See Hackster for a more detailed description of the project.


#imports
import time
import adafruit_dht
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import adafruit_rgb_display.ili9341 as ili9341
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

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
SPI_PORT = 2
SPI_DEVICE = 0

# Create TFT LCD display class.
disp = TFT.ST7735(
    DC,
    rst=RST,
    spi=SPI.SpiDev(
        SPI_PORT,
        SPI_DEVICE,
        max_speed_hz=SPEED_HZ))
        
# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor1 = Adafruit_DHT.DHT11
sensor2 = Adafruit_DHT.DHT11

#set the temperature data pins
pin2 = "GPIO1_12"
pin1 = "GPIO1_14"

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

# End def

# Define a function to create rotated text.  Unfortunately PIL doesn't have good
# native support for rotated fonts, but this function can be used to make a
# text image and rotate it so it's easy to paste in the buffer.
def draw_rotated_text(image, text, position, angle, font, fill=(255,255,255)):
    # Get rendered font width and height.
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', (width, height), (0,0,0,0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0,0), text, font=font, fill=fill)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=1)
    # Paste the text into the image, using it as a mask for transparency.
    image.paste(rotated, position, rotated)


def show_temp():

    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity1, temperature1 = Adafruit_DHT.read_retry(sensor1, pin1)
    humidity2, temperature2 = Adafruit_DHT.read_retry(sensor2, pin2)

    
    #convert temperature from C to F
    temperature1F = (temperature1*1.8) + 32
    temperature2F = (temperature2*1.8) + 32
    


    # Get a PIL Draw object to start drawing on the display buffer.
    draw = disp.draw()


    # Load default font.
    font = ImageFont.load_default()

    # Write the text on the display for the indoor and outdoor temperature
    draw_rotated_text(disp.buffer,  'Today\'s Weather:    ', (0, 150), 180, font, fill=(255,255,255))
    draw_rotated_text(disp.buffer,  'Outdoor  Temp ={0:0.1f}*F'.format(temperature2F), (0, 135), 180, font, fill=(255,255,255))
    draw_rotated_text(disp.buffer,  'Outdoor Humid ={0:0.1f} %'.format(humidity2), (0, 125), 180, font, fill=(255,255,255))

    draw_rotated_text(disp.buffer,  'Indoor  Temp ={0:0.1f}*F'.format(temperature1F), (0, 105), 180, font, fill=(255,255,255))
    draw_rotated_text(disp.buffer,  'Indoor Humid ={0:0.1f} %'.format(humidity2), (0, 95), 180, font, fill=(255,255,255))

    #make a face for fun
    draw.ellipse((10, 0, 110, 90), outline=(0,0,0), fill=(0,255,0))

    draw.ellipse((25, 45, 55, 75), outline=(255,255,255), fill=(255,0,200))
    draw.ellipse((65, 45, 95, 75), outline=(255,255,255), fill=(255,0,200))
    draw.ellipse((25, 20, 95, 40), outline=(255,255,255), fill=(0,0,200))

    # Write buffer to display hardware, must be called to make things visible on the
    # display!
    disp.display()


#set up the display and button
def setup_temp():
    gpio_setup(BUTTON0, IN)
    
    disp.begin()
    # Clear the display to a red background.
    # Can pass any tuple of red, green, blue values (from 0 to 255 each).
    disp.clear((255, 0, 0))
    disp.display()


#main driver function
if __name__ == '__main__':
    setup_temp()
    
    while (True):
        if (gpio_get(BUTTON0) == 0):
            show_temp() 
            time.sleep(15.0)
            disp.clear((255, 0, 0))
            disp.display()
        time.sleep(1.0)

    cleanup_temp()
