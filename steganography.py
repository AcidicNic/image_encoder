from PIL import Image, ImageDraw
import textwrap
from sys import argv

_BLACK = (0, 0, 0)
_WHITE = (255, 255, 255)


def decode_image(file_location, output_filename=None):
    if file_location[-4:] != '.png':
        file_location += '.png'
    if output_filename is None:
        output_filename = file_location[:-12] + "_decoded.png"
    encoded_image = Image.open(file_location)
    decoded_image = Image.new("RGB", encoded_image.size)
    raw_encoded_img = list(encoded_image.getdata())

    decoded_pixels = []
    for pixel in raw_encoded_img:
        binary_digit = bin(pixel[0])[-1]
        if binary_digit == "1":
            decoded_pixels.append(_BLACK)
        else:
            decoded_pixels.append(_WHITE)
    decoded_image.putdata(decoded_pixels)
    decoded_image.save(output_filename)


def write_text(text, height, width):
    text_img = Image.new('RGB', (width, height), color=_WHITE)

    char_per_line = (width - 20) // 6
    draw = ImageDraw.Draw(text_img)

    # wraps text into lines so it fits the image size
    lines = textwrap.wrap(text, width=char_per_line)
    # this centers the text
    y_text = (height // 2) - ((len(lines)*15)//2)
    # writes text to the image
    for line in lines:
        draw.text((10, y_text), line, fill=_BLACK)
        y_text += 15

    return text_img


def encode_image(original_img_filename, text, encoded_filename=None):
    if original_img_filename[-4:] != '.png':
        original_img_filename += '.png'
    if encoded_filename is None:
        encoded_filename = original_img_filename[:-4] + "_encoded.png"

    img = Image.open(original_img_filename)
    raw_img = list(img.getdata())
    encoded_image = Image.new("RGB", img.size)

    # creates the text image and converts it to a list of tuples containing RBG values.
    text_img = list(write_text(text, img.size[1], img.size[0]).getdata())

    encoded_pixels = []
    for i in range(len(raw_img)):
        pixel = raw_img[i]
        binary = bin(pixel[0])
        if text_img[i] == _BLACK and binary[-1] == "0":
            pixel = (pixel[0]-1, pixel[1], pixel[2])
        if text_img[i] == _WHITE and binary[-1] == "1":
            pixel = (pixel[0]-1, pixel[1], pixel[2])
        encoded_pixels.append(pixel)

    encoded_image.putdata(encoded_pixels)
    encoded_image.save(encoded_filename)


def main():
    while True:
        print("Welcome to steganography.py's menu!")
        print("e | encode a .png with your text!")
        print("d | decode an encoded .png")
        print("t | to run test (with images/chonker.png")
        sel = input("  Make a selection!: ").lower()
        if sel == 't' or sel == 'test':
            chonker_test()
            return
        elif sel == 'e' or sel == 'd':
            filename = input("please type the relative path to your .png file!").lower()
            if sel == 'e':
                text = input("What text would you like to encode your image with?:\n  ")
                encode_image(filename, text)
            else:
                decode_image(filename)
            return


def chonker_test():
    encode_image("images/chonker.png",
                 "i love this thicc little chonker boy with my whole heart. he's trying his best. please be nice and help him get around! he loves his little cart! use it to wheel him around and take him on walks.")
    decode_image("images/chonker_encoded.png")


if __name__ == "__main__":
    if len(argv) <= 1:
        main()
    elif argv[1] == 'test' or argv[0] == 't':
        print('test')
        chonker_test()
    elif len(argv) == 2:
        print('decoding')
        decode_image(argv[1])
    else:
        print('encoding')
        encode_image(argv[1], " ".join(argv[2:]))
