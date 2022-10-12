from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from pimoroni import Button
import micropython
from machine import Pin
from random import seed, randint
from time import time, sleep
import gc


def draw_cell(draw_x, draw_y, color):
    """Define a function to draw scaled pixels to full screen"""
    display.set_pen(color)
    display.rectangle(draw_x * scale, draw_y * scale, scale, scale)


def compare_neighbours(x, y):
    f = set()
    # Gather neighbouring cell locations into list
    n = [
        (x - 1, y - 1),
        (x - 1, y),
        (x - 1, y + 1),
        (x, y - 1),
        (x, y + 1),
        (x + 1, y - 1),
        (x + 1, y),
        (x + 1, y + 1),
    ]
        if x < 0:
            toroid_x = int(320 / scale)
        elif x == int(320 / scale):
            toroid_x = 0
        else:
            toroid_x = x

        if y < 0:
            toroid_y = int(240 / scale)
        elif y == int(240 / scale):
            toroid_y = 0
        else:
            toroid_y = y
        f.add((toroid_x, toroid_y))
    ln = sum([x in current_gen for x in f])
    return ln  # Return number of live neighbours


def print_status():
    gen = f"Gen {i}"
    width = display.measure_text(gen, 1, 0)
    display.set_pen(red)
    display.rectangle(0, 234, (width + 10), 6)
    display.update()
    display.set_pen(white)
    display.set_font("bitmap6")
    display.text(gen, 2, 234, 320, 1)
    display.update()


led = Pin(25, Pin.OUT)
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
button_a = Button(7, invert=False)

white = display.create_pen(255, 255, 255)
black = display.create_pen(0, 0, 0)
red = display.create_pen(120, 0, 0)
green = display.create_pen(0, 255, 0)
yellow = display.create_pen(255, 255, 0)

scale = int(8)  # Set scale, must be divisible by 2, good scales are 4, 8 or 16
scaled_x = int(320 / scale)
scaled_y = int(240 / scale)

gc.enable()

seed(time())  # Seed prng

i = 0
current_gen = set()
next_gen = set()

while True:
    if current_gen == next_gen:
        print("Equilibrium reached. Resetting.")
        reset = True
    if reset == True:
        i = 0
        current_gen = set()  # Define a set to hold current_gen
        next_gen = set()
        c = 0
        while c < (450):
            c = c + 1
            spawn_x = randint(0, scaled_x)
            spawn_y = randint(0, scaled_y)
            current_gen.add((spawn_x, spawn_y))
            draw_cell(spawn_x, spawn_y, green)
        reset = False
    else:
        current_gen = next_gen
        next_gen = set()

    i = i + 1
    start = time()  # Start generation timer
    x = 0  # Start scan from zero
    while x <= scaled_x:
        if x < 6:
            print_status()
        display.update()
        y = 0
        while y <= scaled_y:
            # Is current cell alive?
            if (x, y) in current_gen:
                cell_alive = True
            else:
                cell_alive = False

            # Neighbourhood watch
            ln = compare_neighbours(x, y)

            # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
            # Any live cell with more than three live neighbours dies, as if by overpopulation.
            if ((ln < 2) or (ln > 3)) and (cell_alive == True):
                current_gen.remove((x, y))  # remove dead cells to free memory
                draw_cell(x, y, black)  # clear dead cells
                led.value(0)

            # Any live cell with two or three live neighbours lives on to the next generation.
            if ((ln == 2) or (ln == 3)) and (cell_alive == True):
                draw_cell(x, y, yellow)  # Surviving current_gen are yellow
                try:
                    gc.collect()
                    next_gen.add((x, y))
                except MemoryError:
                    print(micropython.mem_info())
                    print("Out of memory. Resetting...")
                    next_gen = set()
                    current_gen = set()
                    reset = True
                    continue

            # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
            if (ln == 3) and (cell_alive == False):
                draw_cell(x, y, green)  # Newborn current_gen are green
                next_gen.add((x, y))
                led.value(1)
            y = y + 1  # Next row
        x = x + 1  # Next column

    print(
        f"Generation {i}, generate time {time() - start} sec, {len(current_gen)} cells in current_gen, {len(next_gen)} next gen"
    )

    if button_a.is_pressed:
        reset = True
        display.set_pen(black)
        display.clear()
        print("Resetting..")
        sleep(1)
