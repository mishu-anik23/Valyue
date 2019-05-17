from tkinter import *
from PIL import Image, ImageTk

#image = Image.open("img_0.gif")
#photo = ImageTk.PhotoImage(image)

if __name__ == '__main__':
    root = Tk()
    img = PhotoImage(file="img_0.gif")
    bl_1 = Label(image=PhotoImage(file="img_0.gif")).grid()
    root.mainloop()