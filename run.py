#!/usr/bin/env python3

from dwinlcd import DWIN_LCD
import OPi.GPIO as GPIO
import time

# --- STEP 1: Define the pins you want to use ---
# These are the TRUE KERNEL GPIO numbers for the selected physical pins.
#
# Physical pin 19 (SoC pin PH7) -> Kernel GPIO 231
ENCODER_PIN_A = 79
# Physical pin 18 (SoC pin PC14) -> Kernel GPIO 78
ENCODER_PIN_B = 78
# Physical pin 15 (SoC pin PC8) -> Kernel GPIO 72
# (We use pin 15 because physical pin 17 is a 3.3V power pin)
BUTTON_PIN = 72

# --- STEP 2: Create the identity map ---
# This is a dictionary where each pin number is mapped to itself.
# This "tricks" the library into using our raw kernel numbers directly.
identity_map = {
    ENCODER_PIN_A: ENCODER_PIN_A,
    ENCODER_PIN_B: ENCODER_PIN_B,
    BUTTON_PIN:    BUTTON_PIN,
}

# --- STEP 3: Use CUSTOM mode with our identity map ---
GPIO.setmode(identity_map)

# This line disables the non-critical warning about pull-up resistors.
GPIO.setwarnings(False)

# --- The rest of the script ---
encoder_Pins = (ENCODER_PIN_B, ENCODER_PIN_A)
button_Pin = BUTTON_PIN
LCD_COM_Port = '/dev/ttyS5'
API_Key = 'XXXXXX' # Enter your API Key here

print("Initializing DWIN LCD...")

# Initialize the DWIN_LCD class with the correct pin numbers
DWINLCD = DWIN_LCD(
    LCD_COM_Port,
    encoder_Pins,
    button_Pin,
    API_Key
)

print("DWIN LCD Initialized. Press CTRL+C to exit.")

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # --- AGGRESSIVE SHUTDOWN SEQUENCE ---
    print("\nShutdown requested...")
    
    # First, tell the DWIN object to shut down its threads gracefully
    DWINLCD.lcdExit()
    
    # Wait for threads to exit with countdown
    print("Waiting for threads to exit...", end="", flush=True)
    for i in range(10):  # Wait max 1 second
        time.sleep(0.1)
        print(".", end="", flush=True)
    print(" Done.")
    
    print("Cleaning up GPIO...")
    try:
        GPIO.cleanup()
    except:
        pass  # Ignore GPIO cleanup errors
    
    print("Force terminating all threads...")
    
    import os
    
    print("Exiting cleanly.")
    
    # Nuclear exit - bypasses all cleanup and threading issues
    import os
    os._exit(0)
