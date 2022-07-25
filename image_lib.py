
import framebuf


# read .PBM image and return a framebuffer with the loaded image
# (original image can be resized by integer multiples)
# image data loading from .pbm is loosely inspired by:
# https://www.mfitzp.com/tutorials/displaying-images-oled-displays/
def read_image(pbm_img_path, resize=1, verbose=True):
    if verbose:
        print(f"Loading image {pbm_img_path}.")
    with open(pbm_img_path, "rb") as f:
        img_format = f.readline()
        if img_format != b"P4\n":
            print("Wrong image format.")
            exit()
        f.readline()  # line with creator info
        dimensions = f.readline()
        w, h = [int(x) for x in dimensions.split(b" ")]
        img = bytearray(f.read())
        if verbose:
            print(f"Image loaded (size {w}x{h} pixels).")
    img_buffer = framebuf.FrameBuffer(img, w, h, framebuf.MONO_HLSB)

    if resize != 1:
        if verbose:
            print("Resizing image.")
        if resize is not int:
            print("Resize factor must be integer.")
        new_w = w * resize
        new_h = h * resize
        new_bytearray = bytearray(new_w*new_h)
        new_img_buffer = framebuf.FrameBuffer(new_bytearray, new_w, new_h, framebuf.MONO_HLSB)

        for y in range(new_h):
            for x in range(new_w):
                old_x = x // resize
                old_y = y // resize
                if img_buffer.pixel(old_x, old_y):
                    new_img_buffer.pixel(x, y, 1)

        img_buffer = new_img_buffer
        w, h = new_w, new_h

    return img_buffer, w, h



"""
# alien 1 (directly as bytearray)  
img = bytearray([
    0b00100000, 0b10000000,
    0b00010001, 0b00000000,
    0b00111111, 0b10000000,
    0b01101110, 0b11000000,
    0b11111111, 0b11100000,
    0b10111111, 0b10100000,
    0b10100000, 0b10100000,
    0b00011011, 0b00000000,
])
print(img)
"""


