# A RASPBERRY PI PICO SNAKE GAME

## Requirements
- Raspberry Pi Pico W
- A SSD1306 compatible 128x64 OLED display
- A rotary encoder

## How to use this for yourself
The project uses the micropython-rotary driver by Mike Teachman
Download the files and drop them into the Pico's folder (I used ThonnyIDE)
In main.py, line 20:
`rotary = RotaryIRQ(10, 11, ...`
and line 37:
`i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)`

You can choose to wire differently and change the pin numbers yourself, but if you don't wanna tweak the numbers in the source code, my recommendation is to wire as my basic settings.
The RotaryIRQ pins would be 10 and 11.
The display's pins would be 14 and 15.

Swapping the position of 2 rotary's pins (i.e., (10, 11) vs (11, 10)) would change the direction the rotary encoder controls the snake's turning.

After wiring and some tweaking, just run the code and have fun.
