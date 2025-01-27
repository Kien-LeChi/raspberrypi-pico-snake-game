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

X_LENGTH = 54
Y_LENGTH = 32

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
OLED = SSD1306_I2C(128, 64, i2c)

directions = [[0, -1],
              [1, 0],
              [0, 1],
              [-1, 0]]
current_dir = 0
snake = None
food = None

def init():
    global snake
    global food
    snake = deque(list([[32, 16],
                    [32, 17],
                    [32, 18],
                    [32, 39],
                    [32, 20]
                    ]), 128 * 64 + 100)
    food = [randint(0, X_LENGTH - 1), randint(0, Y_LENGTH - 1)]
    for y in range(0, Y_LENGTH - 1):
        draw_pixel(X_LENGTH, y, 1)
    
    
    hi_text = [[1, 0, 1, 0, 1],
               [1, 1, 1, 0, 1],
               [1, 0, 1, 0, 1]]
    
    text_pos_x = X_LENGTH + 2
    text_pos_y = 0
    
    for y, row in enumerate(hi_text):
        for x, pix in enumerate(row):
            draw_pixel(x + X_LENGTH + 2, y + 2, pix)
    
    ## For highscore it would sit at (X_LENGTH + 2, 10) -> (128, 40)
    OLED.text(f"{0}", ((X_LENGTH + 1) << 1) + 1, 13)
    OLED.show()
            

def check_pixel(x, y):
    _x = x * 2
    _y = y * 2
    return OLED.pixel(_x, _y)

def draw_pixel(x, y, color):
    _x = x * 2
    _y = y * 2
    OLED.pixel(_x, _y, color)
    OLED.pixel(_x + 1, _y, color)
    OLED.pixel(_x, _y + 1, color)
    OLED.pixel(_x + 1, _y + 1, color)
    
    OLED.show()

def new_food_coords():
    global food
    while check_pixel(food[0], food[1]):    
        food[0] = randint(0, X_LENGTH - 1)
        food[1] = randint(0, Y_LENGTH - 1)
    
    draw_pixel(food[0], food[1], 1)

def extend_snake_head():
    head = snake.pop()
    snake.append(head)
    
    new_head = [(head[0] + directions[current_dir][0]) % X_LENGTH,
                (head[1] + directions[current_dir][1]) % Y_LENGTH]
    snake.append(new_head)
    
    return new_head
    pass

def update_score():
    ## For highscore it would sit at (X_LENGTH + 2, 10) -> (128, 
    for x in range(((X_LENGTH + 1) << 1) + 1, 128):
        for y in range(13, 23):
            OLED.pixel(x, y, 0)
    
    OLED.text(f"{len(snake) - 5}", ((X_LENGTH + 1) << 1) + 1, 13)  
    OLED.show()
    
    pass


def main():
    current_rotary_value = 0
    global current_dir
    global food
    global snake
    
    new_food_coords()
    print(food[0], food[1])
    
    while True:
        new_rotary_value = rotary.value()
        update_score()
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
            update_score()
            print(food[0], food[1])
            print("You're supposed to eat")
            
        elif check_pixel(head[0], head[1]) == 1:
            OLED.fill(0)
            OLED.text("YOU LOST", 34, 10, 1)
            OLED.text(f"HI: {len(snake) - 6}", 43, 19, 1)
            OLED.text("Spin to" , 37, 35, 1)
            OLED.text("try again", 29, 43, 1)
            OLED.show()
            break
        
        elif head[0] != food[0] or head[1] != food[1]: #
            tail = snake.popleft()
            draw_pixel(tail[0], tail[1], 0)
        # if snake itself - lose haha loser
        
        draw_pixel(head[0], head[1], 1)
        
        current_rotary_value = new_rotary_value
        time.sleep_ms(80)



while True:
    init()
    main()
    
    # Restart game mechanism
    current_rotary_value = rotary.value()
    time.sleep_ms(1500)
    while True:
        new_value = rotary.value()
        if new_value != current_rotary_value :
            break
    OLED.fill(0)
    OLED.show()
            




