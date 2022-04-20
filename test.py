import apa102
from gpiozero import LED
import time

PIXELS_N = 12

strip = apa102.APA102(num_led=PIXELS_N)
strip.clear_strip()
for i in range(PIXELS_N):
    strip.set_pixel(i, 255, 0, 0)
strip.show()
time.sleep(5)
strip.clear_strip()
