'''
GGP's Image Generator for LGTK's Chatter Tier List

The script takes the input of an excel file "file.xlsx" to extract
a list of names from the "Twitch Name" column and then outputs the
generated images into an img folder.I used Pandas for this because
it was what I knew and I learned PIL for image generation. 

Built Using:
python      3.12.3
pandas      2.2.3
pillow      11.2.1
openpyxl    3.1.5

Versions aren't a hard requirement, you will need a version of
python that supports secrets. For PIL you will need something over
version 8.0.0 due to getbbox. Openpyxl should be required if you
are on linux and want to read excel files.
'''
import secrets as sc
import textwrap as tw

import pandas as pd
from PIL import Image, ImageDraw, ImageFont

text_colors = [
    (0, 255, 255),      # Cyan
    (0, 128, 255),      # Azure
    (0, 0, 255),        # Blue
    (128, 0, 255),      # Violet
    (255, 0, 255),      # Magenta
    (255, 0, 128),      # Rose
    (255, 0, 0),        # Red
    (255, 128, 0),      # Orange
    (255, 255, 0),      # Yellow
    (128, 255, 0),      # Chartreuese
    (0, 255, 0),        # Green
    (0, 255, 128),      # Spring Green
]

background_colors = [
    # (0, 0, 0),          # Black
    (32, 32, 32),       # Darker Gray
    # (64, 64, 64),       # Dark Gray
    # (128, 128, 128),    # Gray
]


def get_bg_clr():
    return sc.choice(background_colors)


def get_txt_clr():
    return sc.choice(text_colors)


def generate_img(
        txt,
        img_m,
        img_s,
        img_bg_clr,
        img_outline_clr,
        img_outline_rad,
        img_outline_wdth,
        fnt,
        txt_wrp_lngth,
        txt_clr):
    img = Image.new(mode=img_m,
                    size=img_s,
                    color=None)

    txt_lines = tw.wrap(txt, txt_wrp_lngth)

    # Set my preferred color :)
    if txt == 'GamersGottaPlay':
        txt_clr = (0, 128, 255)

    # Calculate the text top down starting point to ensure middle alignment
    # (Image Height - Total Text Height) / 2 = Top Margin from 0,0
    # Total Text Height = Number of Text Lines x Text Height Per Line
    td_mrgn = (img.size[1] - (len(txt_lines) * fnt.getbbox(txt)[3])) / 2

    box_size = [(0, 0), img_s]
    drw = ImageDraw.Draw(img)
    drw.rounded_rectangle(xy=box_size,
                          radius=img_outline_rad,
                          fill=img_bg_clr,
                          outline=img_outline_clr,
                          width=img_outline_wdth)

    if len(txt_lines) > 1:
        for line in txt_lines:
            # Calculate the text left right starting point to ensure middle alignment for each line
            # (Image Width - Text Width) / 2 = Left Margin from 0,0
            lr_mrgn = (img.size[0] - fnt.getbbox(line)[2]) / 2
            drw.text(xy=(lr_mrgn, td_mrgn),
                     text=line,
                     fill=txt_clr,
                     font=fnt)
            td_mrgn += fnt.getbbox(line)[3]
    else:
        # Calculate the text left right starting point to ensure middle alignment
        # (Image Width - Text Width) / 2 = Left Margin from 0,0
        lr_mrgn = (img.size[0] - fnt.getbbox(txt)[2]) / 2
        drw.text(xy=(lr_mrgn, td_mrgn),
                 text=txt,
                 fill=txt_clr,
                 font=fnt)

    # Test the generated image
    if txt == 'GamersGottaPlay':
        img.show()

    file_name = "".join(e for e in txt if e.isalnum())
    file_name = file_name.lower()
    img.save("img/" + file_name + ".png")


def main():
    image_width = 1800
    image_height = 800
    image_mode = "RGBA"
    image_outline_color = "White"
    image_outline_radius = 100
    image_outline_width = 8
    font = "UbuntuMono-R.ttf"
    font_size = 200
    textwrap_length = 16

    font_obj = ImageFont.truetype(font, font_size)
    image_size = (image_width, image_height)

    df = pd.read_excel("file.xlsx")
    name_list = df["Twitch Name"].values.tolist()

    for name in name_list:
        generate_img(txt=name,
                     img_m=image_mode,
                     img_s=image_size,
                     img_bg_clr=get_bg_clr(),
                     img_outline_clr=image_outline_color,
                     img_outline_rad=image_outline_radius,
                     img_outline_wdth=image_outline_width,
                     fnt=font_obj,
                     txt_wrp_lngth=textwrap_length,
                     txt_clr=get_txt_clr())


if __name__ == "__main__":
    main()
