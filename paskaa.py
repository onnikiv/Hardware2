from machine import Pin
from fifo import Fifo
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

LEDS = {
    1: "LED1",
    2: "LED2",
    3: "LED3"
}

class Encoder:
    def __init__(self, rot_a, rot_b, button):
        self.a = Pin(rot_a, mode=Pin.IN, pull=Pin.PULL_UP)
        self.b = Pin(rot_b, mode=Pin.IN, pull=Pin.PULL_UP)
        self.button = Pin(button, mode=Pin.IN, pull=Pin.PULL_UP)
        self.fifo = Fifo(30, typecode='i')
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)
    
    def handler(self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)

rot = Encoder(10, 11, 12)
y = 1

while True:
    if rot.fifo.has_data():
        y += rot.fifo.get()
        if y < 1:
            y = 3
        elif y > 3:
            y = 1
        
        oled.fill(0)
        for i in range(1, 4):
            if i == y:
                oled.text(f">{LEDS[i]}<", 0, 10 * i, 1)
            else:
                oled.text(f" {LEDS[i]}", 0, 10 * i, 1)
        oled.show()

