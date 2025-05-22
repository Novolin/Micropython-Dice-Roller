# Dice definitions live here.
from random import randint
from framebuf import FrameBuffer, MONO_HLSB #type:ignore
from array import array
from math import ceil
import anims
import asyncio
from time import sleep_ms #type:ignore
import fonts
from micropython import const #type:ignore

# for advantage/disadvantage shit
ADVANTAGE = const(1)
DISADVANTAGE = const(-1)
NEUTRAL = const(0)

# Text-related display stuff

def get_centered_text_coords(string_of_text:str, font_width = 8, box_start = 0, box_size = 128):
    # returns the starting x coord for the text you enter, assuming default font (8px)
    string_size = len(string_of_text) * font_width
    return ((box_size - string_size) // 2) + box_start

def signed_int_to_str(val) -> str:
    if val > 0:
        return "+" + str(val)
    return str(val)

def build_d6_gfx(val) -> FrameBuffer:
    # returns a framebuffer object with the image of a D6 of the given value, as a 32x32 block
    output = FrameBuffer(bytearray(32*4), 32, 32, MONO_HLSB)
    # draw a border
    output.hline(1,0,29,1)
    output.hline(1,30,29,1)
    output.vline(0,1,29,1)
    output.vline(30,1,29,1)
    if val in [1,3,5]:
        # draw a dot in the middle
        output.ellipse(15,15,3,3,1,1)
    if val == 1: 
        return output # Thats all we need for a 1, so return it.
    # Every other combo uses NW and SE dots
    output.ellipse(6,6,3,3,1,1)
    output.ellipse(24,24,3,3,1,1) 
    if val > 3: # Everything but 3 has NE and SW
        output.ellipse(24,6,3,3,1,1)
        output.ellipse(6,24,3,3,1,1)
    if val == 6:
        output.ellipse(6,15,3,3,1,1)
        output.ellipse(24,15,3,3,1,1)
    return output

def build_triad_gfx(value) -> FrameBuffer:
    # returns a framebuffer object with the die in a lil triangle doodler
    output = FrameBuffer(bytearray(32*4), 32, 32, MONO_HLSB)
    coords = array('h',[0,0,30,0,15,30,0,0])
    output.poly(0,0,coords,1)
    output.text(str(value), 15 - len(str(value))* 4, 7, 1) # TODO: replace with a custom font
    return output


class MenuScreen:
    # The main menu you see with options and shit
    def __init__(self, display):
        self.display = display
        self.die_sides = 6
        self.die_vals = [2,4,6,8,10,12,16,20,100]
        self.val_pointer = 2 # where in the value list are we
        self.dice_amount = 1
        self.modifier = 0
        self.advantage_state = NEUTRAL
        self.varlist = [self.dice_amount, self.die_sides, self.modifier, "hist", self.advantage_state , "roll"]
        self.selected_var = 0 # what variable is the +/- key setting.
        self.font = fonts.SevenSeg(10,20)
        

    def select_next(self):
        self.selected_var += 1
        if self.selected_var >= len(self.varlist):
            self.selected_var = 0
        self.draw_to_display()
        

    def select_prev(self):
        self.selected_var -= 1
        if self.selected_var < 0:
            self.selected_var = len(self.varlist) - 1
        self.draw_to_display()

    def change_die_sides(self, val):
        self.val_pointer += val
        if self.val_pointer >= len(self.die_vals):
            self.val_pointer = 0
        elif self.val_pointer < 0:
            self.val_pointer = len(self.die_vals) - 1
        self.die_sides = self.die_vals[self.val_pointer]
        self.draw_to_display()

    def change_dice_amount(self, amount):
        self.dice_amount += amount
        if self.dice_amount == 0:
            self.dice_amount = 1
        elif self.dice_amount >= 10: # max # of dice at once.
            self.dice_amount = 1
        self.draw_to_display()

    def change_modifier(self, amount):
        self.modifier += amount
        self.draw_to_display()

    def increase_chosen_var(self):
        if self.selected_var == 0: # number of dice:
            self.change_dice_amount(1)
        elif self.selected_var == 1: # die value
            self.change_die_sides(1)
        elif self.selected_var == 2: # Modifier
            self.change_modifier(1)
        elif self.selected_var == 4: # advantage, this is a bit messy.
            if self.advantage_state == NEUTRAL:
                self.advantage_state = ADVANTAGE
            if self.advantage_state == DISADVANTAGE:
                self.advantage_state = NEUTRAL
        return
    
    def decrease_chosen_var(self):
        if self.selected_var == 0: # number of dice:
            self.change_dice_amount(-1)
        elif self.selected_var == 1: # die value
            self.change_die_sides(-1)
        elif self.selected_var == 2: # Modifier
            self.change_modifier(-1)
        elif self.selected_var == 4: # advantage, this is a bit messy.
            if self.advantage_state == NEUTRAL:
                self.advantage_state = DISADVANTAGE
            elif self.advantage_state == ADVANTAGE:
                self.advantage_state = NEUTRAL
        return
    
    def is_roll_selected(self):
        # simple getter for seeing if we can roll the die or not.
        if self.varlist[self.selected_var] == "roll":
            return True
        else:
            return False


    def draw_to_display(self):

        # blank:
        self.display.blank_and_draw_border()
        # Header (modifier val)
        self.display.text("MODIFIER:",16,2)
        self.display.text(signed_int_to_str(self.modifier), 88,2)

        # Die info
        self.display.blit(self.font.get_num(10), 59, 22) # big "d" in the center
        self.display.blit(self.font.get_num(abs(self.dice_amount)), 46, 22) # number of die, shouldn't be over 10 anyway?
        side_offset = 0
        if self.die_sides >= 100:
            self.display.blit(self.font.get_num(self.die_sides// 100), 72, 22)
            side_offset += 12 # add a 12 px buffer to the next #
        if self.die_sides >= 10:
            self.display.blit(self.font.get_num(self.die_sides % 100 // 10), 72 + side_offset, 22)
            side_offset += 12
        
        self.display.blit(self.font.get_num(self.die_sides % 10), 72 + side_offset, 22)
        # Footer
        self.display.text("HIST ADV ROLL", 8,54)
        
        # Place the selector indicator:
        if self.selected_var == 0: # Number of Dice
            self.display.rect(44, 20,self.font.width + 4, self.font.height + 4, 1)
        elif self.selected_var == 1: # Die Value
            self.display.rect(70,20,self.font.width + 4 +  (2 + self.font.width) * (side_offset // 12), self.font.height + 4, 1)
        elif self.selected_var == 2: # Modifier
            self.display.hline(88,11,len(signed_int_to_str(self.modifier)) *8, 1)
        elif self.selected_var == 3: # History
            self.display.hline(8,50,32,1)
        elif self.selected_var == 4: # Advantage
            self.display.hline(48, 50, 24, 1)
        elif self.selected_var == 5: # Roll
            self.display.hline(80, 50, 32, 1)
        self.display.needs_refresh = True
            

class HistoryScreen:
    def __init__(self, display):
        self.display = display
        self.hist_list = {
            "20":[]}
        self.hist_max_len = 5
        self.hist_file = "roll_history.txt"
    
    def get_last_roll(self, dtype):
        print(self.hist_list[dtype])

class ResultScreen:
    def __init__(self, display):
        self.display = display
        self.active = False
        self.roll_anim = anims.SquareRoll(10, 10) # just use coin flip for now
        self.font = fonts.Font18x32()
        self.show_animation = True # toggle animation on roll
        self.always_use_numbers = True # Results will always be numerics, instead of dice gfx


    async def draw_result_screen(self, diesize, dicenum, modify, advantage = NEUTRAL, disp_lock = None):
        
        if self.show_animation and disp_lock:
            async with disp_lock:
                while not self.roll_anim.done:
                    self.display.blit(self.roll_anim.get_next_frame(), 0, 0)
                    await asyncio.sleep_ms(self.roll_anim.frame_rate) #type: ignore
                self.roll_anim.reset_anim()
        
        # do the math:
        raw_results = []
        for d in range(dicenum):
            raw_results.append(randint(1,diesize))
            if advantage != NEUTRAL: # Hopefully we don't have more than 1Dx with advantage?
                raw_results.append(randint(1, diesize))

        # Blank and draw the border on the main display:
        self.display.blank_and_draw_border()

        # Most common: one die, without advantage.
        if dicenum == 1 and advantage == NEUTRAL:
            if modify == 0: # nothing new, just do it straight
                self.font.write(str(raw_results[0]), self.display, 32,20)
            else: 
                self.display.text(str(raw_results[0]) + signed_int_to_str(modify) + " =", 32,32)
                self.font.write(str(raw_results[0] + modify), self.display, 80, 20 )
        else:
            print("not yet bucko")

        


    def wait(self, time):
        sleep_ms(time) # wait for a full second.
        self.display.text("ANY KEY",2,46)
        self.display.text("TO CONTINUE", 2,54)