from tkinter import *
from PIL import Image, ImageFont, ImageDraw
import os


class Watermark:

    def __init__(self, img_path, transparency, size):
        self.img_path = img_path
        self.transparency = round((transparency / 100) * 255)
        self.position = None
        self.size = size

    # Watermarks are placed with a margin of 5% of image width/height
    def calculate_position(self, img, watermark_width, watermark_height, selected_position):
        watermark_position = None
        if selected_position == "Top-Left":
            watermark_position = (
                round(0.05 * img.width),
                round(0.05 * img.height)
            )
        elif selected_position == "Top-Right":
            watermark_position = (
                round(0.95 * img.width - watermark_width),
                round(0.05 * img.height)
            )
        elif selected_position == "Bottom-Left":
            watermark_position = (
                round(0.05 * img.width),
                int(0.95 * img.height - watermark_height)
            )
        elif selected_position == "Bottom-Right":
            watermark_position = (
                round(0.95 * img.width - watermark_width),
                round(0.95 * img.height - watermark_height)
            )
        elif selected_position == "Center":
            watermark_position = (
                round(0.5 * img.width - 0.5 * watermark_width),
                round(0.5 * img.height - 0.5 * watermark_height)
            )
        self.position = watermark_position


    def add_logo_watermark(self, selected_position, logo_path):

        img_list = os.listdir(self.img_path)

        for file_name in img_list:

            img = Image.open(f"{self.img_path}\\{file_name}").convert("RGBA")
            watermark = Image.open(logo_path).convert("RGBA")
            watermark.putalpha(self.transparency)
            watermark_final = watermark.resize((
                round((self.size / 100) * img.width),
                round((self.size / 100) * img.height)))
            transparent = Image.new(mode="RGBA", size=(img.width, img.height), color=0)
            transparent.paste(img)
            self.calculate_position(
                img=img,
                watermark_width=watermark_final.width,
                watermark_height=watermark_final.height,
                selected_position=selected_position,
            )
            transparent.paste(im=watermark_final, box=self.position, mask=watermark_final)
            save_path = f"watermarked/{file_name.split(sep='.')[0]}.png"
            transparent.save(save_path)


    def add_text_watermark(self, selected_position, text, font_family, font_color):

        img_list = os.listdir(self.img_path)

        for file_name in img_list:

            img = Image.open(f"{self.img_path}\\{file_name}").convert("RGBA")
            txt = Image.new("RGBA", img.size, (font_color[0], font_color[1], font_color[2], 0))
            draw = ImageDraw.Draw(txt)
            font_size = round(((self.size / 2) / 100) * img.height)
            font_object = ImageFont.truetype(f"fonts/{font_family}.ttf", font_size)
            txt_width, txt_height = draw.textsize(text=text, font=font_object)
            self.calculate_position(
                img=img,
                watermark_width=txt_width,
                watermark_height=txt_height,
                selected_position=selected_position,
            )
            fill = (font_color[0], font_color[1], font_color[2], self.transparency)
            draw.text(xy=self.position, text=text, fill=fill, font=font_object)
            watermarked = Image.alpha_composite(img, txt)
            save_path = f"watermarked/{file_name.split(sep='.')[0]}.png"
            watermarked.save(save_path)
