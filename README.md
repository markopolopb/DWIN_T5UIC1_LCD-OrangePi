# DWIN T5UIC1 LCD on Orange Pi Zero 3

This repository is a modified fork of `JMSPI/DWIN_T5UIC1_LCD-OrangePi`, specifically adapted to be fully compatible with the **Orange Pi Zero 3** running Klipper. The original code relied on hardware libraries and an architecture that were incompatible with the Allwinner H616 SoC.

The code in this repository has been extensively reworked to provide stable functionality.

## Installation

These instructions assume you are running a Debian-based OS like Armbian. My OS:

```console
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
VERSION_CODENAME=bookworm
```

### Hardware Setup

1.  **Enable UART Communication:**
    First, enable an additional UART for communicating with the screen. UART5 is recommended.

    - Start orangepi-config: `sudo orangepi-config`
    - Select `System`
    - Select `Hardware`
    - Enable `ph-uart5`
    - Save and Exit

2.  **Wire the Display:**
    Connect the display to your Orange Pi Zero 3 using the following pin mapping:

    | Display Pin | Orange Pi Zero 3 GPIO | Function  |
    | ----------- | --------------------- | --------- |
    | Rx          | PH2 (Pin 8)           | UART5 TX  |
    | Tx          | PH3 (Pin 10)          | UART5 RX  |
    | Ent         | PI0 (Pin 26)          | Button    |
    | A           | PI15 (Pin 22)         | Encoder A |
    | B           | PI12 (Pin 18)         | Encoder B |
    | Vcc         | 5V (Pin 2 or 4)       | Power     |
    | Gnd         | GND (Pin 6, 9, etc.)  | Ground    |

    **Pro-tip:** Connect 5V and GND to the original cable, and tape off the 5V pin on the USB cable to the printer. This way your screen will turn off when you turn off the printer.

    **Wiring Reference Images:**

    Wire color coding used in the reference photos:

    - Rx = Purple
    - Tx = Blue
    - Ent = Orange
    - A = Yellow
    - B = White
    - Vcc = Red
    - Gnd = Green

    <img src="images/panel.png?raw=true" width="325" height="180">
    *Display panel connection points*

    <img src="images/wire1.png?raw=true" width="200" height="400">
    *Example wiring implementation*

