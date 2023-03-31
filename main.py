from argparse import ArgumentParser

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter

from xray_intensity.utils import get_average_pixel_value

def setup_args():
    parser = ArgumentParser()
    parser.add_argument("--input", type=str, help="Path to the input file", required=True)
    parser.add_argument("--radius", type=int, help="Radius of values to take the average of", default=2)
    parser.add_argument("--blur", help="Whether to apply Gaussian blur to the image", action="store_true")
    return parser.parse_args()

if __name__ == "__main__":
    args = setup_args()

    img = Image.open(args.input)
    gray_img = img.convert("L")
    if args.blur:
        gray_img = gray_img.filter(ImageFilter.GaussianBlur(1.0))

    # create 2 vertical subplots
    fig, axs = plt.subplots(2, 2)
    axs[1][1].axis("off")

    axs[0][0].imshow(gray_img, cmap="gray")

    # get pixel values horizontally across the image
    h_values = []
    for x in range(gray_img.width):
        middle = gray_img.height // 2
        # get vertical slices of the image and average
        img_slice = gray_img.crop((x, middle - args.radius, x + 1, middle + args.radius + 1))
        h_values.append(get_average_pixel_value(img_slice))

    # plot the horizontal pixel values
    axs[1][0].bar(range(len(h_values)), h_values, width=1.0)
    axs[1][0].set_ylim(0, 255)
    axs[1][0].margins(x=0)

    # get pixel values vertically across the image
    v_values = []
    for y in range(gray_img.height):
        middle = gray_img.width // 2
        # get vertical slices of the image and average
        img_slice = gray_img.crop((middle - args.radius, y, middle + args.radius + 1, y + 1))
        v_values.append(get_average_pixel_value(img_slice))

    # plot the vertical pixel values
    axs[0][1].barh(range(len(v_values)), v_values, height=1.0)
    axs[0][1].invert_yaxis()
    axs[0][1].set_xlim(0, 255)
    axs[0][1].margins(y=0)

    # set the subplot to be the same size as the image
    asp = np.diff(axs[1][0].get_xlim())[0] / np.diff(axs[1][0].get_ylim())[0]
    asp /= np.abs(np.diff(axs[0][0].get_xlim())[0] / np.diff(axs[0][0].get_ylim())[0])
    axs[1][0].set_aspect(asp)

    plt.show()