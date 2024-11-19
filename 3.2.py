from machine import Pin
from fifo import Fifo
from machine import I2C
from ssd1306 import SSD1306_I2C
import time

class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, mode=Pin.IN, pull=Pin.PULL_UP)
        self.b = Pin(rot_b, mode=Pin.IN, pull=Pin.PULL_UP)
        self.fifo = Fifo(30, typecode='i')
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)

    def handler(self, pin):
        if self.b.value():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)


class LedMenu:
    def __init__(self, button):
        self.i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
        self.oled_width = 128
        self.oled_height = 64
        self.oled = SSD1306_I2C(self.oled_width, self.oled_height, self.i2c)
        self.button = Pin(button, mode=Pin.IN, pull=Pin.PULL_UP)
        self.button.irq(handler=self.button_handler, trigger=Pin.IRQ_FALLING, hard=True)
        self.fifo = Fifo(10, typecode="i")
        
        self.old_time = 0
        
        self.led1 = Pin(22, Pin.OUT)
        self.led2 = Pin(21, Pin.OUT)
        self.led3 = Pin(20, Pin.OUT)
        self.leds = {
            self.led1: 'OFF',
            self.led2: 'OFF',
            self.led3: 'OFF'
        }
        
        for led in self.leds.keys():
            led.off()

        self.current_row = 1
        self.state = self.cursor


    def button_handler(self, pin):
        delay = 50
        current_time = time.ticks_ms()
        if current_time - self.old_time < delay:
            return
        self.fifo.put(2)
        self.old_time = current_time


    def cursor(self):
        self.oled.fill(0)
        movement = rot.fifo.get()
        
        if movement == -1 and self.current_row < 2:
            self.current_row += 1
        elif movement == 1 and self.current_row > 0:
            self.current_row -= 1


        for i, (led, status) in enumerate(self.leds.items()):
            led_name = f"LED{i + 1}"
            if i == self.current_row:
                self.oled.text(f"{led_name}: {status} <", 0, 10 * (i + 1), 1)
            else:
                self.oled.text(f"{led_name}: {status}", 0, 10 * (i + 1), 1)

        self.oled.show()


    def menu_update(self):
        self.oled.fill(0)
        for i, (led, status) in enumerate((self.leds.items())):
            led_name = f"LED{i + 1}"
            if i == self.current_row:

                self.oled.text(f"{led_name}: {status} <", 0, 10 * (i + 1), 1)
            else:
                self.oled.text(f"{led_name}: {status}", 0, 10 * (i + 1), 1)

        self.oled.show()
        self.state = self.cursor


    def led_toggle(self):

            action = self.fifo.get()
            if action == 2:
                selected_led = list(self.leds.keys())[self.current_row]


                if selected_led == self.led1:
                    self.led1.toggle() 
                    self.leds[self.led1] = 'ON' if self.led1.value() else 'OFF'
                elif selected_led == self.led2:
                    self.led2.toggle()
                    self.leds[self.led2] = 'ON' if self.led2.value() else 'OFF'
                elif selected_led == self.led3:
                    self.led3.toggle()
                    self.leds[self.led3] = 'ON' if self.led3.value() else 'OFF'


                self.menu_update()


rot = Encoder(10, 11)
led_screen = LedMenu(12)

while True:
    if rot.fifo.has_data():
        led_screen.state()

    if led_screen.fifo.has_data():
        led_screen.led_toggle()
