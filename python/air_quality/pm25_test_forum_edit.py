import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import adafruit_pm25

#reset_pin = None
reset_pin = DigitalInOut(board.P1_35)
reset_pin.direction = Direction.OUTPUT
reset_pin.value = False

uart = busio.UART(board.TX, board.RX, baudrate=9600)
pm25 = adafruit_pm25.PM25_UART(uart, reset_pin)

print("Found PM2.5 sensor, reading data...")

while True:
    time.sleep(1)

    try:
        aqdata = pm25.read()
        # print(aqdata)
    except Exception as exception:
        print("Unable to read from sensor, retrying...", exception)
        continue

    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
