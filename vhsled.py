## control script for VHS's wall display array of WS2801 36mm Square LEDs 

import RPi.GPIO as GPIO, time, os, random
from vhsled_spi import *
from vhsled_text import *
from vhsled_colour import *

GPIO.setmode(GPIO.BCM)

#properties of our display
width = 26
height = 10
strings= ["VHS! VHS!", "Welcome to the Bunker","drink beer", "hack the planet", "42", "feed donatio", "go hack something"]
oddstrings = ["subliminal message","They Live"]


ledpixels = []
for i in range(0,width):
	ledpixels.append([0]*height)

spidev = file("/dev/spidev0.0", "w")        		
random.seed()

c = randomColor()
setFullColor(ledpixels,spidev,c)

colorwipe_snake(ledpixels,spidev,randomColor(),0.05)
colorFlashMode(ledpixels,spidev,random.randint(0,20),0.5)
colorwipe_vertical(ledpixels,spidev,randomColor(), 0.0005,1)
colorwipe_vertical(ledpixels,spidev,randomColor(), 0.0005,-1)
colorwipe_horiz(ledpixels,spidev,randomColor(),0.0005,1)
colorwipe_horiz(ledpixels,spidev,randomColor(),0.0005,-1)
rainbowCycle(ledpixels,spidev, 0.00)
rainbowBoard(ledpixels,spidev,0.0)
scrollText(ledpixels,spidev,characters, random.choice(strings),randomColor(),Color(0,0,0),0.05)



while (not os.path.exists("/home/pi/stop")):
	action = random.randint(0,6)
	if action == 0:
		colorFlashMode(ledpixels,spidev,random.randint(0,20),0.1)
	elif action == 1:
		wipe = random.choice([0,1])
		if wipe == 0:
			colorwipe_vertical(ledpixels,spidev,randomColor(), 0.0005,random.choice([-1,1]))
		elif wipe == 1:
			colorwipe_horiz(ledpixels,spidev,randomColor(),0.0005,random.choice([-1,1]))
	elif action == 2:
		rainbowCycle(ledpixels,spidev, 0.00)
	elif action == 3:
		rainbowBoard(ledpixels,spidev,0.0)
	elif action >=4 and action < 6:
		scrollText(ledpixels,spidev,characters, random.choice(strings),randomColor(),Color(0,0,0),0.05)
	elif action ==6:
		oddityroll = random.randint(0,100)
		bright_colors = [Color(255,0,0),Color(0,255,0),Color(0,0,255),Color(255,255,255)]
		if oddityroll > 95:
			scrollText(ledpixels,spidev,characters,random.choice(oddstrings),random.choice(bright_colors),random.choice(bright_colors),0.001)

spidev.close()
print "stopping led display"