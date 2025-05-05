# Micropython SSD1306 Dice Roller thing

#V0.1

from machine import Pin, I2C #type: ignore
import hardwares
import asyncio
import dice
from time import sleep_ms


# Pin assignments
CONFIRM = 16 # confirm button pin
SELECT_PREV = 17 # Select <- 
SELECT_NEXT = 18 # Select -> 
VAL_UP = 19 # Increase button
VAL_DOWN = 20 # Decrease button
CONFIRM_LED = -1 # LED Pin for the confirm button.
ADV_LED = -1 # LED pin for advantage
DISADV_LED = -1 # LED pin for disadvantage


SDA_PIN = Pin(4) # pico binding, change as needed
SCL_PIN = Pin(5) 


running = True

i2c = I2C(0, sda = SDA_PIN, scl = SCL_PIN )

debug_pin = Pin(25) # random pin to kill stuff in the loop

screen_address = i2c.scan()
if screen_address == []:
    print("ERR: SCREEN NOT FOUND")
    raise ValueError

# objecterinos
screen = hardwares.Display(i2c)
screen_lock = asyncio.Lock() # are we doing something that should stop the screen from updating?
die_list = [2,4,6,8,10,12,20,100]



mnu = dice.MenuScreen(screen)

# Buttons, look how neat!!!!
butt_sel_prev = hardwares.Button(12)
butt_sel_next = hardwares.Button(13)
butt_decrease = hardwares.Button(14)
butt_increase = hardwares.Button(15)
butt_roll_bro = hardwares.Button(17)




async def main():
    # create our monitor function
    

    pass

async def debug_kill():
    while running:
        if not debug_pin.value():
            running = False
            raise EOFError # raise an error to just kill it.

if __name__ == "__main__":
    mnu.draw_to_display()
        