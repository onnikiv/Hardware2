from machine import Pin
from fifo import Fifo
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)
led = Pin(22, mode = Pin.OUT)

class Encoder:
    def __init__(self, rot_a, rot_b, button):
        self.a = Pin(rot_a, mode=Pin.IN, pull=Pin.PULL_UP)
        self.b = Pin(rot_b, mode=Pin.IN, pull=Pin.PULL_UP)
        self.button = Pin(button, mode=Pin.IN, pull=Pin.PULL_UP)
        self.fifo = Fifo(30, typecode='i')
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)
        self.button.irq(handler = self.button_handler, trigger = Pin.IRQ_FALLING, hard = True)

    
    def handler(self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)

    def button_handler(self,pin):
        self.fifo.put(2)

    

class LedScreen:
    
    def __init__(self):
        self.y_axl = 0
        self.leds = {
            " LED1": 'OFF',
            " LED2": 'OFF',
            " LED3": 'OFF'}
        self.state = self.off
        
    def off(self):
        oled.fill(0)
        y = 0
        for key, value in sorted(self.leds.items()): #perkele
            oled.text(f"{key}: {value}", 0, y)
            y += 10
        oled.show()
        self.state = self.cursor
    
    def cursor(self):
        
        self.y_axl += rot.fifo.get()
        
        if self.y_axl > 1:
            self.y_axl = 1
        elif self.y_axl < -1:
            self.y_axl = -1

        print(f"y value: {self.y_axl}")

        oled.fill(0)
        for i, key in enumerate(sorted(self.leds.keys())):
            if i - 1 == self.y_axl:
                oled.text(f"{key}: {self.leds[key]}<", 0, 10 * i, 1)
            else:
                oled.text(f"{key}: {self.leds[key]}", 0, 10 * i, 1)
        oled.show()
        
        
        



rot = Encoder(10, 11, 12)
led_screen = LedScreen()

rot.fifo.put(1)
while True:
    if rot.fifo.has_data():
        led_screen.state()
        

