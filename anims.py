# Trying to make some animations in this bad boy

import framebuf #type:ignore
import asyncio
from math import fabs, sin, cos, floor, pi
from array import array

class Animation:
    def __init__(self, frame_rate):
        self.frame_rate = frame_rate
        self.fcount = 0
        self.image_buffer = framebuf.FrameBuffer(bytearray(1024), 128, 64, framebuf.MONO_HLSB)
        self.done = False

    def draw_next_frame(self):
        self.fcount += 1
        frame = self.get_next_frame()
        return frame

    def get_next_frame(self):
        pass # Replace in child class
    def reset_anim(self):
        pass # replace in child
    
class CoinFlip(Animation):
    def __init__(self, frame_rate, radius):
        super().__init__(frame_rate)
        self.coin_x = -radius
        self.coin_y = 64
        self.x_vel = 3
        self.x_rad = radius
        self.y_rad = radius - 1
        self.rotation = 0
        self.side = 0
        self.y_vel = -4
        self.grav = 1
        self.growing = False
    
    def get_next_frame(self):
        # does physics calc for the next frame, draws to buffer
        self.image_buffer.fill(0)
        self.coin_y += self.y_vel
        
        if self.fcount >= 4:
            self.y_vel += self.grav
            self.fcount = 0
        if self.y_vel > 4:
            self.y_vel = 4
        self.coin_x += self.x_vel
        self.y_rad  = self.x_rad - self.rotation
        if self.growing: # flips
            pass
            self.rotation -= 2
            if self.rotation <= 0:
                self.growing = False
                self.rotation = 1
        else:
            self.rotation += 2
            if self.rotation >= self.x_rad:
                self.growing = True
                if self.side:
                    self.side = 0
                else:
                    self.side = 1
        if self.coin_y == 64 and self.y_vel > 0: # bounce
            self.y_vel = -3

        self.image_buffer.ellipse(self.coin_x, self.coin_y, self.x_rad, self.y_rad, 1, self.side)
        if self.coin_x > 128 + self.x_rad:
            self.done = True
        return self.image_buffer
    def reset_anim(self):
        self.coin_x = -self.x_rad
        self.coin_y = 64
        self.x_vel = 3
        self.x_rad = self.x_rad
        self.y_rad = self.x_rad - 1
        self.rotation = 0
        self.side = 0
        self.y_vel = -4
        self.grav = 1
        self.growing = False
        self.done = False
    

class SquareRoll(Animation):
    def __init__(self, frame_rate, size):
        super().__init__(frame_rate)
        self.radius = size # How big from corner to corner. Called "radius" because we're using trig shit.
        self.rot = 0
        self.pos_x = 0
        self.pos_y = 0 # will get calculated on the first frame anyway
        self.angle = 30 # Adjust this bad boy to change the spin


    def get_next_frame(self):
        self.image_buffer.fill(0)
        self.pos_x += 1
        self.pos_y = 64 - floor(fabs(sin((self.pos_x + 90)* pi / 180 ))* 64)
        self.angle += 5
        self.image_buffer.poly(self.pos_x,self.pos_y,self.get_points(), 1)
        if self.pos_x > 128 + self.radius:
            self.done = True
        return self.image_buffer
        
    def reset_anim(self):
        self.rot = 0
        self.pos_x = 0
        self.pos_y = 0
        self.angle = 30
        self.done = False

    def get_points(self):
        # Sets the spin of the square
        point_list = array('h', [0,0,0,0,0,0,0,0])
        point_list[0] = floor(self.radius * cos(self.angle * pi / 180))
        point_list[1] = floor(self.radius * sin(self.angle * pi / 180))
        point_list[2] = floor(self.radius * cos((self.angle + 90) * pi / 180))
        point_list[3] = floor(self.radius * sin((self.angle + 90) * pi / 180))
        point_list[4] = floor(self.radius * cos((self.angle + 180) * pi/ 180))
        point_list[5] = floor(self.radius * sin((self.angle + 180) * pi / 180))
        point_list[6] = floor(self.radius * cos((self.angle + 270) * pi / 180))
        point_list[7] = floor(self.radius * sin((self.angle + 270) * pi / 180))
        return point_list