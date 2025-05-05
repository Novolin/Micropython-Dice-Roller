# Dice definitions live here.
from random import randint
from framebuf import FrameBuffer, MONO_HMSB #type:ignore
import array

# for advantage/disadvantage shit
ADVANTAGE = 1
DISADVANTAGE = -1
NEUTRAL = 0

# Text-related display stuff

def get_centered_text_coords(string_of_text:str, box_start = 0, box_size = 128):
    # returns the starting x coord for the text you enter, assuming default font (8px)
    string_size = len(string_of_text) * 8 
    return ((box_size - string_size) // 2) + box_start

def signed_int_to_str(val) -> str:
    if val > 0:
        return "+" + str(val)
    return str(val)

def build_d6_gfx(val) -> FrameBuffer:
    # returns a framebuffer object with the image of a D6 of the given value, as a 32x32 block
    output = FrameBuffer(bytearray(32*4), 32, 32, MONO_HMSB)
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

def build_triad_gfx(value):
    # returns a framebuffer object with the die in a lil triangle doodler
    output = FrameBuffer(bytearray(32*4), 32, 32, MONO_HMSB)
    coords = array('h',[0,0,30,0,15,30,0,0])
    output.poly(0,0,coords,1)
    output.text(str(value), 15 - len(str(value))//2, str(value), 7,1) # TODO: replace with a custom font


class MenuScreen:
    # The main menu you see with options and shit
    def __init__(self, display):
        self.display = display
        self.die_sides = 6
        self.die_amount = 1
        self.modifier = 0
        self.advantage_state = NEUTRAL
        self.hist = HistoryScreen
        self.varlist = [self.die_sides, self.die_amount, self.modifier, self.advantage_state, self.hist, "roll"]
        self.selected_var = 0 # what variable is the +/- key setting.

    def select_next(self):
        self.selected_var += 1
        if self.selected_var >= len(self.varlist):
            self.selected_var = 0
        self.draw_to_display()
        
    def change_die_sides(self, sides):
        self.die_sides = sides
        self.draw_to_display()

    def change_die_amount(self, amount):
        self.die_amount = amount
        self.draw_to_display()

    def change_modifier(self, amount):
        self.modifier += amount
        self.draw_to_display()

    def do_roll_action(self):
        # TODO: make the gfx nice
        pass

    def draw_to_display(self):
        # blank:
        self.display.fill(0)
        # Border:
        self.display.hline(1,0,126,1)
        self.display.hline(1,63,126,1)
        self.display.vline(0,1,62,1)
        self.display.vline(127,1,62,1)
        # Pushes a change to the display
        #TEMP: we're using default text to start.
        # Header (modifier val)
        self.display.text("MODIFIER:",16,2)
        self.display.text(signed_int_to_str(self.modifier), 88,2)

        # Die info
        # This is where I'd change to a larger custom font
        self.display.text(str(self.die_amount) + "D" + str(self.die_sides), 8,16)
        # Footer
        self.display.text("ROLL HIST ADV", 8,54)
        
        # Place the selector indicator:
        if self.selected_var == 0: # Die size, will need tweaks after font change!!!!
            self.display.hline(24,24,len(str(self.die_sides)) * 8,2)
        elif self.selected_var == 1: # Number of Dice
            self.display.hline(8,24,8,2)
        elif self.selected_var == 2: # Modifier
            self.display.hline(88,11,len(signed_int_to_str(self.modifier)) *8, 1)
        elif self.selected_var == 3:
            self.display.vline(100,50,4,1)
        self.display.needs_refresh = True
        # TEMP: just blit immediately.
        self.display.show()

class HistoryScreen:
    def __init__(self, display):
        self.display = display
        self.hist_list = {
            "20":[]}
        self.hist_max_len = 10
    
    def get_last_roll(self, dtype):
        print(self.hist_list[dtype])