from tkinter import *
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageFont, ImageDraw
import os

var_dict = {
    "img_path": "",
    "logo_path": "",
    "font_color": None,
}


# Watermarks are placed with a margin of 1/20 of image width/height
def calculate_position(img, watermark_width, watermark_height, position):
    watermark_position = None
    if position == "Top-Left":
        watermark_position = (
            int(0.05 * img.width),
            int(0.05 * img.height)
        )
    elif position == "Top-Right":
        watermark_position = (
            int(0.95 * img.width - watermark_width),
            int(0.05 * img.height)
        )
    elif position == "Bottom-Left":
        watermark_position = (
            int(0.05 * img.width),
            int(0.95 * img.height - watermark_height)
        )
    elif position == "Bottom-Right":
        watermark_position = (
            int(0.95 * img.width - watermark_width),
            int(0.95 * img.height - watermark_height)
        )
    elif position == "Center":
        watermark_position = (
            int(0.5 * img.width - 0.5 * watermark_width),
            int(0.5 * img.height - 0.5 * watermark_height)
        )
    return watermark_position


# Making sure all required variables are in place
def add_watermark():
    if radio_var.get() == "logo":
        if not var_dict["img_path"]:
            messagebox.showwarning(title="Oops", message="Choose image directory.")
        elif not var_dict["logo_path"]:
            messagebox.showwarning(title="Oops", message="Choose logo file.")
        elif position_input_value.get() == "position":
            messagebox.showwarning(title="Oops", message="Choose positioning.")
        else:
            add_logo_watermark()
    elif radio_var.get() == "text":
        add_text_watermark()


# Pretty much your standard Pillow watermarking
def add_logo_watermark():
    img_path = var_dict["img_path"]
    logo_path = var_dict["logo_path"]
    transparency = transparency_input.get()
    transparency_level = round((transparency / 100) * 255)
    position = position_input_value.get()
    size = size_input.get()
    file_list = os.listdir(img_path)

    for file_name in file_list:

        img = Image.open(f"{img_path}\\{file_name}").convert("RGBA")
        watermark = Image.open(logo_path).convert("RGBA")
        watermark.putalpha(transparency_level)
        watermark_final = watermark.resize((round((size / 100) * img.width), round((size / 100) * img.height)))
        transparent = Image.new(mode="RGBA", size=(img.width, img.height), color=0)
        transparent.paste(img)
        watermark_position = calculate_position(
            img=img,
            watermark_width=watermark_final.width,
            watermark_height=watermark_final.height,
            position=position,
        )
        transparent.paste(im=watermark_final, box=watermark_position, mask=watermark_final)
        save_path = f"watermarked/{file_name.split(sep='.')[0]}.png"
        transparent.save(save_path)
    messagebox.showinfo("Message", "All done!")


def add_text_watermark():
    img_path = var_dict["img_path"]
    transparency = transparency_input.get()
    transparency_level = round((transparency / 100) * 255)
    position = position_input_value.get()
    size = size_input.get()
    file_list = os.listdir(img_path)
    text = text_input.get()
    font_color = var_dict["font_color"]

    for file_name in file_list:

        img = Image.open(f"{img_path}\\{file_name}").convert("RGBA")
        txt = Image.new("RGBA", img.size, (font_color[0], font_color[1], font_color[2], 0))
        draw = ImageDraw.Draw(txt)
        font_size = round(((size / 2) / 100) * img.height)
        font_object = ImageFont.truetype(f"fonts/{font_family.get()}.ttf", font_size)
        txt_width, txt_height = draw.textsize(text=text, font=font_object)
        draw_position = calculate_position(
            img=img,
            position=position,
            watermark_width=txt_width,
            watermark_height=txt_height,
        )
        fill = (font_color[0], font_color[1], font_color[2], transparency_level)
        draw.text(xy=draw_position, text=text, fill=fill, font=font_object)
        watermarked = Image.alpha_composite(img, txt)
        save_path = f"watermarked/{file_name.split(sep='.')[0]}.png"
        watermarked.save(save_path)
    messagebox.showinfo("Message", "All done!")


