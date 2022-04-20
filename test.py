from driver import apa102
from gpiozero import LED
import time

strip = apa102.APA102(num_led=12, global_brightness=100, mosi=10, sclk=11, order='rbg')
strip.clear_strip()
for i in range(12):
    strip.set_pixel_rgb(i, 0xFF0000)
strip.show()
time.sleep(5)
strip.clear_strip()
