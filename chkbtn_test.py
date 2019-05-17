import os
from tkinter import *
from PIL import ImageTk, Image


def select_image():
    img_pth = os.path.join(os.getcwd(), "green.png")
    img = Image.open(img_pth)
    img = img.resize((10,10), Image.ANTIALIAS)
    photoimg = ImageTk.PhotoImage(img)
    return photoimg


def deselect_image():
    img_pth = os.path.join(os.getcwd(), "red.png")
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
        for i in range(self.bitwidth):
            if value & 1:
                self.chkbtns_bitfield[i].deselect()
            else:
                self.chkbtns_bitfield[i].select()
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


class BitLabel(Frame):
    def __init__(self, master, bitwidth, value, **kwargs):
        super().__init__(master)
        self.bitwidth = bitwidth
        self.select_img = select_image()
        self.deselect_img = deselect_image()
        self.labels_bitfield = []
        for col in range(bitwidth):
            lbl_bitfield = Label(self,**kwargs)
            # To avoid None type, Geometry mngr should call on created instance in new line :
            lbl_bitfield.grid(row=0, column=col)
            #self._create_label_group(col*4)
            if col and not col%4:
                Label(self).grid(row=0, column=col)
            self.labels_bitfield.append(lbl_bitfield)

        self.set_value(value)

    def set_value(self, value):
        for bitlabel in self.labels_bitfield:
            if value & 1:
                 bitlabel.config(image=self.deselect_img)
            else:
                 bitlabel.config(image=self.select_img)
            value >>= 1


    def _create_label_group(self, col):
        for i in range(4):
            bitlbl = Label(self)
            bitlbl.grid(row=0, column=col+i)
            self.labels_bitfield.append(bitlbl)


if __name__ == '__main__':
    root = Tk()
    bitframe = BitArray(master=root, bitwidth=12, value=423, borderwidth=0)#, highlightthickness=0)
    bitframe.grid()
    bitlabel = BitLabel(master=root, bitwidth=12, value=423)
    bitlabel.grid()
    root.mainloop()
