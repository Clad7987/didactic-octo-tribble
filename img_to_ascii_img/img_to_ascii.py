from PIL import Image, ImageDraw
from sys import argv
import os
import shutil


ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]


def resize_image(image, ratio):
    width, height = image.size
    new_width = 200
    new_height = int(new_width * (height / width))

    resized_image = image.resize((new_width, new_height))
    return resized_image


def grayify(image):
    grayscale_image = image.convert("L")
    return grayscale_image


def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters


def convert(image_path):
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, ".", "src", image_path)
    ratio = 10
    try:
        image = Image.open(path)
        resized_image = resize_image(image, ratio)
        grayified_image = grayify(resized_image)
        new_image_data = pixels_to_ascii(grayified_image)

        pixel_count = len(new_image_data)
        ascii_image = "\n".join(
            new_image_data[i : (i + resized_image.width)]
            for i in range(0, pixel_count, resized_image.width)
        )


        with open(
            os.path.join(
                dirname,
                "output",
                "ascii",
                f"{os.path.basename(path)}.txt",
            ),
            "w",
        ) as f:
            f.write(ascii_image)

        os.remove(path)

    except:
        print(path, "Is not a valid image")


if __name__ == "__main__":
    dirname = os.path.dirname(__name__)
    os.makedirs(os.path.join(dirname, "output", "ascii"), exist_ok=True)
    os.makedirs(os.path.join(dirname, "output", "image"), exist_ok=True)
    for file in os.listdir(os.path.join(dirname, "src")):
        convert(file)
