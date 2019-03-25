from signalrow_valid import *
from signaldef import *


class SignalFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        #self._create_button_widget(master=self.main_frame)
        #self.get_frame_inputs()
        #self._create_button_widget()
        self.sigrows = []

        self.row1 = SignalRow(master, row=2,
                     signal_1=SignalDefinition(name="Temperature_D", minimum="-40", maximum="165", unit="°C",
                                               physical=Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=16)),
                     signal_2=SignalDefinition(name="Temperature_K", minimum="233.98", maximum="438.35", unit="Kelvin",
                                               physical=Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=16)))
        self.sigrows.append(self.row1)
        self.row2 = SignalRow(master, row=4,
                     signal_1=SignalDefinition(name="Temperature_Bosch", minimum="-40.15", maximum="130.10", unit="°C",
                                               physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12)),
                     signal_2=SignalDefinition(name="Differential Air Pressure", minimum="-16", maximum="2", unit="KiloPascal",
                                               physical=Physical(x1=-16, x2=2, y1=193, y2=3896, bitwidth=12)))
        self.sigrows.append(self.row2)


    def _create_button_widget(self, master):

        self.b_update = Button(master, text="Update", command=self.get_values(self.sigrows), state=NORMAL)
        self.b_update.grid(row=5, column=12, sticky='NE', padx=7)

    def get_values(self, list):
        return [row_obj.get_user_value() for row_obj in list]





if __name__ == '__main__':
    root = Tk()
    sigframe = SignalFrame(master=root)
    create_column_heading_signal_name(root, heading_text="Signal Name 1", column=0)
    create_column_heading_signal_name(root, heading_text="Signal Name 2", column=3)

    create_column_heading_signal_widgets(root)
    #sigframe.grid()
    print(sigframe.sigrows)
    root.mainloop()