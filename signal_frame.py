from signalrow_valid import *
from signaldef import *


sd1 = get_signal_details(SignalDefinition(name="Temperature_D", minimum="-40", maximum="165", unit="°C",
                                          physical=Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=16)))
sd2 = get_signal_details(SignalDefinition(name="Temperature_K", minimum="233.98", maximum="438.35",
                                          unit="Kelvin",
                                          physical=Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=16)))

sd3 = get_signal_details(SignalDefinition(name="Air Pressure_Ps", minimum="0", maximum="600", unit="Pascal",
                                                   physical=Physical(x1=0, x2=600, y1=1, y2=60001, bitwidth=16)))

sd4 = get_signal_details(SignalDefinition(name="Air Pressure_lpb", minimum="149.98", maximum="548.35",
                                                   unit="Pound",
                                                   physical=Physical(x1=0, x2=600, y1=1, y2=60001, bitwidth=16)))

sd5 = get_signal_details(SignalDefinition(name="Temperature_Bosch", minimum="-40.15", maximum="130.10",
                                                   unit="°C",
                                                   physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626,
                                                                     bitwidth=12)))

sd6 = get_signal_details(SignalDefinition(name="Differential Air Pressure", minimum="-16", maximum="2",
                                                   unit="KiloPascal",
                                                   physical=Physical(x1=-16, x2=2, y1=193, y2=3896, bitwidth=12)))


class SignalFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.sigrows = []


        row = SignalRow(self, row=2, signal1_details=sd1, signal2_details=sd2)
        self.sigrows.append(row)

        row = SignalRow(self, row=4, signal1_details=sd3, signal2_details=sd4)
        self.sigrows.append(row)

        row = SignalRow(self, row=6, signal1_details=sd5, signal2_details=sd6)
        self.sigrows.append(row)

        self._create_button_widget()
        self._create_column_heading_signal_name(heading_text="Signal Name 1", column=0)
        self._create_column_heading_signal_name(heading_text="Signal Name 2", column=3)
        self._create_column_heading_signal_widgets()

    def commit(self, dummy=None):
        for row_obj in self.sigrows:
            row_obj.commit()

    def _create_button_widget(self):
        self.b_update = Button(self, text="Update", command=self.commit, state=NORMAL)
        self.b_update.grid(row=7, column=12, sticky='NE', padx=7)

    def get_values(self):
        lst = [row_obj.get_user_value() for row_obj in self.sigrows]
        print(lst)
        return lst

    def _create_column_heading_signal_name(self, heading_text, column):
        """
        Create the Heading of column to display the name of signal 1 & 2.

        Subheadings will be displayed into individual column by spanning the main column.

        By default signal Name heading will be created on row position 0 & subheadings on row position 1.

        To get the actual signal row, user should start the row from position 2.
        Args:
            master = Main tkinter frame
            heading_text = given name for signal 1 & 2 during method call.
            column = given column number during method call.
        """
        subheadings = ["Minimum", "Maximum", "Unit"]
        lbl_column_signame = Label(self, text=heading_text, bg=COLUMN_COLOR_LIST[column], font='Helvetica 11 bold')
        lbl_column_signame.grid(row=0, column=column, columnspan=len(subheadings), sticky=W + E)
        for index, element in enumerate(subheadings):
            lbl = Label(self, text=element, bg=COLUMN_COLOR_LIST[column], font='Helvetica 9 bold')
            lbl.grid(row=1, column=column + index, sticky=W + E)

    def _create_column_heading_signal_widgets(self):
        """
        Create the heading of column to display the respective widgets for signal 1 & 2 and also to display the headings of
        the common widgets, which is applicable for both signal 1 & 2.
        Args:
            master = Main tkinter frame
        """
        column_headings_sig_widgets = ["Measured Value 1", "User Value 1", "Measured Value 2", "User Value 2",
                                       "Gateway", "Signal Active"]
        start_index = 6
        for col, label in enumerate(column_headings_sig_widgets, start_index):
            heading_sig_widgets = Label(self, text=label, bg=COLUMN_COLOR_LIST[col], font='Helvetica 11 bold')
            empty_lbl = Label(self, text="", bg=COLUMN_COLOR_LIST[col], width=24)
            heading_sig_widgets.grid(row=0, column=col, sticky=W + E)
            empty_lbl.grid(row=1, column=col)

if __name__ == '__main__':
    root = Tk()
    sigframe = SignalFrame(master=root)
    sigframe.grid()
    root.mainloop()