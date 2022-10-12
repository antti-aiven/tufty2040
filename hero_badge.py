from picographics import PicoGraphics, DISPLAY_TUFTY_2040
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
import random
from pimoroni import Button
from time import time
from time import sleep
#from machine import ADC, Pin
import math

#lux_pwr = Pin(27, Pin.OUT)
#lux_pwr.value(1)
#lux = ADC(26)

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
RED = display.create_pen(255, 0, 0)
BLUE = display.create_pen(0, 0, 255)
GRAY = display.create_pen(90, 90, 90)
GREEN = display.create_pen(0, 255, 0)
YELLOW = display.create_pen(255, 255, 0)
BG_1 = display.create_pen(0, 150, 0)
BG_2 = display.create_pen(0, 100, 0)
BOUNCE_COLOR = display.create_pen(255, 0, 0)

# Clear screen
display.set_pen(BLACK)
display.clear()

# Define text to show
your_name = "Antti Kurittu"
slogan = "SecOps Forever!"

# Seed the pseudorandom number generator
random.seed(time())

# Set the iterator directions
x_right = True
y_down = True
ball_x_right = False
ball_y_down = False

# Randomize starting position
x = random.randint(10,100)
y = random.randint(10,100)
ball_x = random.randint(10,100)
ball_y = random.randint(10,100)

# Set the initial blanker
x_prev = x - 1
y_prev = y - 1

# Define buttons and font
#display.set_font('bitmap16')

button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)
button_up = Button(22, invert=False)
button_down = Button(6, invert=False)

# Speed iterator
i = 1
ball_i = 1
ball_rnd_x = 1
ball_rnd_y = 1

#r_i = i
# Main loop
while True:

    if ball_x_right == True:  # Iterate x to move right
        ball_x_prev = ball_x
        ball_x = ball_x + ball_i + ball_rnd_x
    else:  # Iterate x to move left
        ball_x_prev = ball_x
        ball_x = ball_x - ball_i - ball_rnd_y

    if ball_y_down == True:  # Iterate y to go down
        ball_y_prev = ball_y
        ball_y = ball_y + ball_i + ball_rnd_x
    else:  # Iterate y to go up
        ball_y_prev = ball_y
        ball_y = ball_y - ball_i - ball_rnd_y

    if ball_x >= 310:  # Change direction if you hit x upper boundary
        ball_x_right = False
        ball_rnd_x = random.randint(1,5)
        ball_rnd_y = random.randint(1,5)
    if ball_y >= 230:  # Change direction if you hit y upper boundary
        ball_y_down = False
        ball_rnd_x = random.randint(1,3)
        ball_rnd_y = random.randint(1,3)
    if ball_x < 0:  # Change direction if you hit x lower boundary
        ball_x_right = True
        ball_rnd_x = random.randint(1,3)
        ball_rnd_y = random.randint(1,3)
    if ball_y < 0:  # Change direction if you hit y lower boundary
        ball_y_down = True
        ball_rnd = random.randint(1,5)

    if (ball_y in range(y, y + 40)) and (ball_x in range(x,x + 120)):  # 
Change direction if you hit boundary
        burst = 0
        display.set_pen(BLACK)
        display.clear()
        BOUNCE_COLOR = display.create_pen(random.randint(0,255), 
random.randint(0,255), random.randint(0,255))
        
        if ball_y_down == True:
            ball_y_down = False
            ball_y = ball_y - 10
        else:
            ball_y_down = True
            ball_y = ball_y + 10

        if ball_x_right == True:
            ball_x_right = False
            ball_x = ball_x - 10

        else:
            ball_x_right = True
            ball_x = ball_x + 10

#        display.set_pen(YELLOW)
#        while burst < 6:
#            burst = burst + 1
#            display.line(ball_x, ball_y, 0, random.randint(0,240))
#            display.line(ball_x, ball_y, 320, random.randint(0,240))
#            display.line(ball_x, ball_y, random.randint(0,320), 0)
#            display.line(ball_x, ball_y, random.randint(0,320), 240)

    display.set_pen(BLACK) # Blank the previous frame of the slogan
    display.circle(ball_x_prev, ball_y_prev, 10)
    display.set_pen(RED) #  Bouncer next frame
    display.circle(ball_x, ball_y, 10)
    display.set_pen(BLACK)
    display.circle(ball_x, ball_y, 7)

    if x_right == True:  # Iterate x to move right
        x_prev = x
        x = x + i
    else:  # Iterate x to move left
        x_prev = x
        x = x - i
    if y_down == True:  # Iterate y to go down
        y_prev = y
        y = y + i + 2
    else:  # Iterate y to go up
        y_prev = y
        y = y - i

    if x >= 200:  # Change direction if you hit x upper boundary
        x_right = False
    if y >= 200:  # Change direction if you hit y upper boundary
        y_down = False
    if x < 0:  # Change direction if you hit x lower boundary
        x_right = True
    if y < 0:  # Change direction if you hit y lower boundary
        y_down = True

    display.set_font('bitmap6')
    display.set_pen(BLACK) # Blank the previous frame of the slogan
    display.text(slogan, x_prev, y_prev, 200, 3)
    display.set_pen(BOUNCE_COLOR) #  Bouncer next frame
    display.text(slogan, x, y, 200, 3)

    display.set_font('sans')
    display.set_pen(BG_1) # Blank the previous frame of the slogan
    display.text("..............", 140, 120 + x, 200, 4, (y * 2) + x)
    display.set_pen(BG_2) #  Bouncer next frame
    display.text("..............", 120 + x, 100, 200, 4, (x * 2) + y)
    
    display.set_font('bitmap6')
    display.set_pen(RED) # Define name in CoOl CoLoRZ
    display.text(your_name, 50, 70, 200, 6)
    display.set_pen(BLUE)
    display.text(your_name, 52, 72, 200, 6)
    display.set_pen(WHITE)
    display.text(your_name, 54, 74, 200, 6)
    display.update() # Render frame

    if button_c.is_pressed:  # Reset display and speed
        display.set_pen(BLACK)
        display.clear()
        BOUNCE_COLOR = display.create_pen(255, 0, 0)
        b_floor = 1
        b_ceiling = 1
        b_divider = 1
        b_level = 1
        r = 0
        i = 1
    
    if button_b.is_pressed:  # Randomize locations
        x = random.randint(10,200)
        y = random.randint(10,200)
        if x > (200/2):
            x_right = True
        else:
            x_right = False
        if y > (200/2):
            y_down = True
        else:
            y_down = False

    if button_a.is_pressed:  # Randomize color
        BOUNCE_COLOR = display.create_pen(random.randint(0,255), 
random.randint(0,255), random.randint(0,255))

    if button_up.is_pressed:  # Add speed
        if i < 25:
            i = i + 1
            display.set_pen(WHITE)
            display.text("Speed: %s" % i, 10, 10, 200, 3)
            display.update()
            sleep(0.5)
            display.set_pen(BLACK)
            display.clear()
    if button_down.is_pressed:  # Remove speed
        if i > 1:
            i = i - 1
            display.set_pen(WHITE)
            display.text("Speed: %s" % i, 10, 10, 200, 3)
            display.update()
            sleep(0.5)
            display.set_pen(BLACK)
            display.clear()


