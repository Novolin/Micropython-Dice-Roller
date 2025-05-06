# Trying to make some animations in this bad boy

import framebuf #type:ignore
import asyncio

class Animation:
    def __init__(self, frame_rate):
        self.frame_rate = frame_rate
        self.image_data = None    
    