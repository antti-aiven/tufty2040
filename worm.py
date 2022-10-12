from picographics import PicoGraphics, DISPLAY_TUFTY_2040

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
import random
from time import sleep
from pimoroni import Button
from time import time

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
RED = display.create_pen(255, 0, 0)
GREEN = display.create_pen(0, 255, 0)
BLUE = display.create_pen(0, 0, 255)
GRAY = display.create_pen(150, 150, 150)

button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)


# Starting values
action = "move_right"
x = 0
y = 0
score = 0
pixels = []
fruits = []

# Main loop

display.set_pen(BLACK)
display.rectangle(0, 0, 320, 240)
display.update()
score = 0
snake_length = 20

f = 0
while f < 3:
    fruits.append((random.randint(10, 120), random.randint(10, 100)))
    f = f + 1

for fruit_coords in fruits:
    display.set_pen(GREEN)
    display.rectangle(fruit_coords[0] * 2, fruit_coords[1] * 2, 2, 2)

alive = True

while alive == True:
    sleep(0.01)
    if action == "move_right":  # Move right
        x = x + 1
    elif action == "move_left":  # Move left
        x = x - 1
    elif action == "move_down":  # Move down
        y = y + 1
    elif action == "move_up":  # Move up
        y = y - 1
    else:
        action == action

    if x > 160:
        x = 0
    if x < 0:
        x = 160
    if y > 120:
        y = 0
    if y < 0:
        y = 120

    display.set_pen(WHITE)
    display.rectangle(x * 2, y * 2, 2, 2)
    location = (x, y)

    if location in fruits:
        snake_length = snake_length + 20
        fruits.remove(location)
        new_fruit_x = random.randint(10, 150)
        new_fruit_y = random.randint(10, 110)
        display.set_pen(GREEN)
        display.rectangle(new_fruit_x * 2, new_fruit_y * 2, 2, 2)
        fruits.append((new_fruit_x, new_fruit_y))

    if location in pixels:
        display.set_pen(RED)
        display.set_font("bitmap8")
        display.text("You died! \nScore: %s" % snake_length, 51, 71, 200, 3)
        display.update()
        sleep(3)
        action = "move_right"
        x = 0
        y = 0
        score = 0
        pixels = []
        fruits = []
        # Main loop
        display.set_pen(BLACK)
        display.rectangle(0, 0, 320, 240)
        display.update()
        score = 0
        snake_length = 20
        f = 0

    else:
        pixels.append((x, y))

    if len(pixels) > (snake_length):
        last_section = pixels.pop(0)
        display.set_pen(BLACK)
        last_x = last_section[0]
        last_y = last_section[1]
        display.rectangle(last_x * 2, last_y * 2, 2, 2)

    display.update()

    if button_up.is_pressed:
        if action != "move_down":
            action = "move_up"
    if button_down.is_pressed:
        if action != "move_up":
            action = "move_down"
    if button_a.is_pressed:
        if action != "move_left":
            action = "move_left"
    if button_b.is_pressed:
        if action != "move_left":
            action = "move_right"