def select_directory():
    var_dict["img_path"] = filedialog.askdirectory()


def select_file():
    var_dict["logo_path"] = filedialog.askopenfilename(filetypes=(("png files", ".jpg"), ("all files", "*.*")))


def select_color():
    color = colorchooser.askcolor(color="#ffffff", title="Select a color")
    var_dict["font_color"] = color[0]


# ---------------------------UI SETUP ------------------------------ #
window = Tk()
window.title("Watermarking app")
window.config(padx=30, pady=30)

canvas = Canvas(width=640, height=480)
canvas.grid(column=4, row=0, rowspan=6)

# Labels
img_path_label = Label(window, text="Choose base image directory:")
img_path_label.grid(column=0, row=2, pady=5, padx=5)
logo_path_label = Label(window, text="Choose logo file:")
logo_path_label.grid(column=2, row=2, pady=5, padx=5)
position_label = Label(window, text="Choose watermark positioning:")
position_label.grid(column=0, row=3, padx=5, pady=5)
size_label = Label(window, text="Select size:")
size_label.grid(column=2, row=3, padx=5, pady=5)
font_family_label = Label(window, text="Choose font (Text only):")
font_family_label.grid(column=0, row=4, padx=5, pady=5)
transparency_label = Label(window, text="Transparency level:")
transparency_label.grid(column=2, row=4, pady=5, padx=5)
text_label = Label(window, text="Enter watermark text (Text only):")
text_label.grid(column=0, row=5, pady=5, padx=5)
font_color_label = Label(window, text="Select color (Text only):")
font_color_label.grid(column=2, row=5, pady=5, padx=5)

# Inputs
position_input_value = StringVar(window)
position_input_value.set("Position")
position_input = OptionMenu(window, position_input_value, "Center", "Top-Left", "Top-Right", "Bottom-Left",
                            "Bottom-Right")
position_input.config(width=15)
position_input.grid(column=1, row=3, pady=5, padx=5)
font_family = StringVar()
font_family.set("Arial")
values = ["Arial", "Eagle Lake", "IBM Plex Mono", "Jacques Francois", "Quando", "Racing Sans One", "Sacramento",
              "Sail", "Trade Winds", "Verdana", "ZCOOL KuaiLe"]
font_input = OptionMenu(window, font_family, *values)
font_input.config(width=15)
font_input.grid(column=1, row=4, pady=5, padx=5)
transparency_input = Scale(window, from_=0, to=100, orient="horizontal")
transparency_input.set(25)
transparency_input.grid(column=3, row=4, padx=5, pady=5)
size_input = Scale(window, from_=0, to=100, orient="horizontal")
size_input.set(10)
size_input.grid(column=3, row=3, pady=5, padx=5)
text_input = Entry(window, width=36)
text_input.grid(column=1, row=5, padx=5, pady=5)

# Buttons
radio_var = StringVar(None, "logo")
radio_img = Radiobutton(window, text="Logo", variable=radio_var, value="logo")
radio_img.grid(column=0, row=0, pady=5, padx=5)
radio_text = Radiobutton(window, text="Text", variable=radio_var, value="text")
radio_text.grid(column=0, row=1, pady=5, padx=5)
img_path_button = Button(text="Select directory", command=select_directory, width=17)
img_path_button.grid(column=1, row=2, padx=5, pady=5)
logo_path_button = Button(text="Select file", command=select_file, width=17)
logo_path_button.grid(column=3, row=2, pady=5, padx=5)
font_color_button = Button(window, text="Select", command=select_color, width=17)
font_color_button.grid(column=3, row=5, pady=5, padx=5)
add_logo_button = Button(window, text="Add watermark", command=add_watermark, width=17)
add_logo_button.grid(column=0, row=6, padx=30, pady=30)

window.mainloop()
