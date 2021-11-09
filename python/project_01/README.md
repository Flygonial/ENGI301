This is the implementation code for assignment project_01 in the course ENGI 301.

In order to operate this code, install onto your Cloud9 IDE on your PocketBeagle. Access 192.168.7.2:3000 on your local laptop, and connect your PocketBeagle to the internet (be sure to resolve a nameserver to ensure you can specify URLs). If you have not already, then run the following lines:

sudo apt-get update
sudo pip3 install --upgrade Pillow
sudo pip3 install adafruit-circuitpython-busdevice
sudo pip3 install adafruit-circuitpython-rgb-display
sudo apt-get install ttf-dejavu -y
sudo apt-get install libopenjp2-7
sudo pip3 install adafruit-circuitpython-pm25
sudo pip3 install adafruit-circuitpython-ccs811
sudo pip3 install adafruit-circuitpython-ahtx0

Navigate to your appropriate directory and then run the following line to start the module:

sudo python3 air_quality_module.py

The device will display in order: PM0.5 (ug/m^3 density) readings, eCO2 (equivalent carbon dioxide concentration in PPM) readings, TVOC (total volatile organic compound concentration in PPB) readings, temperature readings (both celsius and farenheit), and humidity.
