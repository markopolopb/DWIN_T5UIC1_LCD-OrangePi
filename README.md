# DWIN T5UIC1 LCD on Orange Pi Zero 3

This repository is a modified fork of `JMSPI/DWIN_T5UIC1_LCD-OrangePi`, specifically adapted to be fully compatible with the **Orange Pi Zero 3** running Klipper. The original code relied on hardware libraries and an architecture that were incompatible with the Allwinner H616 SoC.

The code in this repository has been extensively reworked to provide stable functionality.

## Installation

These instructions assume you are running a Debian-based OS like Armbian.

1.  **Install System Dependencies:**
    First, install `git` and the necessary Python tools (`pip`, `python-serial`).
    ```bash
    sudo apt-get update
    sudo apt-get install python3-pip python3-serial git
    ```

2.  **Install Python Libraries:**
    Install the required Python packages using `pip`.
    ```bash
    sudo pip3 install multitimer requests
    ```

3.  **Install the Correct `OPi.GPIO` Library:**
    The standard `OPi.GPIO` library does not support the Orange Pi Zero 3. You must install a specific fork that includes the correct pin mappings for the H616 chip.
    ```bash
    sudo pip3 install git+[https://github.com/PicoPlanetDev/OPi.GPIO.git](https://github.com/PicoPlanetDev/OPi.GPIO.git)
    ```

4.  **Clone This Repository:**
    Clone this repository to your device.
    ```bash
    git clone <YOUR_REPOSITORY_URL>
    # Example: git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd <YOUR_REPOSITORY_DIRECTORY>
    ```

5.  **Run the Script:**
    The main script must be run with `sudo` to access the GPIO hardware.
    ```bash
    sudo python3 ./run.py
    ```

---
## Summary of Code Modifications

The original codebase was incompatible with the Orange Pi Zero 3's GPIO architecture. The following key technical changes were implemented to achieve full functionality.

1.  **GPIO Library Migration:**
    * All dependencies on the incompatible `wiringpi` library and the custom `encoder.py` class were completely removed.
    * The entire GPIO handling logic was migrated to the **`OPi.GPIO`** library, which is designed for Orange Pi boards.

2.  **Input Logic Overhaul:**
    * The original event-driven model, which relied on hardware interrupts (`wiringPiISR`), was replaced with a multi-threaded software **polling model**.
    * Two dedicated background threads were created in `dwinlcd.py`:
        1.  A **hardware polling thread (`_poll_inputs`)** continuously reads the GPIO pin states, decodes the rotary encoder signal, and detects button presses.
        2.  A **UI loop thread (`_ui_loop`)** constantly checks for events detected by the hardware thread and calls the appropriate UI rendering functions.

3.  **Pin Mapping Correction:**
    * It was determined that the Orange Pi Zero 3 uses two separate GPIO controllers, and its header pins correspond to high kernel GPIO numbers (e.g., >200).
    * An **"identity map"** mechanism was implemented in `run.py`. This uses the `CUSTOM` mode of the `OPi.GPIO` library to force it to use raw, correct kernel GPIO numbers, bypassing the library's flawed internal translation.

4.  **Encoder Sensitivity Adjustment:**
    * A configurable class attribute, `ENCODER_SENSITIVITY`, was added to the `DWIN_LCD` class.
    * The input logic was modified to require multiple physical encoder "clicks" to trigger a single UI action, resolving issues with over-sensitivity.

---
### Collaboration Note
### The code in this repository was prepared and modified in collaboration with the AI assistant, **Gemini**.
---

# Original README:
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

   The [wiringOP-Python library](https://github.com/orangepi-xunlong/wiringOP). Install according to instructions in your boards' user manual or the instructions in the repository.

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
Make new file run.py and copy/paste in the following (pick one).
Use /dev/ttyS5 for UART5, /dev/ttyS3 for UART3 etc.

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

If your control wheel is reversed (Voxelab Aquila) use this instead (or swap A and B cables).
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

Run with `sudo python3 ./run.py`

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
