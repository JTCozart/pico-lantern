# Flame Ring Controller for Raspberry Pi Pico

This project drives a 16-bit circular NeoPixel ring using a Raspberry Pi Pico. It simulates different flame effects (amber, green, blue) with smooth flicker transitions and toggle modes, triggered by button input.

---

## Features

- **Amber Flame**: Flickers for 55–65 minutes or until toggled off
- **Green Flame**: Sickly green flame effect, same duration
- **Blue Flame**: Cool gas-flame effect, same duration
- **Constant Amber Mode**: Manual on/off flame without a timer
- **Smooth Flickering**: Uses interpolated color transitions for realistic flame

---

## Hardware Requirements

- Raspberry Pi Pico (MicroPython firmware installed)
- 16-LED WS2812 (NeoPixel) circular ring
- 4 push buttons (momentary, connected with pull-up)
- Appropriate resistors, wires, breadboard, or soldered PCB
- 5V power supply (USB or external)

---

## Wiring

| Function         | GPIO Pin |
|------------------|----------|
| NeoPixel Data    | GP19     |
| Amber Flame Btn  | GP4      |
| Green Flame Btn  | GP2      |
| Toggle Flame Btn | GP1      |
| Blue Flame Btn   | GP3      |
| Onboard LED      | GP25     |

---

## Setup Instructions

### 1. Flash MicroPython Firmware

1. Hold down the **BOOTSEL** button on the Pico and plug it into your computer via USB.
2. Drag and drop the `.uf2` file from the [MicroPython download page](https://micropython.org/download/rp2-pico/) onto the mounted `RPI-RP2` drive.
3. The Pico will reboot into MicroPython mode.

---

### 2. Install MicroPico VS Code Extension

1. Open **Visual Studio Code**
2. Go to **Extensions (Ctrl+Shift+X)** and search for `MicroPico`
3. Install the extension by Marius van Wyk
4. Open the command palette (`Ctrl+Shift+P`) and run:  
   `MicroPico: Configure MicroPython Device`
5. Select the COM port of your Pico and `rp2` as the MicroPython variant

---

### 3. Deploy Files to the Pico

1. Clone or copy this repo into a new VS Code workspace
2. Open the command palette and run:  
   `MicroPico: Upload Project to Device`
3. This will upload `main.py` and any modules to the Pico’s internal filesystem

> **Note:** Ensure `main.py` contains the code logic to run on boot.

---

## Usage

- Press a button to activate a flame mode
- Press the **same** button again to turn it off
- Use the constant amber flame button to manually turn on/off a flame indefinitely
- On boot, the onboard LED flashes and a red-blue-green ring animation confirms startup

---

## Customization

- Flame duration is randomized between 55 and 65 minutes
- Color logic can be adjusted in `GetFlameColorForMode(mode)`
- Flicker speed varies between transitions for realism

---

## License

MIT License. Use freely, modify as needed.
