# Defining some fonts as drawing things because eat my nuts image conversion is making me die
import framebuf #type:ignore






def get_buffer_array(width, height) -> bytearray:
    # returns a bytearray object that can fit a horizontally sorted image buffer
    buff_width = width // 8
    if width % 8: # If we're less than a full horizontal byte, pad it with an extra one.
        buff_width += 1
    output = bytearray(buff_width * height)
    return output



class Font:
    # Parent font class
    def __init__(self, width, height) -> None:
        self.height = height
        self.width = width
        print("Generating Font Data:", width, "x", height, end="")
        self.generate_font_framebufs()
        self.populate_chars()

    def generate_font_framebufs(self):
        print(".", end="")
        # start with a blank buffer for each frame
        self.chars = {}
        for c in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ ":
            self.chars[c] = framebuf.FrameBuffer(get_buffer_array(self.width, self.height), self.width, self.height, framebuf.MONO_HMSB)

    def populate_chars(self):
        print("None made: Invalid font?")
        pass # Each subclass will make their own stuff

    def write(self, string, target_display, x_pos, y_pos):
        # Writes the string to the given display, using our font.
        ch_count = 0
        ln_count = 0
        for c in string.upper(): # make sure it's upper case
            if c == "\n":
                ln_count += 1
                continue
            elif c not in self.chars.keys():
                c = " "
            target_display.blit(self.chars[c], x_pos + (ch_count * self.width), y_pos + (ln_count * self.height))
            ch_count += 1

class ImgFont(Font): #TODO: do images again, dingus.
    def __init__(self) -> None:
        pass


class Font18x32(Font):
    # 18 x 32 sized font
    def __init__(self) -> None:
        super().__init__(18, 32)


    def populate_chars(self):
        # This is a lot, sorry.
        print("\n0", end="")
        self.chars["0"].rect( 3, 3,12,26,1,1)
        self.chars["0"].rect( 6, 6, 6,20,0,1)
        print("1", end="")
        self.chars["1"].rect(12, 3, 3,26,1,1)
        print("2", end="")
        self.chars["2"].rect( 3, 3,12,26,1,1)
        self.chars["2"].rect( 3, 6, 9, 6,0,1)
        self.chars["2"].rect( 6,15,12,11,0,1)
        print("3", end="")
        self.chars["3"].rect( 3, 3,12,26,1,1)
        self.chars["3"].rect( 3, 6, 9,20,0,1)
        self.chars["3"].rect( 6,12, 9, 3,1,1)
        print("4", end="")
        self.chars["4"].rect( 3, 3, 9,15,1,1)
        self.chars["4"].rect(12, 3, 3,26,1,1)
        self.chars["4"].rect( 6, 3, 6,12,0,1)
        print("5", end="")
        self.chars["5"].rect( 3, 3,12,26,1,1)
        self.chars["5"].rect( 6, 6,12, 6,0,1)
        self.chars["5"].rect( 3,15, 9,11,0,1)
        print("6", end="")
        self.chars["6"].rect( 3, 6, 3,23,1,1)
        self.chars["6"].rect( 3, 3, 6, 3,1,1)
        self.chars["6"].rect( 6,12, 9,17,1,1)
        self.chars["6"].rect( 6,15, 6,11,0,1)
        print("7", end="")
        self.chars["7"].rect( 3, 3,12, 3,1,1)
        self.chars["7"].rect(12, 3, 3,26,1,1)
        print("8", end="")
        self.chars["8"].rect( 3, 3,12,26,1,1)
        self.chars["8"].rect( 6, 6, 6, 6,0,1)
        self.chars["8"].rect( 6,15, 6,11,0,1)
        print("9", end= "")
        self.chars["9"].rect( 3, 3,12,12,1,1)
        self.chars["9"].rect(12, 3, 3,26,1,1)
        self.chars["9"].rect( 6, 6, 6, 6,0,1)
        print("A", end="")
        self.chars["A"].rect( 3, 3,12,26,1,1)
        self.chars["A"].rect( 6, 6, 6, 6,0,1)
        self.chars["A"].rect( 6,15, 8,14,0,1)
        print("B", end="")
        self.chars["B"].rect( 3, 3,10,26,1,1)
        self.chars["B"].rect( 3,12,12,15,1,1)
        self.chars["B"].rect( 6, 6, 4, 6,0,1)
        self.chars["B"].rect( 6,15, 8,11,0,1)
        print("C", end="")
        self.chars["C"].rect( 3, 3,12,26,1,1)
        self.chars["C"].rect( 6, 6,12,20,0,1)
        print("D",end="")
        self.chars["D"].rect( 3, 3,10,26,1,1)
        self.chars["D"].rect(12, 5, 3,22,1,1)
        self.chars["D"].rect( 6, 6, 6,20,0,1)
        print("E", end="")
        self.chars["E"].rect( 3, 3,12,26,1,1)
        self.chars["E"].rect( 6, 6,12,20,0,1)
        self.chars["E"].rect( 6,12, 6, 3,1,1)
        print("F", end="")
        self.chars["F"].rect( 3, 3,12,26,1,1)
        self.chars["F"].rect( 6, 6,12,23,0,1)
        self.chars["F"].rect( 6,12, 6, 3,1,1)
        print("G", end="")
        self.chars["G"].rect( 3, 3,12,26,1,1)
        self.chars["G"].rect( 6, 6,12,20,0,1)
        self.chars["G"].rect(12,12, 3,17,1,1)
        self.chars["G"].rect( 9,12, 6, 3,1,1)
        print("H", end="")
        self.chars["H"].rect( 3, 3, 3,26,1,1)
        self.chars["H"].rect(12, 3, 3,26,1,1)
        self.chars["H"].rect( 3,12,12, 3,1,1)
        print("I", end="")
        self.chars["I"].rect( 9, 3, 3,26,1,1)
        print("J", end="")
        self.chars["J"].rect(12, 3, 3,26,1,1)
        self.chars["J"].rect( 3,12,12,17,1,1)
        self.chars["J"].rect( 6,12, 6,14,0,1)
        print("K",end="")
        self.chars["K"].rect( 3, 3, 3,26,1,1)
        # TODO: FINISH THESE

        print("")


