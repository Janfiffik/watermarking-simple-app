import tkinter as tk
from tkinter import filedialog
import win32gui
from PIL import Image, ImageTk, ImageGrab, ImageFont, ImageDraw


def add_watermark():
    global new_image
    text = textBox.get()
    image = ImageTk.getimage(ph)

    text_image = Image.new("RGBA", image.size, (0, 0, 0, 0))

    # you can change font here
    font = ImageFont.truetype("BeckyTahlia.ttf", 140)
    d = ImageDraw.Draw(text_image)

    # get coordination for text
    size = image.size
    width_x = int(size[0]/4)
    height_y = int(size[1]/2)

    d.text((width_x, height_y), text, fill=(150, 150, 150, 130), font=font)
    combined = Image.alpha_composite(image, text_image)
    new_image = ImageTk.PhotoImage(combined)
    show_image(size[0], size[1], image=new_image)


def show_image(width, height, image):
    image_space.create_image(0, 0, anchor=tk.NW, image=image)
    image_space.itemconfigure(image, image=image, bd=0, highlightthickness=0, relief='ridge')
    image_space.grid(row=1, column=0, columnspan=2)

    # adjust window size
    adjust_wind_geometry(width, height)
    window.configure(borderwidth="5", bg="#cccccc")


def adjust_wind_geometry(width, height):
    window.geometry(f"{width+10}x{height+100}")


def open_image():
    global ph, image_space, width, height, textBox

    # open window for choosing image
    filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *jpeg")])
    image = Image.open(filename)

    # get size of an image
    size = image.size
    width = int(size[0]/2)
    height = int(size[1]/2)

    # creates an instance of canvas
    image_space = tk.Canvas(master=window, width=width, height=height, bd=0, highlightthickness=0, relief='ridge')

    # resize image
    im = Image.open(filename)
    im.thumbnail((width, height))
    ph = ImageTk.PhotoImage(im)

    show_image(width, height, ph)

    # Text_box fore watermark
    text_box_label = tk.Label(text="Add watermark text:", bg="#cccccc")
    textBox = tk.Entry()
    textBox.grid(row=2, column=1)
    text_box_label.grid(row=2, column=0)

    # watermark button
    watermark_button = tk.Button(text="Add watermark", command=add_watermark)
    watermark_button.grid(row=3, column=1)

    # save image button
    save_button = tk.Button(text="save image", command=save_img)
    save_button.grid(row=3, column=0)


def save_img():
    HWND = image_space.winfo_id()
    rect = win32gui.GetWindowRect(HWND)
    im = ImageGrab.grab(rect)
    path = filedialog.asksaveasfile(filetypes=[("Image Files", "*.png *.jpg *jpeg")], initialdir="/")
    im.save(path)

# Creates window
window = tk.Tk()
window.title("Watermark app")
window.configure(borderwidth="5", bg="#cccccc")
window.geometry("270x100")

# add image button
add_button = tk.Button(text="Open image", command=open_image)
add_button.grid(row=0, column=0)

window.mainloop()
