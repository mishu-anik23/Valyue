import os
from tkinter import *
from PIL import ImageTk, Image


def select_image():
    img_pth = os.path.join(os.getcwd(), "Start-icon.png")
    img = Image.open(img_pth)
    img = img.resize((10,10), Image.ANTIALIAS)
    photoimg = ImageTk.PhotoImage(img)
    return photoimg


def deselect_image():
    img_pth = os.path.join(os.getcwd(), "Stop-red-icon.png")
    img = Image.open(img_pth)
    img = img.resize((10,10), Image.ANTIALIAS)
    photoimg = ImageTk.PhotoImage(img)
    return photoimg


class BitArray(Frame):
    def __init__(self, master, bitwidth, value, **kwargs):
        super().__init__(master)
        self.bitwidth = bitwidth
        self.chkbtns_bitfield = []
        for col in range(bitwidth):
            var = IntVar()
            chkbtn_bitfield = Checkbutton(self, variable=var, **kwargs)
            chkbtn_bitfield.grid(row=0, column=col, padx=(0, 0), pady=(0, 0))
            chkbtn_bitfield.var = var
            self.chkbtns_bitfield.append(chkbtn_bitfield)
        self.set_value(value)

    def set_value(self, value):
        for i in reversed(range(self.bitwidth)):
            if value & 1:
                self.chkbtns_bitfield[i].select()
            else:
                self.chkbtns_bitfield[i].deselect()
            value >>= 1

    def get_value(self):
        bits = []
        for chkbtn in self.chkbtns_bitfield:
            bit = chkbtn.var.get()
            bits.append(bit)
        ret_num = 0
        for bit in bits:
            ret_num <<= 1
            ret_num = ret_num | bit
        return ret_num


class BitLabel(Label):
    def __init__(self, master, on_image, off_image, **kwargs):
        super().__init__(master)
        self._value = 0
        self.select_img = on_image
        self.deselect_img = off_image

    def set_value(self, value):
        self._value = value
        if value:
            self.config(image=self.select_img)
        else:
            self.config(image=self.deselect_img)

    def get_value(self):
        return self._value


class BitArray2(Frame):
    def __init__(self, master, bitwidth, value, **kwargs):
        super().__init__(master)
        self.select_img = select_image()
        self.deselect_img = deselect_image()
        self.bitlabels = []
        for col in range(bitwidth):
            if col and not col % 4:
                Label(self, text="").pack(side=LEFT, fill=Y)
            bitlbl = BitLabel(self,
                              on_image=self.select_img,
                              off_image=self.deselect_img,
                              **kwargs)
            bitlbl.pack(side=LEFT, fill=Y)
            self.bitlabels.append(bitlbl)
        self.set_value(value)

    def set_value(self, value):
        for bitlabel in reversed(self.bitlabels):
            bitlabel.set_value(value&1)
            value >>= 1

    def get_value(self):
        value = 0
        for bitlbl in self.bitlabels:
            value <<= 1
            value += bitlbl.get_value()
        return value



if __name__ == '__main__':
    root = Tk()
    bitframe = BitArray(master=root, bitwidth=12, value=254, borderwidth=0)#, highlightthickness=0)
    bitframe.grid()
    bitlabel = BitArray2(master=root, bitwidth=12, value=254)
    bitlabel.grid()
    print(bitframe.get_value())
    print(bitlabel.get_value())
    root.mainloop()
