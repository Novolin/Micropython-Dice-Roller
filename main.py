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




i2c = I2C(0, sda = SDA_PIN, scl = SCL_PIN )

screen_address = i2c.scan()
if screen_address == []:
    print("ERR: SCREEN NOT FOUND")
    raise ValueError

# objecterinos
screen = hardwares.Display(i2c)
screen_lock = asyncio.Lock() # are we doing something that should stop the screen from updating?
die_list = []

mnu = dice.MenuScreen(screen)

async def main():
    # create our monitor function
    

    pass


if __name__ == "__main__":
    mnu.draw_to_display()
        