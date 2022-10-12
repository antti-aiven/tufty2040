from picographics import PicoGraphics, DISPLAY_TUFTY_2040

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
import random
from time import sleep
from pimoroni import Button

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
RED = display.create_pen(255, 0, 0)
GREEN = display.create_pen(0, 255, 0)
BLUE = display.create_pen(0, 0, 255)
GRAY = display.create_pen(150, 150, 150)

# Assign buttons

button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)
button_boot = Button(23, invert=True)

with open("facts.txt", "r") as f:
    facts = f.readlines()
    f.close()

random.seed(1)


# Start splash
display.set_pen(BLACK)
display.clear()
display.set_pen(BLUE)
display.set_font("bitmap8")
display.text("Hello my name is Antti", 60, 60, 200, 3)
display.set_pen(RED)
display.set_font("bitmap8")
display.text("Hello my name is Antti", 61, 61, 200, 3)
display.set_pen(GREEN)
display.set_font("bitmap8")
display.text("Hello my name is Antti", 62, 62, 200, 3)
display.update()
display.text("Press B for a random finn fact", 60, 140, 200, 2)
display.update()

while True:
    if button_b.is_pressed:
        random_fact = facts[random.randint(1, (len(facts) - 1))]
        display.set_pen(BLACK)
        display.clear()
        display.set_pen(BLUE)
        display.set_font("bitmap8")
        display.text("Hello my name is Antti", 60, 60, 200, 3)
        display.set_pen(RED)
        display.set_font("bitmap8")
        display.text("Hello my name is Antti", 61, 61, 200, 3)
        display.set_pen(GREEN)
        display.set_font("bitmap8")
        display.text("Hello my name is Antti", 62, 62, 200, 3)
        display.set_pen(WHITE)
        display.update()
        display.text("Random Finn Fact: %s" % random_fact, 60, 130, 200, 2)
        display.update()
        sleep(1)
