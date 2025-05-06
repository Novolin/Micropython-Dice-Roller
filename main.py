# Micropython SSD1306 Dice Roller thing

#V0.1

from machine import Pin, I2C #type: ignore
import hardwares
import asyncio
import dice
from time import sleep_ms


# Pin assignments
CONFIRM = 17 # confirm button pin
SELECT_PREV = 12 # Select <- 
SELECT_NEXT = 13 # Select -> 
VAL_UP = 14 # Increase button
VAL_DOWN = 15 # Decrease button
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


print("FART")

mnu = dice.MenuScreen(screen)

print("GAY")


# Button bindings
#butt_sel_prev = hardwares.Button(SELECT_PREV)
#butt_sel_next = hardwares.Button(SELECT_NEXT)
#butt_decrease = hardwares.Button(VAL_UP)
#butt_increase = hardwares.Button(VAL_DOWN)
#butt_roll_bro = hardwares.Button(CONFIRM)


def poll_buttons(list_of_buttons):
    poll_result_list = []
    for b in list_of_buttons:
        b.update_state() # TODO: make this be an "if" so we can repeat keypresses if held
        poll_result_list.append(b.released)
    
    if poll_result_list.count(False) == 1:
        return poll_result_list.index(False)
    return -1 # no valid presses.


def DEBUG_TEST():
    # goes through a few dice displays.
    for i in range(6):

        mnu.display.fill(0)
        mnu.display.blit(dice.build_d6_gfx(i+1), 12, 12)
        mnu.display.show()
        print(i+1)
        sleep_ms(250)
    for i in range(20):
        mnu.display.fill(0)
        mnu.display.blit(dice.build_triad_gfx(i+1), 12, 12)
        mnu.display.show()
        print(i+1)
        sleep_ms(250)
    
    for c in "0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        print(c)
        mnu.display.fill(0)
        mnu.display.blit(mnu.font.chars[c], 12, 12)
        mnu.display.show()
        
        sleep_ms(250)



async def main():
    # create our monitor function
    

    pass


        