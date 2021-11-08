# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
"""

import serial
import time
import digitalio
import board
import busio

from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341

from adafruit_pm25.uart import PM25_UART

import adafruit_ccs811
import adafruit_ahtx0
from adafruit_pm25.i2c import PM25_I2C

# Initialize the I2C1 ports of the PocketBeagle

i2c = board.I2C()
ccs811 = adafruit_ccs811.CCS811(i2c)
aht10 = adafruit_ahtx0.AHTx0(i2c)

# Initialize UART connection for PM2.5 sensor

rst_uart = None
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
pm25 = PM25_UART(uart, rst_uart)

# First define some constants to allow easy resizing of shapes.
BORDER = 20
FONTSIZE = 24

# Configuration for CS and DC pins (these are PiTFT defaults):
rst_LCD   = digitalio.DigitalInOut(board.P1_2)
dc_LCD    = digitalio.DigitalInOut(board.P1_4)
cs_LCD    = digitalio.DigitalInOut(board.P1_6)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create LCD display class.

disp = ili9341.ILI9341(
    spi,
    rotation=90,  # 2.2", 2.4", 2.8", 3.2" ILI9341
    cs=cs_LCD,
    dc=dc_LCD,
    rst=rst_LCD,
    baudrate=BAUDRATE,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

image = Image.new("RGB", (width, height))\

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
#draw.rectangle((0, 0, width, height), outline=0, fill=(255, 124, 186))
disp.image(image)

# First define some constants to allow easy positioning of text.
padding = 10
x = 30

# Load a TTF Font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

#-------------------------------------------------------------------------------
# Component access functions
#-------------------------------------------------------------------------------
        
def draw_readings(pm25, co2, tvoc, temp, humidity):
    # Get rendered font width and height.
    draw.rectangle((0, 0, width, height), outline=0, fill=(124, 124, 186))
    y = padding
    pm25_level = "PM 0.5: " + str(pm25) + " (um/dL)"
    co2_level = "CO2: " + str(co2) + " (PPM)"
    tvoc_level = "TVOC: " + str(tvoc) + " (PPB)"
    temp_level = "Temperature: %0.1f C" % temp
    humidity_level = "Humidity: %0.1f %%" % humidity

    draw.text((x, y), pm25_level, font=font, fill="#FFFFFF")
    y += font.getsize(pm25_level)[1]
    
    draw.text((x, y), co2_level, font=font, fill="#FFFFFF")
    y += font.getsize(co2_level)[1]
    
    draw.text((x, y), tvoc_level, font=font, fill="#FFFFFF")
    y += font.getsize(tvoc_level)[1]
    
    draw.text((x, y), temp_level, font=font, fill="#FFFFFF")
    y += font.getsize(temp_level)[1]
    
    draw.text((x, y), humidity_level, font=font, fill="#FFFFFF")
    y += font.getsize(pm25_level)[1]

    disp.image(image)
    
def pms5003_read():
    time.sleep(1)
    try:
        aqdata = pm25.read()
        return aqdata["particles 05um"]
    except RuntimeError:
        return "ERROR"
    
def ccs811_read():
    return ccs811.eco2, ccs811.tvoc
        
def aht10_read():
    return aht10.temperature, aht10.relative_humidity
    
# Main Loop:

if __name__ == '__main__':
    pm25_rd = "WAIT"
    while True:
        if pms5003_read() == "ERROR":
            pass
        elif pms5003_read() != "ERROR":
            pm25_rd = pms5003_read()
        
        co2_rd = ccs811_read()[0]
        tvoc_rd = ccs811_read()[1]
        temp_rd = aht10_read()[0]
        humi_rd = aht10_read()[1]
        draw_readings(pm25_rd, co2_rd, tvoc_rd, temp_rd, humi_rd)
    