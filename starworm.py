from picographics import PicoGraphics, DISPLAY_TUFTY_2040

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
import random
from time import sleep
from pimoroni import Button
from time import time


def show_score(score):
    display.set_pen(BLACK)
    display.rectangle(67, 107, 180, 50)
    display.set_pen(GREEN)
    display.set_font("bitmap8")
    display.text("You died! Score: %s" % score, 70, 110, 200, 2)
    display.text("Press C to restart.", 70, 140, 200, 2)
    display.update()
    return True


# define colours

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

# Set snake tail length, initial number of stars and zero the score

snake_length = 500
stars = 50
score = 0
move = "reset"
win = False
level = 1

# Start splash
display.set_pen(BLACK)
display.clear()
display.set_pen(BLUE)
display.set_font("bitmap8")
display.text("Hello my name is Antti", 50, 70, 200, 3)
display.text("Press B to play snaek gaem1!", 60, 140, 200, 3)
display.set_pen(RED)
display.set_font("bitmap8")
display.text("Hello my name is Antti", 51, 71, 200, 3)
display.text("Press B to play snaek gaem1!", 61, 141, 200, 3)
display.set_pen(GREEN)
display.set_font("bitmap8")
display.text("Hello my name is Antti", 52, 72, 200, 3)
display.text("Press B to play snaek gaem1!", 62, 142, 200, 3)
display.update()
while True:
    if button_b.is_pressed:
        break

# Main game loop
while True:
    if move == "r":  # Move right
        x = x + 1
    elif move == "l":  # Move left
        x = x - 1
    elif move == "d":  # Move down
        y = y + 1
    elif move == "u":  # Move up
        y = y - 1
    elif move == "reset":  # Reset game state
        print("Resetting..")
        # Handle when winning a round
        if win == True:
            i = i + 500  # 500 points!
            stars = stars + 25
            level = level + 1
            win == False
        else:
            i = 0
            stars = 50
            level = 1
        display.set_pen(WHITE)  # Splash white background
        display.clear()
        display.set_pen(BLACK)  # Draw a black rectangle, leave a white border
        display.rectangle(1, 1, 318, 238)
        display.set_pen(WHITE)  # Reset to white draw color
        display.set_font("bitmap8")
        display.text("Level %s, %s stars" % (level, stars), 80, 110, 200, 2)
        display.update()  # Show text
        sleep(3)
        display.set_pen(BLACK)
        display.text("Level %s, %s stars" % (level, stars), 80, 110, 200, 2)
        display.update()  # Blank text
        random.seed(time())
        # Init variables
        obs_count = 0  # Obstacles
        bns_count = 0  # Bonuses
        move = "r"
        x = 160  # Starting position
        y = 120
        prev_x = 160
        prev_y = 120
        store_loc = []
        store_bns = []
        snake = []

        # Draw and store obstacles
        while obs_count < stars:
            display.set_pen(RED)
            obs_count = obs_count + 1
            obs_x = random.randint(1, 319)
            obs_y = random.randint(1, 239)
            display.pixel(obs_x, obs_y)
            display.update()
            store_loc.append((obs_x, obs_y))

        # Draw and store bonuses
        while bns_count < 1:
            display.set_pen(GREEN)
            bns_count = bns_count + 1
            bns_x = random.randint(10, 310)
            bns_y = random.randint(10, 230)
            display.pixel(bns_x, bns_y)
            display.update()
            store_bns.append((bns_x, bns_y))
    else:
        a = a

    # Blank the score corner
    display.set_pen(BLACK)
    display.rectangle(5, 230, 20, 8)
    display.update()

    # Draw the snake and score
    i = i + 1  # score
    display.set_pen(GRAY)
    display.pixel(prev_x, prev_y)
    display.set_pen(WHITE)
    display.pixel(x, y)
    display.text(str(i), 5, 230, 0, 1)  # Draw score
    prev_x = x
    prev_y = y
    loc = (x, y)  # Store location

    # Collision check
    if loc in store_loc:
        print("Collision with star")
        print(store_loc, loc)
        move = "reset"
        show_score(i)
        stars = 50
        level = 1
        win = False
        while True:
            if button_c.is_pressed:
                break

    if loc in snake:
        print("Collision with tail")
        print(snake, loc)
        move = "reset"
        show_score(i)
        stars = 50
        level = 1
        win = False
        while True:
            if button_c.is_pressed:
                break

    if (loc[0] >= 320) or (loc[0] <= 0) or (loc[1] >= 240) or (loc[1] <= 0):
        print("Collision with edge")
        print(snake, loc)
        move = "reset"
        show_score(i)
        stars = 50
        level = 1
        win = False
        while True:
            if button_c.is_pressed:
                break

    if loc in store_bns:
        store_bns.remove(loc)
        i = i + 500
        print("bonus!")
        if len(store_bns) == 0:
            win = True
            move = "reset"
            store_bns = []

    if len(snake) <= snake_length:  # Initial snake
        snake.append((x, y))  # Add snake section to snake
        display.update()
    else:
        snake_clear = snake.pop(0)  # Clear snake section
        snake.append((x, y))  # Add new snake section
        clr_x = snake_clear[0]  # Take the last from list
        clr_y = snake_clear[1]
        display.set_pen(BLACK)  # Blank that section
        display.pixel(clr_x, clr_y)
        display.update()

    if button_up.is_pressed:
        move = "u"

    if button_down.is_pressed:
        move = "d"

    if button_a.is_pressed:
        move = "l"

    if button_b.is_pressed:
        move = "r"

    if button_c.is_pressed:
        move = "reset"
