from tkinter import *
from tkinter import messagebox, colorchooser, filedialog
from watermark import Watermark

var_dict = {
    "img_path": "",
    "logo_path": "",
    "font_color": None,
}


def select_directory():
    var_dict["img_path"] = filedialog.askdirectory()


def select_logo():
    filetypes = (
        ("PNG files", ".png"),
        ("JPEG files", ".jpeg"),
        ("PPM files", ".ppm"),
        ("GIF files", ".gif"),
        ("TIFF files", ".tiff"),
        ("BMP files", ".bmp"),
        ("All files", "*.*")
    )
    var_dict["logo_path"] = filedialog.askopenfilename(filetypes=filetypes)


# PyCharm seems to have a problem with this, tried fixing, but no luck, still works though
def select_color():
    color = colorchooser.askcolor(color="#ffffff", title="Select a color")
    var_dict["font_color"] = color[0]


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
            watermark = Watermark(
                img_path=var_dict["img_path"],
                transparency=transparency_input.get(),
                size=size_input.get()
            )
            watermark.add_logo_watermark(
                selected_position=position_input_value.get(),
                logo_path=var_dict["logo_path"]
            )
            messagebox.showinfo(title="Message", message="All done!")

    elif radio_var.get() == "text":
        if not var_dict["img_path"]:
            messagebox.showwarning(title="Oops", message="Choose image directory.")
        elif position_input_value.get() == "Position":
            messagebox.showwarning(title="Oops", message="Choose positioning.")
        elif not text_input.get():
            messagebox.showwarning(title="Oops", message="Enter watermark text.")
        elif not var_dict["font_color"]:
            messagebox.showwarning(title="Oops", message="Chose font color.")
        else:
            watermark = Watermark(
                img_path=var_dict["img_path"],
                transparency=transparency_input.get(),
                size=size_input.get()
            )
            watermark.add_text_watermark(
                font_family=font_family.get(),
                font_color=var_dict["font_color"],
                selected_position=position_input_value.get(),
                text=text_input.get(),
            )
            messagebox.showinfo(title="Message", message="All done!")


# ---------------------------UI SETUP ------------------------------ #
window = Tk()
window.title("Watermarking app")
window.config(padx=30, pady=30)

# Labels
img_path_label = Label(window, text="Choose images directory:")
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
text_input = Entry(window, width=30)
text_input.grid(column=1, row=5, padx=5, pady=5)

# Buttons
radio_var = StringVar(None, "logo")
radio_img = Radiobutton(window, text="Logo", variable=radio_var, value="logo")
radio_img.grid(column=0, row=0, pady=5, padx=5)
radio_text = Radiobutton(window, text="Text", variable=radio_var, value="text")
radio_text.grid(column=0, row=1, pady=5, padx=5)
img_path_button = Button(text="Select directory", command=select_directory, width=17)
img_path_button.grid(column=1, row=2, padx=5, pady=5)
logo_path_button = Button(text="Select file", command=select_logo, width=17)
logo_path_button.grid(column=3, row=2, pady=5, padx=5)
font_color_button = Button(window, text="Select", command=select_color, width=17)
font_color_button.grid(column=3, row=5, pady=5, padx=5)
add_logo_button = Button(window, text="Add watermark", command=add_watermark, width=17)
add_logo_button.grid(column=0, row=6, padx=30, pady=30)

window.mainloop()
