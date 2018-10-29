import os
import time
import Adafruit_CharLCD as LCD
from ina219 import INA219
from ina219 import DeviceRangeError
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

lcd = LCD.Adafruit_CharLCDPlate()

track_URI = ""
track_playing = ""

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
	time.sleep(5)

def display_track():
	check_spotify()
	lcd.clear()
	lcd.message(artist)
        lcd.message('\n')
	lcd.message(track)
#	if len(track) > 16:
#		for i in range(len(track)-16):
#			time.sleep(0.5)
#			lcd.move_left()
#		for i in range(len(track)-16):
#			time.sleep(0.5)
#			lcd.move_right()
#		time.sleep(2)
#	else:
	time.sleep(5)

def check_spotify():
# Get the track id from the Librespot log file
        global artist
        global track
        global track_URI
        global track_playing
        f = open('/var/log/syslog')
        f.readline()
        for line in f:
                if "spotify:track:" in line:
                        track_URI = line[-24:-2]
        f.close()
#	print track_URI,track_playing
        if track_URI != track_playing:

# Put track metadata in templog.txt
                os.system("curl https://open.spotify.com/track/" + track_URI + "> /home/pi/templog.txt")

# Get track metadata from templog.txt
                l = open('/home/pi/templog.txt')
                line = l.readline()
                line = l.readline()
                line = l.readline()
                track_start = 88
                track_end = line.find(", a song by ")
                track = line [track_start:track_end]
                artist_start = track_end + 12
                artist_end = line.find(" on Spotify</title><meta name")
                artist = line [artist_start:artist_end]
                track_playing = track_URI
                l.close()
        	if "&#039;" or "&amp;" in artist:
	                artist = artist.replace("&#039;", "'").replace("&amp;", "&")
	        if "&#039;" or "&amp;" in track:
        	        track = track.replace("&#039;", "'").replace("&amp;", "&")
	        print "Spotify:",artist,"-", track


print
print (time.strftime("%d/%m/%Y")), (time.strftime("%H:%M:%S"))
temp1 =sensor1.readTempC()
temp2 =sensor2.readTempC()
print "Bus Voltage RPI: %.2f V" % ina1.voltage(), "     Bus Voltage DAC: %.2f V" % ina2.voltage()
print "Bus Current RPI: %.0f mA" % ina1.current(), "     Bus Current DAC: %.0f mA" % ina2.current()
print('Temperature RPI: {0:0.2F}*C'.format(temp1)), ('    Temperature DAC: {0:0.2F}*C'.format(temp2)) 

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
#		lcd.set_backlight(0)
		display_data()
#	lcd.set_backlight(1)
	display_data()
	display_track()

