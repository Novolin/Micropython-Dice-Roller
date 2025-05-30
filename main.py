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
CONFIRM_LED = 16 # LED Pin for the confirm button.
ADV_LED = 21 # LED pin for advantage
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
discard_next_press = False # Are we going to dump our next button press in the trash (we're using it to confirm something, usually)
print("Loading Screens...")

mnu = dice.MenuScreen(screen)
results = dice.ResultScreen(screen)
anim_scr = anims.CoinFlip(20, 6)
active_screen = mnu

# Button bindings
butt_sel_prev = hardwares.Button(SELECT_PREV)
butt_sel_next = hardwares.Button(SELECT_NEXT)
butt_decrease = hardwares.Button(VAL_UP)
butt_increase = hardwares.Button(VAL_DOWN)
butt_roll_bro = hardwares.LEDButton(CONFIRM,CONFIRM_LED, False)

advantage_light = hardwares.LED(ADV_LED)
disadvantage_light = hardwares.LED(DISADV_LED)



def poll_buttons(list_of_buttons):
    poll_result_list = []
    for b in list_of_buttons:
        b.update_state() # TODO: make this be an "if" so we can repeat keypresses if held
        poll_result_list.append(b.released)
    
    if poll_result_list.count(False) == 1:
        return poll_result_list.index(False)
    return -1 # no valid presses.


async def check_inputs():
    global discard_next_press
    b_list = [butt_sel_prev, butt_sel_next, butt_decrease, butt_increase, butt_roll_bro]
    last_result = -1
    while True:
        async with screen_lock:
            poll_result = poll_buttons(b_list)
            if poll_result != last_result and not results.active:
                last_result = poll_result # So we don't repeat right now
                if poll_result == 0:
                    mnu.select_prev()
                    if mnu.is_roll_selected():
                        asyncio.create_task(butt_roll_bro.led.start_blink(250))
                    else:
                        butt_roll_bro.led.turn_off()
                elif poll_result == 1:
                    mnu.select_next()
                    if mnu.is_roll_selected():
                        asyncio.create_task(butt_roll_bro.led.start_blink(250))
                    else:
                        butt_roll_bro.led.turn_off()
                elif poll_result == 2: # Increment
                    mnu.increase_chosen_var()
                elif poll_result == 3: # Decrement
                    mnu.decrease_chosen_var()
                elif poll_result == 4 and not discard_next_press: # Roll/select
                    if mnu.is_roll_selected():
                        butt_roll_bro.led.turn_off()
                        discard_next_press = True
                        asyncio.create_task(results.draw_result_screen(mnu.die_sides, mnu.dice_amount, mnu.modifier, mnu.advantage_state, disp_lock = screen_lock))
                        
                    elif mnu.modifier == 10 and mnu.val_pointer == 0 and mnu.selected_var == 4:
                        print("KILL?")
                        global running
                        running = False
                elif discard_next_press and poll_result == 4:
                    discard_next_press = False
                    asyncio.create_task(butt_roll_bro.led.start_blink(250))
                    mnu.draw_to_display()
        await asyncio.sleep_ms(10) #type:ignore


async def refresh_screen():
    while True:
        if screen.needs_refresh:
            screen.show()
        await asyncio.sleep_ms(30) #type:ignore
            
async def continue_loop():
    while running: # Check the flag once per second until it is flipped. This is a bit sloppy, but it works???
        await asyncio.sleep_ms(1000) #type:ignore

async def check_advantage():
    while True:
        if mnu.advantage_state > 0:
            advantage_light.turn_on()
            disadvantage_light.turn_off()
        elif mnu.advantage_state < 0:
            disadvantage_light.turn_on()
            advantage_light.turn_off()
        else:
            advantage_light.turn_off()
            disadvantage_light.turn_off()
        await asyncio.sleep_ms(20) #type:ignore

async def main():
    # create our monitor function
    asyncio.create_task(check_inputs())
    asyncio.create_task(refresh_screen())
    asyncio.create_task(check_advantage())
    # Put one here for lights that checks adv/disadv, and if we can roll
    await continue_loop() # This will await infinitely until we kill the process


if __name__ == "__main__":
    mnu.draw_to_display()
    print("Ready!")
    asyncio.run(main())