### Software Installation

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
    sudo pip3 install git+https://github.com/PicoPlanetDev/OPi.GPIO.git
    ```

4.  **Clone This Repository:**
    Clone this repository to your device.

    ```bash
    git clone <YOUR_REPOSITORY_URL>
    # Example: git clone https://github.com/your-username/your-repo-name.git
    cd <YOUR_REPOSITORY_DIRECTORY>
    ```

5.  **Configure the Example Script:**
    This repository includes a pre-configured `run.py` example that implements the Orange Pi Zero 3-specific GPIO handling. The script uses **raw kernel GPIO numbers** and an identity mapping system to work around OPi.GPIO library limitations.

    **Key differences from the original:**

    - Uses actual kernel GPIO numbers (e.g., 79, 78, 72) instead of wiringPi pin numbers
    - Implements GPIO identity mapping for H616 compatibility
    - Includes proper shutdown handling with thread cleanup
    - Pre-configured for recommended pin layout

    **To use the example:**

    1. Edit the `API_Key` in `run.py` to match your Moonraker configuration
    2. Optionally adjust pin assignments if you used different physical pins
    3. The default configuration uses:
       - Physical pin 19 → Encoder A (GPIO 79)
       - Physical pin 18 → Encoder B (GPIO 78)
       - Physical pin 15 → Button (GPIO 72)
       - UART5 (`/dev/ttyS5`) for display communication

    **For custom configurations:**
    If you need to modify pin assignments, update the GPIO numbers in `run.py`:

    ```python
    # Example: Different pin assignment
    ENCODER_PIN_A = 79  # Your chosen kernel GPIO number
    ENCODER_PIN_B = 78  # Your chosen kernel GPIO number
    BUTTON_PIN = 72     # Your chosen kernel GPIO number
    ```

    **For reversed encoder (Voxelab Aquila):**
    Simply swap the encoder pin assignments in the script:

    ```python
    encoder_Pins = (ENCODER_PIN_B, ENCODER_PIN_A)  # Swapped order
    ```

6.  **Run the Script:**
    The main script must be run with `sudo` to access the GPIO hardware.
    ```bash
    sudo python3 ./run.py
    ```

### Run at Boot (Optional)

To automatically start the LCD interface at boot:

```bash
sudo chmod +x run.py
sudo chmod +x simpleLCD.service
sudo mv simpleLCD.service /lib/systemd/system/simpleLCD.service
sudo chmod 644 /lib/systemd/system/simpleLCD.service
sudo systemctl daemon-reload
sudo systemctl enable simpleLCD.service
sudo reboot
```

**Note:** The service includes a 30-second delay after boot to allow web services to settle. The expected path for `run.py` is `/home/orangepi/DWIN_T5UIC1_LCD/run.py`.

### Buzzer Configuration (Optional)

To enable audio feedback, add buzzer configuration to your Klipper `printer.cfg`:

1. **Copy the buzzer configuration:**

   ```bash
   cp klipper_buzzer_macro.cfg ~/printer_data/config/
   ```

2. **Include in printer.cfg:**

   ```ini
   [include klipper_buzzer_macro.cfg]
   ```

3. **Update buzzer pin:**
   Edit the pin number in `klipper_buzzer_macro.cfg` to match your hardware:

   ```ini
   # Ender 3 V2 (Creality 4.2.x boards)
   [output_pin buzzer]
   pin: PC6  # Most common for Ender 3 V2

   # Other common pins:
   # pin: PB0  # Older Creality boards
   # pin: PC9  # SKR Mini E3 boards
   ```

4. **Find your buzzer pin:**
   First, check if you already have a buzzer configured:

   ```bash
   grep -i buzzer ~/printer_data/config/printer.cfg
   ```

   If not found, consult these common pins:

   | Printer Board            | Buzzer Pin | Notes                 |
   | ------------------------ | ---------- | --------------------- |
   | Ender 3 V2 (4.2.2/4.2.7) | `PC6`      | Most common           |
   | Creality 1.1.x           | `PB0`      | Older boards          |
   | SKR Mini E3 V2/V3        | `PC9`      | Popular upgrade       |
   | RAMPS 1.4                | `ar37`     | If using Arduino pins |

5. **Test the buzzer:**
   ```gcode
   TEST_BUZZER
   ```

**Note:** If no buzzer is configured, the system will fall back to console logging without affecting functionality.

---

## Summary of Code Modifications

The original codebase was incompatible with the Orange Pi Zero 3's GPIO architecture. The following key technical changes were implemented to achieve full functionality.

1.  **GPIO Library Migration:**

    - All dependencies on the incompatible `wiringpi` library and the custom `encoder.py` class were completely removed.
    - The entire GPIO handling logic was migrated to the **`OPi.GPIO`** library, which is designed for Orange Pi boards.

2.  **Input Logic Overhaul:**

    - The original event-driven model, which relied on hardware interrupts (`wiringPiISR`), was replaced with a multi-threaded software **polling model**.
    - Two dedicated background threads were created in `dwinlcd.py`:
      1.  A **hardware polling thread (`_poll_inputs`)** continuously reads the GPIO pin states, decodes the rotary encoder signal, and detects button presses.
      2.  A **UI loop thread (`_ui_loop`)** constantly checks for events detected by the hardware thread and calls the appropriate UI rendering functions.

3.  **Pin Mapping Correction:**
    - It was determined that the Orange Pi Zero 3 uses two separate GPIO controllers, and its header pins correspond to high kernel GPIO numbers (e.g., >200).
    - An **"identity map"** mechanism was implemented in `run.py`. This uses the `CUSTOM` mode of the `OPi.GPIO` library to force it to use raw, correct kernel GPIO numbers, bypassing the library's flawed internal translation.

<img src="images/gpioreadall.png?raw=true" width="700" height="386">
*Orange Pi Zero 3 GPIO mapping output showing kernel GPIO numbers*

4.  **Encoder Sensitivity Adjustment:**
    - A configurable class attribute, `ENCODER_SENSITIVITY`, was added to the `DWIN_LCD` class.
    - The input logic was modified to require multiple physical encoder "clicks" to trigger a single UI action, resolving issues with over-sensitivity.

## Current Status

### Working Features:

**Print Menu:**

- List / Print jobs from Moonraker
- Auto switching to Print Menu on job start/end
- Display print time, progress, temperatures, and job name
- Pause / Resume / Cancel job
- Tune Menu: Print speed & temperatures

**Prepare Menu:**

- Move / Jog toolhead
- Disable steppers
- Auto Home
- Z offset (PROBE_CALIBRATE)
- Preheat
- Cooldown

**Info Menu:**

- Shows printer information

**Control Menu:**

- Temperature Menu: Full temperature control with PLA/ABS/PETG presets
- Motion Menu: Complete motion settings (Max Velocity, Acceleration, etc.)

### Recent Updates & Breaking Changes:

**🔥 Breaking Changes (v2.0):**

- **Motion Menu:** Completely rewritten - now fully functional with 5 motion settings
- **Temperature Menu:** Enhanced with PETG support and persistent JSON configuration
- **Preheat System:** All presets (PLA/ABS/PETG) now save to `preheat_settings.json`
- **Shutdown Sequence:** Improved with aggressive thread termination (`os._exit(0)`)

**✅ New Features:**

- **PETG Material Support:** Full integration in Temperature and Prepare menus
- **Persistent Settings:** Preheat configurations survive restarts via JSON file
- **Enhanced Motion Menu:** Max Velocity, Acceleration, Corner Velocity, Speed Factor, Flow Rate
- **Improved Scrolling:** Temperature menu now handles 7+ items without overlapping status bar
- **Better Shutdown:** Clean exit with LCD screen clearing and thread cleanup
- **Audio Feedback:** Full buzzer support with Klipper BEEP macro
  - Click sounds for menu navigation
  - Success/error tones for operations
  - Warning sounds for temperature alerts
- **Improved Error Handling:** Robust API error handling prevents crashes
  - Graceful handling of Moonraker API failures
  - Detailed error logging for troubleshooting
  - Automatic fallbacks for missing data
- **Fixed Boot Screen:** Restored logo display during startup
  - Proper logo positioning and loading animation
  - Resolved duplicate function definitions
  - Clean startup sequence with visual feedback

**⚠️ Configuration Changes:**

- Preheat settings now stored in `preheat_settings.json` (auto-created)
- Default PETG settings: 230°C nozzle, 70°C bed, 50% fan speed
- Motion menu uses G-code commands instead of API calls for better compatibility

### Audio System Implementation

The buzzer system auto-detects available Klipper buzzer methods:

**Method 1: BEEP Macro (Recommended)**

```gcode
BEEP FREQUENCY=1000 DURATION=0.1
```

**Method 2: SET_PIN Direct Control**

```gcode
SET_PIN PIN=buzzer VALUE=1
G4 P100  # Wait 100ms
SET_PIN PIN=buzzer VALUE=0
```

**Method 3: Console Fallback**
If no hardware buzzer is detected, sounds are logged to console.

**Klipper Configuration Required:**
Add to your `printer.cfg`:

```ini
[output_pin buzzer]
pin: !ar37  # Change to your buzzer pin
pwm: True
shutdown_value: 0
value: 0
cycle_time: 0.001

