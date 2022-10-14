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
    n = {
        (x - 1, y - 1),
        (x - 1, y),
        (x - 1, y + 1),
        (x, y - 1),
        (x, y + 1),
        (x + 1, y - 1),
        (x + 1, y),
        (x + 1, y + 1),
    }
    for x, y in n:
        # Check if neighbour is out of bounds, replace with opposite edge if yes
        if x < 0:
            toroid_x = scaled_x - 1
        elif x == (scaled_x):
            toroid_x = 0
        else:
            toroid_x = x

        if y < 0:
            toroid_y = scaled_y - 1
        elif y == (scaled_y):
            toroid_y = 0
        else:
            toroid_y = y
        f.add((toroid_x, toroid_y))

    ln = sum([x in current_gen for x in f])
    n.clear()
    f.clear()
    return ln  # Return number of live neighbours


def create_search_map(cells):
    make_map = set()
    for x, y in cells:
        n = {
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x, y - 1),
            (x, y),
            (x, y + 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
        }
        for n_x, n_y in n:
            if n_x < 0:
                toroid_x = scaled_x - 1
            elif n_x == (scaled_x):
                toroid_x = 0
            else:
                toroid_x = n_x

            if n_y < 0:
                toroid_y = scaled_y - 1
            elif n_y == (scaled_y):
                toroid_y = 0
            else:
                toroid_y = n_y
            make_map.add((toroid_x, toroid_y))
    return make_map


def print_status():
    gen = "Gen %s, %s cells" % (i, len(current_gen))
    width = display.measure_text(gen, 1, 0)
    display.set_pen(red)
    display.rectangle(0, 234, (width + 10), 6)
    display.set_pen(white)
    display.set_font("bitmap6")
    display.text(gen, 2, 234, 320, 1)


led = Pin(25, Pin.OUT)
display = PicoGraphics(display=DISPLAY_TUFTY_2040)
button_a = Button(7, invert=False)

white = display.create_pen(255, 255, 255)
black = display.create_pen(0, 0, 0)
red = display.create_pen(120, 0, 0)
green = display.create_pen(0, 255, 0)
yellow = display.create_pen(255, 255, 0)
blue = display.create_pen(0, 0, 100)

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
        search_map = set()
        i = 0
        current_gen = set()  # Define a set to hold current_gen
        next_gen = set()
        # Test pattern - edge still lifes, a blinker, a spaceship and a beacon.
        current_gen = {
            (25, 11),
            (26, 11),
            (27, 11),
            (0, 10),
            (0, 11),
            (39, 10),
            (39, 11),
            (11, 0),
            (10, 0),
            (11, 29),
            (10, 29),
            (20, 20),
            (21, 20),
            (20, 21),
            (21, 21),
            (19, 19),
            (19, 18),
            (18, 19),
            (18, 18),
            (0, 0),
            (39, 29),
            (39, 0),
            (0, 29),
            (10, 10),
            (11, 10),
            (12, 10),
            (12, 9),
            (11, 8),
        }
        for (x, y) in current_gen:
            draw_cell(x, y, green)
        c = 0
        while c < (150):
            c = c + 1
            spawn_x = randint(0, scaled_x)
            spawn_y = randint(0, scaled_y)
            current_gen.add((spawn_x, spawn_y))
            draw_cell(spawn_x, spawn_y, blue)
        reset = False

    else:
        current_gen = next_gen
        next_gen = set()

    neighbour_map = create_search_map(current_gen)
    search_map = neighbour_map.union(current_gen)
    print(len(search_map))

    i = i + 1
    start = time()  # Start generation timer
    x = 0  # Start scan from zero
    while x <= scaled_x:
        if x < 20:
            print_status()
        y = 0
        while y <= scaled_y:
            if (x, y) in search_map:
                draw_cell(x, y, blue)

                # Is current cell alive?
                if (x, y) in current_gen:
                    cell_alive = True
                else:
                    cell_alive = False

                # Neighbourhood watch
                ln = compare_neighbours(x, y)

                # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                # Any live cell with more than three live neighbours dies, as if by overpopulation.
                if ln == 0:
                    led.value(0)

                if ((ln < 2) or (ln > 3)) and (cell_alive == True):
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
            else:
                pass
            y = y + 1  # Next row
        x = x + 1  # Next column
    display.update()
    display.set_pen(black)
    display.clear()
    print(
        f"Generation {i}, generate time {time() - start} sec, {len(current_gen)} cells in current_gen, {len(next_gen)} next gen"
    )

    if button_a.is_pressed:
        reset = True
        display.set_pen(black)
        display.clear()
        print("Resetting..")
        sleep(1)
