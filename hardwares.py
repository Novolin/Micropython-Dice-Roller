# Defining hardware objects in here to make things cleaner in main:
import asyncio
from ssd1306 import SSD1306_I2C 
from machine import Pin #type:ignore
import framebuf #type:ignore
from math import ceil
# We're only supporting I2C at the moment, since thats what my hardware calls for
# I'm sure you could take this code and make it play nice with any other interface.

class LED:
    def __init__(self, pin):
        self.pin = Pin(pin) #pin Pin pin pin
        self.blink = False # are we going to make it blink?
        self.blink_time_ms = 0 # how many ms per blink?
        self.is_on = False # surface the pin state a bit easier.

    def toggle_state(self):
        if self.is_on:
            self.is_on = False
            self.pin.off()
        else:
            self.is_on = True
            self.pin.on()

    def turn_on(self):
        self.blink = False # override blink loop
        self.is_on = True
        self.pin.on()
        
    def turn_off(self):
        self.blink = False # override blink loop
        self.is_on = False
        self.pin.off()
        
        
    async def start_blink(self, blink_duration):
        # blinks the pin every blink_duration ms until stopped.
        self.blink = True
        self.blink_time_ms = blink_duration
        while self.blink:
            self.toggle_state()
            await asyncio.sleep_ms(self.blink_time_ms) # You can tweak blink time external to this loop, if you're weird.

class Button:
    def __init__(self, button_pin):
        self.button_pin = Pin(button_pin, Pin.IN, Pin.PULL_UP) # I prefer internal pull-ups when possible
        self.just_changed = False # Has it transitioned since the last time we polled it?
        self.released = True # Is the switch open? "released" instead of "pressed" to make it easier to poll with a pull-up.
    def update_state(self):
        if self.button_pin.value():
            if self.released:
                self.just_changed = False # it's been this way for at least one cycle
            else:
                self.just_changed = True # First poll since change
                self.released = True
                
        else:
            if self.released:
                self.just_changed = True # Button was just pressed.
                self.released = False
                
            else:
                self.just_changed = False 
        return self.just_changed
    

class LEDButton(Button):
    def __init__(self, button_pin, led_pin, light_on_press = True):
        # Give Pin numbers per your board's pin identity stuff
        super().__init__(button_pin)
        self.led = LED(led_pin)
        self.light_on_press = light_on_press # If true, the LED will light whenever the state is registered as "pressed"
        

    def update_state(self):
        # Updates the state of the button, and returns True if the state has just changed this cycle
        # If you just want to read the raw value, you can either directly call button_pin.value() or check button.released
        if self.button_pin.value():
            if self.released:
                self.just_changed = False # it's been this way for at least one cycle
            else:
                self.just_changed = True # First poll since change
                self.released = True
                if self.light_on_press and not self.led.blink:
                    self.led.turn_off()
        else:
            if self.released:
                self.just_changed = True # Button was just pressed.
                self.released = False
                if self.light_on_press and not self.led.blink:
                    self.led.turn_on()
            else:
                self.just_changed = False 
        return self.just_changed
    

class Display(SSD1306_I2C):
    # Just a couple of extensions to the existing model, mostly for asyncio stuff.
    def __init__(self, bus, width = 128, height = 64, buff_type = framebuf.MONO_HMSB):
        # The part I'm using is 128x64, so I'm making that the default.
        super().__init__(width, height, bus)
        self.needs_refresh = False # If we should refresh the screen on the next frame, or if it can stay static.
        self.enabled = True # Flip this if you want to stop the refresh loop.
        
    async def start_refresh_loop(self, frame_time):
        # Checks if the screen needs an update every frame_time ms, and runs show() if true.
        while self.enabled: 
            if self.needs_refresh:
                self.show()
                self.needs_refresh = False
            await asyncio.sleep_ms(frame_time)
