"""
--------------------------------------------------------------------------------
PocketBeagle Air Quality Module (PMS5003, AHT10, CCS811, )
--------------------------------------------------------------------------------
License: MIT
Copyright 2021 ladyada for Adafruit Industries

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
Software API:

    draw_readings()
        - Updates ili9341 display with sensor readings
        
    pms5003_read()
        - Returns either PM0.5 readings or "ERROR" upon failure to read from
          sensor
        - Any of the other particle size readings can be chosen but 0.3 and 0.5
          are the most reasonable readings when unable to read the sensor the
          majority of the time
    
    ccs811_read()
        - Returns eCO2 (equivalent carbon dioxide) levels and TVOC (total
          volatile organic compound) levels in parts per million and parts per
          billion respectively
    
    aht10_read()
        - Returns temperature and humidity readings in celsius and percent
    
      
  
--------------------------------------------------------------------------
Background Information: 
 
  * Using 2.2" TFT LCD Display with Adafruit's ILI9341 library
    * https://www.adafruit.com/product/1480
    * https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/python-wiring-and-setup
    * https://cdn-shop.adafruit.com/datasheets/ILI9340.pdf
    
    * Base code (adapted below):
        * https://github.com/adafruit/Adafruit_ILI9341
        * https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/python-usage
        
  * Using PMS5003 sensor with Adafruit's PM25AQI library
        * https://www.adafruit.com/product/3686
        * https://learn.adafruit.com/pm25-air-quality-sensor/python-and-circuitpython
        * https://cdn-shop.adafruit.com/product-files/3686/plantower-pms5003-manual_v2-3.pdf
    * Base code (adapted below):
        * https://github.com/adafruit/Adafruit_PM25AQI
    
  * Using CCS811 sensor with Adafruit's ccs811 library
        * https://www.adafruit.com/product/3566
        * https://learn.adafruit.com/adafruit-ccs811-air-quality-sensor/python-circuitpython
        * https://cdn-shop.adafruit.com/product-files/3566/3566_datasheet.pdf
    * Base code (adapted below):
        * https://github.com/adafruit/Adafruit_CircuitPython_CCS811
        
  * Using AHT10 sensor with breakout board and Adafruit's AHTx0 library
        * https://www.amazon.com/Precision-Temperature-Humidity-Measurement-Communication/dp/B085WCMRSM
        * https://server4.eca.ir/eshop/AHT10/Aosong_AHT10_en_draft_0c.pdf
    * Base code (adapted below):
        * https://github.com/adafruit/Adafruit_CircuitPython_AHTx0
        * https://circuitpython.readthedocs.io/projects/ahtx0/en/latest/
    
--------------------------------------------------------------------------------
"""

# Base Imports
import time
import digitalio
import board
import busio

# Display specific imports
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341

# PMS5003 Air Quality Sensor Imports
import serial
from adafruit_pm25.uart import PM25_UART

# I2C Related Component Imports
import adafruit_ccs811
import adafruit_ahtx0

# Initialize the I2C1 ports of the PocketBeagle

i2c = board.I2C()
ccs811 = adafruit_ccs811.CCS811(i2c)
aht10 = adafruit_ahtx0.AHTx0(i2c)

# Initialize UART connection for PM2.5 sensor

rst_uart = None
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
pm25 = PM25_UART(uart, rst_uart)

# Configuration for CS and DC pins on the PocketBeagle SPI0:
rst_LCD   = digitalio.DigitalInOut(board.P1_2)
dc_LCD    = digitalio.DigitalInOut(board.P1_4)
cs_LCD    = digitalio.DigitalInOut(board.P1_6)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Note: Adjust offsets to maintain centered text if adjusting fontsize
FONTSIZE = 24

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

# Create blank image for drawing, ensure rotation to landscape:
if disp.rotation % 180 == 90:
    height = disp.width
    width = disp.height
else:
    width = disp.width
    height = disp.height

image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
#draw.rectangle((0, 0, width, height), outline=0, fill=(255, 124, 186))
disp.image(image)

# Constants that alter the positioning of text
y_offset = 30
x = 30 # x_offset

# Load Deja Vu TTF font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

#-------------------------------------------------------------------------------
# Component access functions
#-------------------------------------------------------------------------------
        
def draw_readings(pm25, co2, tvoc, temp, humidity):
    """ Updates air quality readings on the ILI9341 display.
    pm25: Takes particle concentration from pms5003_read()
    co2: Takes eCO2 concentration from ccs811_read()
    tvoc: Takes TVOC concentration from ccs811_read()
    temp: Takes temperature (C) from aht10_read()
    humidity: Takes humidity (%) from aht10_read()
    """
    # Get rendered font width and height.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    y = y_offset
    pm25_level = "PM 0.5: " + str(pm25) + " (um/dL)"
    co2_level = "CO2: " + str(co2) + " (PPM)"
    tvoc_level = "TVOC: " + str(tvoc) + " (PPB)"
    temp_level = "Temperature: %0.1f C" % temp
    # Farenheit temperature conversion
    temp_f = "Temperature: %0.1f F" % (temp * (9 / 5) + 32)
    humidity_level = "Humidity: %0.1f %%" % humidity

    # Draw each air quality reading, then offset the next one below
    draw.text((x, y), pm25_level, font=font, fill="#FFFFFF")
    y += font.getsize(pm25_level)[1]
    
    draw.text((x, y), co2_level, font=font, fill="#FFFFFF")
    y += font.getsize(co2_level)[1]
    
    draw.text((x, y), tvoc_level, font=font, fill="#FFFFFF")
    y += font.getsize(tvoc_level)[1]
    
    draw.text((x, y), temp_level, font=font, fill="#FFFFFF")
    y += font.getsize(temp_level)[1]
    
    draw.text((x, y), temp_f, font=font, fill="#FFFFFF")
    y += font.getsize(temp_f)[1]
    
    draw.text((x, y), humidity_level, font=font, fill="#FFFFFF")
    y += font.getsize(pm25_level)[1]

    disp.image(image)
    
def pms5003_read():
    """ Queries PMS5003 Sensor
    Outputs PM0.5 readings if reading is successful, "ERROR" as a str if not
    """
    time.sleep(1)
    try:
        aqdata = pm25.read()
        return aqdata["particles 05um"]
    except RuntimeError:
        return "ERROR"
    
def ccs811_read():
    """ Queries CCS811 Sensor
    Outputs eCO2 and TVOC readings in PPM and PPB respectively
    """
    return ccs811.eco2, ccs811.tvoc
        
def aht10_read():
    """ Queries AHT10 sensor
    Outputs temperature (in celsius) and humidity (%) readings
    """
    return aht10.temperature, aht10.relative_humidity

# ------------------------------------------------------------------------------
# Main Script:
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    # Default value due to unreliability of PMS5003 readings
    pm25_rd = "WAIT"
    while True:
        # Does not update display until a new valid PM0.5 reading is detected
        if pms5003_read() == "ERROR":
            pass
        elif pms5003_read() != "ERROR":
            pm25_rd = pms5003_read()
        
        # Update the CO2, TVOC, temperature, and humidity readings.
        co2_rd = ccs811_read()[0]
        tvoc_rd = ccs811_read()[1]
        temp_rd = aht10_read()[0]
        humi_rd = aht10_read()[1]
        draw_readings(pm25_rd, co2_rd, tvoc_rd, temp_rd, humi_rd)
    