[gcode_macro BEEP]
gcode:
    {% set frequency = params.FREQUENCY|default(1000)|int %}
    {% set duration = params.DURATION|default(0.1)|float %}
    {% set pwm_value = (frequency / 2000.0)|float %}
    {% if pwm_value > 1.0 %}{% set pwm_value = 1.0 %}{% endif %}
    SET_PIN PIN=buzzer VALUE={pwm_value}
    G4 P{duration * 1000}
    SET_PIN PIN=buzzer VALUE=0
```

**Available Methods:**

- `buzzer.beep_success()` - Double high tone for successful operations
- `buzzer.beep_error()` - Low tone for errors
- `buzzer.beep_click()` - Short click for menu navigation
- `buzzer.beep_warning()` - Triple beep for warnings
- `buzzer.tone(duration_ms, frequency_hz)` - Custom tones

**Testing:** Use `TEST_BUZZER` macro to verify your setup.

---

## Credits and Acknowledgments

This project builds upon the excellent work of several open-source projects and contributors:

- **Original Project:** [JMSPI/DWIN_T5UIC1_LCD-OrangePi](https://github.com/JMSPI/DWIN_T5UIC1_LCD-OrangePi) - Direct fork base for this Orange Pi Zero 3 adaptation (part of fork chain: odwdinc → bustedlogic → SuperPi911 → JMSPI)
- **Klipper 3D Printer Firmware:** [klipper3d.org](https://www.klipper3d.org) - Advanced 3D printer firmware
- **Moonraker API:** [github.com/arksine/moonraker](https://github.com/arksine/moonraker) - Web API server for Klipper
- **OctoPrint:** [octoprint.org](https://octoprint.org/) - Web interface for 3D printers
- **OPi.GPIO Library (H616 Fork):** [github.com/PicoPlanetDev/OPi.GPIO](https://github.com/PicoPlanetDev/OPi.GPIO) - Essential GPIO library with Orange Pi Zero 3 support

### Development Note

The code modifications in this repository were developed in collaboration with AI assistance (**Gemini** and **Kiro**) to solve the specific compatibility challenges with the Orange Pi Zero 3's H616 SoC architecture.
