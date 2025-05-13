# Trying to make some animations in this bad boy

import framebuf #type:ignore
import asyncio

class Animation:
    def __init__(self, frame_rate):
        self.frame_rate = frame_rate
        self.image_buffer = framebuf.FrameBuffer(bytearray(1024), 128, 64, framebuf.MONO_HLSB)
        self.done = False

    def draw_next_frame(self):
        pass # Replace in child class
    
class CoinFlip(Animation):
    def __init__(self, frame_rate, radius):
        super().__init__(frame_rate)
        self.fcount = 0
        self.coin_x = -radius
        self.coin_y = 64
        self.x_vel = 3
        self.x_rad = radius
        self.y_rad = radius - 1
        self.rotation = 0
        self.side = 0
        self.y_vel = -4
        self.grav = 1
        self.done = False
        self.growing = False
    
    def draw_next_frame(self):
        # does physics calc for the next frame, draws to buffer
        self.image_buffer.fill(0)
        self.coin_y += self.y_vel
        self.fcount += 1
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