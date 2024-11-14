from machine import Pin
from fifo import Fifo
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
import time
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)
led1 = Pin(22, Pin.OUT)
led2 = Pin(21, Pin.OUT)
led3 = Pin(20, Pin.OUT)
led1.off()
led2.off()
led3.off()

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
        print("2 value put into fifo")

    

class LedScreen:
    
    def __init__(self):
        self.leds = {
            "LED1":'OFF',
            "LED2":'OFF',
            "LED3":'OFF'}
        self.current_row = 1
        self.current_led = 1
        self.state = self.cursor
    
    
    def cursor(self):
        oled.fill(0)
        if rot.fifo.has_data():
            movement = rot.fifo.get()

            print(self.current_row)
            if movement == -1 and self.current_row < 3:
                self.current_row += 1

            elif movement == 1 and self.current_row > 1:
                self.current_row -= 1
                
            elif movement == 2:
                self.state = self.led_toggle
                rot.fifo.empty()
        
        for i, key in enumerate(sorted(self.leds.keys()), start=1):
            if i == self.current_row:
                oled.text(f"{key}: {self.leds[key]}<", 0, 10 * i, 1)
            else:
                oled.text(f"{key}: {self.leds[key]}", 0, 10 * i, 1)
                
        oled.show()

            
    def led_toggle(self):
        self.current_led = self.current_row
        print(f"ledi: {self.current_led}")
        if self.current_led == 1:
            led1.toggle()
            if self.leds["LED1"] == "OFF":
                self.leds["LED1"] = "ON"

            else:
                self.leds["LED1"] = "OFF"
                
        elif self.current_led == 2:
            led2.toggle()
            if self.leds["LED2"] == "OFF":
                self.leds["LED2"] = "ON"

            else:
                self.leds["LED2"] = "OFF"

        elif self.current_led == 3:
            led3.toggle()
            if self.leds["LED3"] == "OFF":
                self.leds["LED3"] = "ON"

            else:
                self.leds["LED3"] = "OFF"
                
        self.state = self.cursor

rot = Encoder(10, 11, 12)
led_screen = LedScreen()

while True:
    if rot.fifo.has_data():
        led_screen.state()