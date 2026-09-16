import time
from machine import TouchPad, Pin

# Setup LED pins
led_pins = [12, 14, 27, 26]
leds = [Pin(pin, Pin.OUT) for pin in led_pins]

# Setup Touch Pin (GPIO 4 is Touch0)
touch = TouchPad(Pin(4))

# Threshold for touch detection (Lower value = touched)
# Baseline reads around 400-800; touching drops it below 200
TOUCH_THRESHOLD = 300

current_pattern = 0
total_patterns = 4

def clear_leds():
    for led in leds:
        led.value(0)

def run_pattern_0():
    # Pattern 1: All Blink
    for led in leds:
        led.value(1)
    time.sleep(0.2)
    for led in leds:
        led.value(0)
    time.sleep(0.2)

def run_pattern_1():
    # Pattern 2: Chaser / Running Light
    for led in leds:
        clear_leds()
        led.value(1)
        time.sleep(0.1)

def run_pattern_2():
    # Pattern 3: Ping-Pong / Bounce
    for led in leds + leds[-2:0:-1]:
        clear_leds()
        led.value(1)
        time.sleep(0.1)

def run_pattern_3():
    # Pattern 4: Alternating Pairs
    leds[0].value(1)
    leds[1].value(1)
    leds[2].value(0)
    leds[3].value(0)
    time.sleep(0.25)
    leds[0].value(0)
    leds[1].value(0)
    leds[2].value(1)
    leds[3].value(1)
    time.sleep(0.25)

patterns = [run_pattern_0, run_pattern_1, run_pattern_2, run_pattern_3]

last_touch_state = False

while True:
    # Read touch value
    touch_value = touch.read()
    is_touched = touch_value < TOUCH_THRESHOLD

    # State machine to detect single tap / edge trigger
    if is_touched and not last_touch_state:
        current_pattern = (current_pattern + 1) % total_patterns
        clear_leds()
        time.sleep(0.3)  # Simple debounce delay
    
    last_touch_state = is_touched

    # Execute active pattern
    patterns[current_pattern]()