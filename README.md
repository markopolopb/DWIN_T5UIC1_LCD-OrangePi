# DWIN_T5UIC1_LCD_OPI

## Python class for the Ender 3 V2 LCD runing klipper3d with Moonraker compatible with OrangePi

https://www.klipper3d.org

https://octoprint.org/

https://github.com/arksine/moonraker


## Setup:

Tested on an OrangePi zero 2w with the official OrangePi Ubuntu Jammy image.

### Enable serial communication
  First, you have to enable an additional UART for communicating with the screen. I used UART5.

  * Start orangepi-config: `sudo orangepi-config`.
  * Select `System`.
  * Select `Hardware`.
  * Enable `ph-uart5`.
  * Save and Exit.
  

### Library requirements

   The [wiringOP-Python library](https://github.com/orangepi-xunlong/wiringOP). Install according to instructions in your boards' user manual.

  `sudo apt-get install python3-pip python3-serial git`

  `sudo pip3 install multitimer requests`

  `git clone https://github.com/JMSPI/DWIN_T5UIC1_LCD-OrangePi.git`

### Wire the display 

Might differ depending on which UART you selected and which opi you have. The wiringPi library uses wPi pin numbers. You can find those using `gpio readall`.

  * Display <-> OrangePi GPIO
  * Rx  =   wPi 5 / PH2  (UART5 TX)
  * Tx  =   wPi 7 / PH3 (UART5 RX)
  * Ent =   wPi 19 / PI0
  * A   =   wPi 20 / PI15
  * B   =   wPi 22 / PI12
  * Vcc =   5v
  * Gnd =   GND

Pro-tip: Connect 5v and GND to the original cable, and tape off the 5v pin on the usb cable to the printer. This way your screen will turn off if you turn off the printer.

I tried to take some images to help out with this: You don't have to use the color of wiring that I used:

  * Rx  =   Purple
  * Tx  =   Blue
  * Ent =   Orange
  * A   =   Yellow
  * B   =   White
  * Vcc =   Red
  * Gnd =   Green

<img src ="images/panel.png?raw=true" width="325" height="180">

<img src ="images/wire1.png?raw=true" width="200" height="400"> 

<img src ="images/opi2w pinout.png?raw=true" width="512" height="337">


### Run The Code

Enter the downloaded DWIN_T5UIC1_LCD folder.
Make new file run.py and copy/paste in the following (pick one)

For an Ender3v2
```python
#!/usr/bin/env python3
from dwinlcd import DWIN_LCD

encoder_Pins = (22, 20)
button_Pin = 19
LCD_COM_Port = '/dev/ttyS5'
API_Key = 'XXXXXX'

DWINLCD = DWIN_LCD(
	LCD_COM_Port,
	encoder_Pins,
	button_Pin,
	API_Key
)
```

If your control wheel is reversed (Voxelab Aquila) use this instead.
```python
#!/usr/bin/env python3
from dwinlcd import DWIN_LCD

encoder_Pins = (20, 22)
button_Pin = 19
LCD_COM_Port = '/dev/ttyS5'
API_Key = 'XXXXXX'

DWINLCD = DWIN_LCD(
	LCD_COM_Port,
	encoder_Pins,
	button_Pin,
	API_Key
)
```

Run with `python3 ./run.py`

# Run at boot:

	Note: Delay of 30s after boot to allow webservices to settal.
	
	path of `run.py` is expected to be `/home/orangepi/DWIN_T5UIC1_LCD/run.py`

   `sudo chmod +x run.py`
   
   `sudo chmod +x simpleLCD.service`
   
   `sudo mv simpleLCD.service /lib/systemd/system/simpleLCD.service`
   
   `sudo chmod 644 /lib/systemd/system/simpleLCD.service`
   
   `sudo systemctl daemon-reload`
   
   `sudo systemctl enable simpleLCD.service`
   
   `sudo reboot`
   
   

# Status:

## Working:

 Print Menu:
 
    * List / Print jobs from OctoPrint / Moonraker
    * Auto swiching from to Print Menu on job start / end.
    * Display Print time, Progress, Temps, and Job name.
    * Pause / Resume / Cancle Job
    * Tune Menu: Print speed & Temps

 Perpare Menu:
 
    * Move / Jog toolhead
    * Disable stepper
    * Auto Home
    * Z offset (PROBE_CALIBRATE)
    * Preheat
    * cooldown
 
 Info Menu
 
    * Shows printer info.

## Notworking:
    * Save / Loding Preheat setting, hardcode on start can be changed in menu but will not retane on restart.
    * The Control: Motion Menu
