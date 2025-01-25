"""
A simple example showing how to handle a button press from a rotary encoder

Requires the RotaryIRQ library from https://github.com/miketeachman/micropython-rotary
"""

import time

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from rotary_irq_rp2 import RotaryIRQ
from rotary import Rotary
from collections import deque
from random import randint

# Enter the two GPIO pins you connected to data pins A and B
# Note the order of the pins isn't strict, swapping the pins
# will swap the direction of change.
step = 100
rotary = RotaryIRQ(10, 11,
                   min_val=0,
                   max_val=step,
                   range_mode = Rotary.RANGE_WRAP,
                   half_step = True,
                   )

# If you're using a Standalone Rotary Encoder instead of a module,
# you might need to enable the internal pull-ups on the Pico
# rotary = RotaryIRQ(14, 15, pull_up=True)

# Enter the pin that SW is connected to on the Pico

# Note: the encoder we're using has a built in pull-up on the push button
#  if you're using a plain rotary encoder you might want to enable the
#  built in pull-up on the Pico with:

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
OLED = SSD1306_I2C(128, 64, i2c)

directions = [[0, -1],
              [1, 0],
              [0, 1],
              [-1, 0]]
current_dir = 0
food = [0, 0]
snake = deque(list([[64, 32],
                    [64, 33],
                    [64, 34],
                    [64, 35],
                    [64, 36],
                    [64, 37],
                    [64, 38]
                    ]), 128 * 64 + 100)



def new_food_coords():
    global food
    OLED.pixel(0, 0, 1)
    while OLED.pixel(food[0], food[1]):    
        food[0] = randint(0, 127)
        food[1] = randint(0, 63)
    
    OLED.pixel(0, 0, 0)
    OLED.pixel(food[0], food[1], 1)
    OLED.show()

def extend_snake_head():
    head = snake.pop()
    snake.append(head)
    
    new_head = [(head[0] + directions[current_dir][0]) % 128,
                (head[1] + directions[current_dir][1]) % 64]
    snake.append(new_head)
    
    return new_head
    pass




def main():
    current_rotary_value = 0
    global current_dir
    global food
    global snake
    
    new_food_coords()
    
    while True:
        new_rotary_value = rotary.value()
        
        if new_rotary_value == current_rotary_value:
            pass
        elif new_rotary_value > current_rotary_value or (current_rotary_value - new_rotary_value) > step/2:
            # Snake turn right
            current_dir = (current_dir + 1) % 4
            print("TURNING CLOCKWISE")
            
        elif new_rotary_value < current_rotary_value or (new_rotary_value - current_rotary_value) < step/2:
            # Snake turn left
            current_dir = (current_dir + 3) % 4
            print("TURNING COUNTER-CLOCKWISE")
        
        # Advance the snake 1 move forward
        head = extend_snake_head()
        
        # Check for collision - 3 cases : with food or with the snake 
        # if food - snake is snake
        # if no food - snake cut tail
       
        if head[0] == food[0] and head[1] == food[1]: 
            new_food_coords()
            print("You're supposed to eat")
            
        elif OLED.pixel(head[0], head[1]) == 1:
            OLED.fill(0)
            OLED.text("YOU LOST", 34, 32, 1)
            OLED.show()
            break
        
        elif head[0] != food[0] or head[1] != food[1]: #
            tail = snake.popleft()
            OLED.pixel(tail[0], tail[1], 0)
            OLED.show()
        # if snake itself - lose haha loser
        
        OLED.pixel(head[0], head[1], 1)
        OLED.show()
        
        current_rotary_value = new_rotary_value
        time.sleep_ms(2)


while True:
    main()
    current_rotary_value = rotary.value()
    while True:
        new_value = rotary.value()
        if new_value != current_rotary_value :
            break
    OLED.fill(0)
    OLED.show()
            


