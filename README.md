# rpi-binary-clock
<img src="https://agilefrontiers.com/assets/images/binaryclock.jpg" width=320></img>
- Converting an old, broken Graymark Binary Clock to use RPi-Pico-W
- NOTE: I selected micropython over circuitpython because uPy supported the BLE chip
- I also use AdaFruit's BlueFruit app on iOS to communicate with the clock
    - in UART mode
- hard-coded to "mpy-uart"
- hard-coded UUID = `6E400001-B5A3-F393-E0A9-E50E24DCCA9E`
    - need to research how this number is created

## GPIO
- GPIO 0-3: Ones of seconds (0-9, little endian)
- GPIO 4-6: Tens of seconds (0-5, little endian)
- GPIO 7-10: Ones of minutes (0-9, little endian)
- GPIO 11-13: Tens of minutes (0-5, little endian)
- GPIO 14-17: Hours (1-12, little endian)

## FEATURES
- Bluetooth allows updating the time
    - format: HHMMSS
- Uses RTC Module for setting/getting time

## TODO
- wire circuit board
    - "risers" for RPi Pico W
    - ribbon cable to LEDs
    - ribbon cable to pushbuttons
- update BLE to use command line
    - perhaps `key=value` or `verb value`
- push buttons on the back
    - Hold
    - Slow
    - Fast
- 5V power supply?
    - battery powered currently
    - rechargeable batteries?
- Add config file (writable via BLE commands)
- Add WiFi time setting (NTP)
    - https://bhave.sh/micropython-ntp/
- Add WWVB Atomic clock time setting
- Add Date setting
- Add Timezone setting
- Add DST setting
- Add HTTP server?
- Add special "icon" displays
    - box, house, etc...

## FILES
- binary_clock.py: The main program
    - NOTE: Store as "main.py" to run at boot time
- ble_advertising.py: From uPy github repo
    - creates the bluetooth connection
- ble_simple_peripheral.py
    - creates the serial port connection
- ble_blink.py
    - exaple: toggle led with BLE
- localtime.py
    - sample of how to do the binary math etc...

## REFERENCES
- Hackster.io article on my project
    - https://www.hackster.io/news/greg-smith-gives-a-beloved-1970s-binary-clock-a-micropython-upgrade-with-a-raspberry-pi-pico-w-c814e78032a6
- Hackster.io article describing bluetooth low energy
    - https://www.hackster.io/Ramji_Patel/raspberry-pi-pico-w-and-bluetooth-low-energy-a829c7
- uPy Docs on BLE
    - https://docs.micropython.org/en/latest/library/bluetooth.html
- uPy Github Repo for BLE
    - https://github.com/micropython/micropython/tree/master/examples/bluetooth
- Graymark Binary Clock: https://www.worthpoint.com/worthopedia/vintage-binary-clock-graymark-model-19959448
- Bluefruit Connect App from AdaFruit
    - https://learn.adafruit.com/bluefruit-le-connect/ios-setup
