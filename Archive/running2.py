#!/usr/bin/python
# Example using a character LCD plate.
import time
import Adafruit_CharLCD as LCD

from ina219 import INA219
from ina219 import DeviceRangeError

import time
import Adafruit_MCP9808.MCP9808 as MCP9808

SHUNT_OHMS = 0.1
sensor1 = MCP9808.MCP9808()
sensor1.begin()
sensor2 = MCP9808.MCP9808(address=0x19)
sensor2.begin()

ina1 = INA219(SHUNT_OHMS)
ina1.configure()
ina2 = INA219(SHUNT_OHMS, address=0x41)
ina2.configure()

def display_data():
	temp1 =sensor1.readTempC()
	temp2 =sensor2.readTempC()
	lcd.clear()
	lcd.message('P:{0:0.0F}C'.format(temp1))
	lcd.message(' %.1fV' % ina1.voltage())
	lcd.message(' %.0fmA' % ina1.current())
	lcd.message('\n')
	lcd.message('D:{0:0.0F}C'.format(temp2))
	lcd.message(' %.1fV' % ina2.voltage())
	lcd.message(' %.0fmA' % ina2.current())

def display_track():
	f = open('/var/log/musicbox_startup.log')
	f.readline()
	for line in f:
		if "INFO:librespot::player: Loading track" in line:
			track = line[39:-2]
	f.close()
	lcd.clear()
	lcd.message(track)
	if len(track) > 16:
		print len(track)
		for i in range(len(track)-16):
			print i
			time.sleep(0.5)
			lcd.move_left()
		for i in range(len(track)-16):
			time.sleep(0.5)
			lcd.move_right()
		print track



print "Bus Voltage RPI: %.2f V" % ina1.voltage(), "     Bus Voltage DAC: %.2f V" % ina2.voltage()
print "Bus Current RPI: %.0f mA" % ina1.current(), "     Bus Current DAC: %.0f mA" % ina2.current()
temp1 =sensor1.readTempC()
temp2 =sensor2.readTempC()
print('Temperature RPI: {0:0.2F}*C'.format(temp1)), ('    Temperature DAC: {0:0.2F}*C'.format(temp2)) 


lcd = LCD.Adafruit_CharLCDPlate()

print (time.strftime("%H:%M:%S"))
print (time.strftime("%d/%m/%Y"))
# Make list of button value, text, and backlight color.
buttons = ( (LCD.SELECT, 'Select', (1,1,1)),
            (LCD.LEFT,   'Left'  , (1,0,0)),
            (LCD.UP,     'Up'    , (0,0,1)),
            (LCD.DOWN,   'Down'  , (0,1,0)),
            (LCD.RIGHT,  'Right' , (1,0,1)) )

while True:
    for button in buttons:
	while ina2.current() < 50:
		time.sleep(1)
		lcd.set_backlight(0)
	lcd.set_backlight(1)
	display_data()
	time.sleep(5)
	display_track()
	time.sleep(5)


