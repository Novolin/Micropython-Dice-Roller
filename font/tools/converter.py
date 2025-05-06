# NOTE! THIS ONLY WORKS ON A COMPUTER! 
# PIL Isn't part of MicroPython for size/compat reasons
# This script is included in case you want to make your own fonts (and so I can convert my own easily)

from PIL import Image

def encode_img_to_bitstream(img)-> bytearray:
    output = bytearray(0)
    # Converts a PIL Image to a bytearray, in HLSB form.
    bitcount = 0
    x_count = 0
    bt = 0
    for px in list(img.getdata()):
        if px > 1:
            bt |= 1 << bitcount
        bitcount += 1
        if bitcount >= 8:
            output.append(bt)
            bt = 0
            bitcount = 0
        x_count += 1
        if x_count > img.width:
            x_count = 0
            if bitcount > 0: # If not divisible by 8, start a new bit anyway.
                output.append(bt)
    return output

def convert_file_to_font(input_filename, output_filename, font_size_x, font_size_y):
    # We only support black/white so we're going to do some hacky shit with colour math.
    # Reads characters from an image L -> R from the top down, assuming they are 0-9, A-Z
    font_arr = []
    hstack = False
    vstack = False
    with Image.open(input_filename) as infile:
        if infile.height > font_size_y:
            print("Vertical Stack Detected")
            vstack = True
        if infile.height > font_size_x:
            print("Horizontal Stack Detected")
            hstack = True
        crop_x = 0
        crop_y = 0
        while crop_y < infile.height:
            while crop_x < infile.width:
                font_arr.append(infile.crop((crop_x, crop_y, crop_x + font_size_x, crop_y + font_size_y)))
                crop_x += font_size_x
            crop_y += font_size_y
        
    # we've loaded our data into our font array, so now we can start encoding shit, starting with character size
    output_data = bytearray(0)
    output_data.append(font_size_x)
    output_data.append(font_size_y)

    for ch in font_arr:
        as_bytearr = encode_img_to_bitstream(ch)
        for b in as_bytearr:
            output_data.append(b)

    with open(output_filename, "w+b") as outfile:
        outfile.write(output_data)
            


if __name__ == "__main__":
    convert_file_to_font("font/tools/lcdfont.bmp", "font/lcdfont", 18,32)