class SevenSeg:
    def __init__(self, width, height, thickness = 1) -> None:
        self.height = height
        self.width = width
        self.thickness = thickness # How many px wide is each segment
        self.buff = framebuf.FrameBuffer(get_buffer_array(width, height), self.width, self.height, framebuf.MONO_HMSB)
        self.seg_size = width - thickness * 2
        self.midpoint = self.height // 2


    def draw_segments(self, number):
        # Draws the given segments into the buffer.
        indx = ["ABCDEF", "DC", "BCGEF", "BCDEG", "ACDG", "ABDEG", "ABDEFG", "BCD", "ABCDEFG", "ABCDG", "DCEFG"] # segments are named clockwise starting at the top left vertical one
        seglist = indx[number]
        for c in seglist:
            if c == "A":
                for i in range(self.thickness):
                    self.buff.vline(i, 1,self.seg_size, 1)
            elif c == "B":
                for i in range(self.thickness):
                    self.buff.hline(1, i, self.seg_size, 1)
            elif c =="C":
                for i in range(self.thickness):
                    self.buff.vline(self.width - 1 - i, 1, self.seg_size, 1)
            elif c== "D":
                for i in range(self.thickness):
                    self.buff.vline(self.width-1 -i, self.midpoint + 1 + i, self.seg_size, 1)
            elif c== "E":
                for i in range(self.thickness):
                    self.buff.hline(1, self.height - 1 - i, self.seg_size, 1)
            elif c == "F":
                for i in range(self.thickness):
                    self.buff.vline(i, self.midpoint + 1 + i, self.seg_size, 1)
            elif c == "G":
                for i in range(self.thickness):
                    if i % 2:
                        self.buff.hline(1,self.midpoint - i, self.seg_size, 1)
                    else:
                        self.buff.hline(1, self.midpoint + i//2, self.seg_size, 1)

    
    def get_num(self, num) -> framebuf.FrameBuffer:
        # Returns a single digit in our framebuf.
        self.buff.fill(0) # Blank our framebuf
        self.draw_segments(num)
        return self.buff
    
    def get_multi_digit(self, number) -> framebuf.FrameBuffer:
        buffsize_x = self.width
        if number // 10:
            buffsize_x += self.width + 2
        if number // 100:
            buffsize_x += self.width + 2
        multibuff = framebuf.FrameBuffer(get_buffer_array(buffsize_x, self.height), buffsize_x, self.height, framebuf.MONO_HMSB)
        target_x = 0
        if number // 100:
            multibuff.blit(self.get_num(number//100), target_x, 0)
            target_x += self.width + 2
        if number // 10:
            multibuff.blit(self.get_num(number%100 // 10), target_x, 0)
            target_x += self.width + 2
        multibuff.blit(self.get_num(number%10), target_x, 0)
        return multibuff

    def write(self, num, target,x, y):
        # Acts like the write method on a regular font, for compat.
        target.blit(self.get_multi_digit(num), x, y)

    def DEBUG_DRAW_ALL(self, target):
        # Draws all the numbers to a target display, to make sure they look good.
        target.fill(0)
        t_x = 4 # small buffer between edges of screen
        t_y = 4
        for i in range(10):
            gfx = self.get_num(i)
            if i == 0:
                pass
            elif t_x + self.width >= target.width:
                t_y += self.height
                t_x = 4
            else:
                t_x += self.width + 1
            target.blit(gfx, t_x, t_y)
        target.show()