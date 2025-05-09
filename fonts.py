# Defining some fonts as drawing things because eat my nuts image conversion is making me die
import framebuf #type:ignore

class Font:
    # Parent font class
    def __init__(self, height, width) -> None:
        self.height = height
        self.width = width
        self.generate_font_framebufs()
        self.populate_chars()

    def generate_font_framebufs(self):
        # start with a blank buffer for each frame
        self.chars = {}
        for c in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.chars[c] = framebuf.FrameBuffer(bytearray((self.height * self.width) // 8), self.height, self.width, framebuf.MONO_HLSB)

    def populate_chars(self):
        pass # Each subclass will make their own stuff

class Font18x32(Font):
    # 18 x 32 sized font
    def __init__(self, height, width) -> None:
        super().__init__(height, width)


    def populate_chars(self):
        # This is a lot, sorry.
        self.chars["0"].rect(1,1,16,30,1)
        self.chars["0"].rect(2,2,14,28,1)

        self.chars["1"].vline(16,1,30,1)
        self.chars["1"].vline(16,1,29,1)

        self.chars["2"].hline(1,1,14,1)
        self.chars["2"].hline(1,2,14,1)
        self.chars["2"].hline(1,30,14,1)
        self.chars["2"].hline(1,29,14,1)