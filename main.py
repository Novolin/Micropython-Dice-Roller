# Micropython SSD1306 Dice Roller thing

#V0.1

from machine import Pin, I2C #type: ignore
import hardwares
import asyncio
import dice
import anims
import gc
from time import sleep_ms #type: ignore
from micropython import mem_info #type:ignore


# Pin assignments
CONFIRM = 17 # confirm button pin
SELECT_PREV = 18 # Select <- 
SELECT_NEXT = 19 # Select -> 
VAL_UP = 25 # Increase button
VAL_DOWN = 24 # Decrease button
CONFIRM_LED = 12 # LED Pin for the confirm button.
ADV_LED = 22 # LED pin for advantage
DISADV_LED = 23 # LED pin for disadvantage


SDA_PIN = Pin(4) # pico binding, change as needed
SCL_PIN = Pin(5) 


running = True

i2c = I2C(0, sda = SDA_PIN, scl = SCL_PIN )

screen_address = i2c.scan()
if screen_address == []:
    print("ERR: SCREEN NOT FOUND")
    raise ValueError

# objecterinos
screen = hardwares.Display(i2c)
screen_lock = asyncio.Lock() # are we doing something that should stop the screen from updating?
die_list = [2,4,6,8,10,12,20,100]
print("Init Screens:")

mnu = dice.MenuScreen(screen)
results = dice.ResultScreen(screen)
anim_scr = anims.CoinFlip(20, 6)

# Button bindings
butt_sel_prev = hardwares.Button(SELECT_PREV)
butt_sel_next = hardwares.Button(SELECT_NEXT)
butt_decrease = hardwares.Button(VAL_UP)
butt_increase = hardwares.Button(VAL_DOWN)
butt_roll_bro = hardwares.LEDButton(CONFIRM,CONFIRM_LED, False)

kill_loop = asyncio.Event() # This is to kill the loop if I need to debug or if things hang. It will crash shit, which is fine.


def poll_buttons(list_of_buttons):
    poll_result_list = []
    for b in list_of_buttons:
        b.update_state() # TODO: make this be an "if" so we can repeat keypresses if held
        poll_result_list.append(b.released)
    
    if poll_result_list.count(False) == 1:
        return poll_result_list.index(False)
    return -1 # no valid presses.


async def check_inputs():
    b_list = [butt_sel_prev, butt_sel_next, butt_decrease, butt_increase, butt_roll_bro]
    last_result = -1
    while True:
        poll_result = poll_buttons(b_list)
        if poll_result != last_result:
            print(poll_result)
            last_result = poll_result # So we don't repeat right now
            if poll_result == 0:
                mnu.select_prev()
            elif poll_result == 1:
                mnu.select_next()
            elif poll_result == 2: # Increment
                mnu.increase_chosen_var()
            elif poll_result == 3: # Decrement
                mnu.decrease_chosen_var()
            elif poll_result == 4: # Roll/select
                if mnu.is_roll_selected():
                    asyncio.create_task(results.show_roll_result(screen_lock, mnu.die_vals[mnu.val_pointer], mnu.modifier, mnu.advantage_state))
        await asyncio.sleep_ms(10) #type:ignore

async def roll_enabled():
    while True:
        if mnu.is_roll_selected():
            butt_roll_bro.led.turn_on()
        else:
            butt_roll_bro.led.turn_off()
        await asyncio.sleep_ms(10) #type:ignore

async def refresh_screen():
    while True:
        if screen.needs_refresh:
            screen.show()
        await asyncio.sleep_ms(30) #type:ignore
            
            

async def main():
    # create our monitor function
    
    mem_info()
    gc.collect()
    print("-----------")
    mem_info()
    while running:
        asyncio.create_task(check_inputs())
        asyncio.create_task(roll_enabled())
        asyncio.create_task(refresh_screen())
        # Put one here for lights that checks adv/disadv, and if we can roll
        if not running: # will this fucking work???
            break
        await kill_loop.wait()


if __name__ == "__main__":
    mnu.draw_to_display()
    asyncio.run(main())