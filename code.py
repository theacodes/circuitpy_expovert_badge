import time
import board
from adafruit_pyportal import PyPortal
from adafruit_button import Button
# from displayio import Group
import terminalio
import neopixel
import displayio
from adafruit_bitmap_font import bitmap_font

arial_font = bitmap_font.load_font("/fonts/Arial-ItalicMT-17.bdf")

color_labels = {
    "red": (255, 0, 0),
    "yellow": (255, 170, 0),
    "green": (0, 255, 0),
}

def create_buttons(size=60, offset=10):
    """Create buttons based on colors and positions

    Based on code from:
        https://learn.adafruit.com/pyportal-neopixel-color-oicker
    """
    buttons = []
    x = offset
    y = offset

    for label, color in color_labels.items():
        button = Button(
            x=x, y=y,
            width=size, height=size,
            style=Button.SHADOWROUNDRECT,
            fill_color=color,
            outline_color=0x222222,
            name=label)
        buttons.append(button)
        x += 80
    return buttons


def chase_pattern(color, offset):
    """Single color chase pattern.

    Based on code from:
        https://learn.adafruit.com/gemma-hoop-earrings/circuitpython-code
    """
    for i in range(num_pixels):
        if ((offset + i) & (num_pixels)) < 2:
            strip[i] = current_color
        else:
            strip[i] = 0
    strip.show()
    time.sleep(0.08)
    offset += 1
    if offset >= num_pixels:
        offset = 0
    return offset

# PyPortal Initialization

background_color = 0x0  # black
brightness = 0.1        # 60%
num_pixels = 5          # 5 pixel strip
auto_write = False      # call strip.show() to change neopixel vals

strip = neopixel.NeoPixel(
    board.D4, num_pixels,
    brightness=brightness,
    auto_write=auto_write)
strip.fill(0)

pyportal = PyPortal(default_bg=background_color)

buttons = create_buttons()
# TODO NZ: Do we want to add the buttons to a group
# before adding them to the pyportal splash screen
button_group = displayio.Group()
for button in buttons:
    button_group.append(button.group)
pyportal.splash.append(button_group)

back_button = Button(
            x=250, y=200,
            width=60, height=40,
            style=Button.SHADOWROUNDRECT,
            fill_color=(165, 172, 184),
            outline_color=0x222222,
            name="back",
            label="back",
            label_font=arial_font,
            )
buttons.append(back_button)
back_button_group = displayio.Group()
back_button_group.append(back_button.group)
pyportal.splash.append(back_button_group)
back_button_group.hidden = True

current_color = 0
current_offset = 0

while True:
    touch = pyportal.touchscreen.touch_point
    if touch:
        for button in buttons:
            if button.contains(touch):
                if button.name == "back":
                    print("1: back_button.hidden", back_button_group.hidden)
                    pyportal.set_background(background_color)
                    back_button_group.hidden = True
                    button_group.hidden = False
                    print("2: back_button.hidden", back_button_group.hidden)
                if button.name == "green":
                    print("Let's display our full battery image.")
                    print("is button group hidden?", button_group.hidden)
                    # pyportal.splash.pop(1)
                    button_group.hidden = True
                    print("is button group hidden?", button_group.hidden)
                    pyportal.set_background("images/full.bmp")
                    back_button_group.hidden = False


                print("Touched", button.name)
                current_color = button.fill_color
                break

    current_offset = chase_pattern(color=current_color, offset=current_offset)
    time.sleep(0.05)