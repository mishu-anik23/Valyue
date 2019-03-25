from collections import namedtuple
from tkinter import *
from signaldef import *


COLUMN_COLOR_LIST = [
    '#8EE5EE',
    '#8EE5EE',
    '#8EE5EE',
    '#C1CDCD',
    '#C1CDCD',
    '#C1CDCD',
    '#8EE5EE',
    '#8EE5EE',
    '#C1CDCD',
    '#C1CDCD',
    None,
    None,
]

SignalDetails = namedtuple('SignalDetails', ['name', 'minimum', 'maximum', 'unit'])


class ValidatingEntry(Entry):
    """
    validating entry widgets

    validate(v: str) -> (raw, status)
    indicate(status, widget) -> None
    """

    def __init__(self, master, validate, indicate, **kwargs):
        """
        Initialisation of entry attributes
        + setting up trace for callback
        """
        super().__init__(master, **kwargs)
        self.indicate = indicate
        self.validate = validate
        self._value = "" # str(signal.default)
        self._variable = StringVar()
        self._variable.set(self._value)  # per default set the value from signal configuration
        self._variable.trace('w', self.callback)
        self.config(textvariable=self._variable)
        self.bind('<Return>', self.commit)

    def callback(self, name, mode, index):
        """
        this callback is called whenever the entry field is written.
        the entered value is validated. If validation fails, the background of
        the entry field changes to red, indicating an error to the user.
        """
        raw, status = self.validate(self._variable.get())
        bg_color_indicator(self, status)

    def commit(self, dummy=None):
        val = self._variable.get()
        _, status = self.validate(val)
        if status != "ERROR":
            self._value = val
        print("Your last Entered Value : {}".format(self._value))

    def get_value(self):
        return self._value


class SignalRow:
    """
    Creates a row to display the attributes of two signals.

    All attributes of a signal will be displayed in individual column based on the user given Row.
    """
    row_num = 0
    def __init__(self, master, row, signal_1, signal_2,
                 **kwargs):
        self.__class__.row_num += 1
        self.row = row
        self.gateway = True
        self.signal_active = False

        self._create_entry_measured_value(master, initval_sig1="", initval_sig2="")
        self._create_entry_user_value(master, signal_1, signal_2)
        self._create_chkbtn_gateway(master)
        self._create_chkbtn_signal_active(master)

        self._create_signal_label(master, row=row, column=0,
                                  signame=signal_1.name, minimum=signal_1.minimum, maximum=signal_1.maximum,
                                  unit=signal_1.unit)
        self._create_signal_label(master, row=row, column=3,
                                  signame=signal_2.name, minimum=signal_2.minimum, maximum=signal_2.maximum,
                                  unit=signal_2.unit)

    def commit(self, dummy=None):
        self.entry_sig1.commit()
        self.entry_sig2.commit()

    def _create_signal_label(self, master, row, column, signame, minimum, maximum, unit):
        """
        Creates label for representing the signal 1 & 2 with four main attributes (name, min, max, unit) at the
        user defined row position in the GUI.
        Args:
            master =  Main tkinter frame
            row = Row position given by the user.
            column = Selected column position during the private method call.
            signame = Given names of Signal 1 & 2 during the private method call.
            minimum = Given minimum range of Signal 1 & 2.
            maximum = Given maximum range of Signal 1 & 2.
            unit = Given unit of Signal 1 & 2.
        """
        lbl_name = Label(master, text=signame, bg=COLUMN_COLOR_LIST[column], font=("Helvetica", 12))
        lbl_min = Label(master, text=minimum, bg=COLUMN_COLOR_LIST[column], font=("Helvetica", 9))
        lbl_max = Label(master, text=maximum, bg=COLUMN_COLOR_LIST[column + 1], font=("Helvetica", 9))
        lbl_unit = Label(master, text=unit, bg=COLUMN_COLOR_LIST[column + 2], font=("Helvetica", 9))
        lbl_name.grid(row=row, column=column, columnspan=3, sticky=W+E)
        lbl_min.grid(row=row+1, column=column, sticky=W+E)
        lbl_max.grid(row=row+1, column=column+1, sticky=W+E)
        lbl_unit.grid(row=row+1, column=column+2, sticky=W+E)

    def _create_entry_measured_value(self, master, initval_sig1, initval_sig2):
        """
        Creates Entry for the measured value of the signal 1 & 2. Default is set to empty string.
        Args:
            master =  Main tkinter frame
            initial_value = Initial Value of the measured signal; default = " ".
        """
        self.entry_measured_value_sig1 = StringVar()
        self.entry_measured_value_sig2 = StringVar()
        self.set_measured_value(initval_sig1, initval_sig2)
        entry_sig1 = Entry(master, textvariable=self.entry_measured_value_sig1, width=28)
        entry_sig2 = Entry(master, textvariable=self.entry_measured_value_sig2, width=28)
        entry_sig1.grid(row=self.row, column=6)
        entry_sig2.grid(row=self.row, column=8)
        empty_lbl_1 = Label(master, text="", bg=COLUMN_COLOR_LIST[6], width=24)
        empty_lbl_2 = Label(master, text="", bg=COLUMN_COLOR_LIST[8], width=24)
        empty_lbl_1.grid(row=self.row+1, column=6)
        empty_lbl_2.grid(row=self.row+1, column=8)

    def _create_entry_user_value(self, master, signal1_details, signal2_details):
        """
        Creates Entry for the User given value for the signal 1 & 2. Default is set to empty string.
        Args:
            master =  Main tkinter frame
        """
        # self.entry_user_value_sig1 = StringVar()
        # self.entry_user_value_sig2 = StringVar()
        #self.set_user_value(self.user_value_sig1, self.user_value_sig2)

        validate_sig1 = signal1_details.validate_str_entry
        validate_sig2 = signal2_details.validate_str_entry
        self.entry_sig1 = ValidatingEntry(master, validate=validate_sig1, indicate=bg_color_indicator, width=28)
        self.entry_sig2 = ValidatingEntry(master, validate=validate_sig2, indicate=bg_color_indicator, width=28)
        self.entry_sig1.grid(row=self.row,column=7)
        self.entry_sig2.grid(row=self.row,column=9)
        empty_lbl_1 = Label(master, text="", bg=COLUMN_COLOR_LIST[7], width=24)
        empty_lbl_2 = Label(master, text="", bg=COLUMN_COLOR_LIST[9], width=24)
        empty_lbl_1.grid(row=self.row+1, column=7)
        empty_lbl_2.grid(row=self.row+1, column=9)

    def _create_chkbtn_gateway(self, master):
        """
        Creates CheckButton for selecting the Gateway mode of the signal 1 & signal 2. Default is set to True.
        Args:
            master =  Main tkinter frame
        """
        self.chkbtn_gateway = BooleanVar()
        self.set_gateway(self.gateway)
        chkbtn_gateway = Checkbutton(master, text="Gateway", variable=self.chkbtn_gateway)
        chkbtn_gateway.grid(row=self.row, column=10)

    def _create_chkbtn_signal_active(self, master):
        """
        Creates CheckButton for selecting the Active mode of the signal 1 & signal 2. Default is set to False.
        Args:
            master =  Main tkinter frame
        """
        self.chkbtn_signal_active = BooleanVar()
        self.set_signal_active(self.signal_active)
        chkbtn_sig_act = Checkbutton(master, text="Signal Active", variable=self.signal_active)
        chkbtn_sig_act.grid(row=self.row, column=11)

    def get_user_value(self):
        user_value_sig1 = self.entry_sig1.get_value()
        user_value_sig2 = self.entry_sig2.get_value()

        return user_value_sig1, user_value_sig2

    def set_measured_value(self, value_sig1, value_sig2):
        """
        Set the measured values for 2 signals in the respective Measured value Entry field.
        Args:
            value_sig1 & value_sig2  = To set measured values for 2 signals.
        """
        self.entry_measured_value_sig1.set(value_sig1)
        self.entry_measured_value_sig2.set(value_sig2)

    def get_gateway(self):
        """Get the current status of Gateway CheckButton."""
        return self.gateway

    def set_gateway(self, bool_value):
        """
        Set the status of Gateway CheckButton.
        Args:
           bool_value = True/False or 0/1 which needed to set for changing the Gateway status.
        """
        self.chkbtn_gateway.set(bool_value)

    def get_signal_active(self):
        """Get the current status of Signal Active CheckButton."""
        return self.signal_active

    def set_signal_active(self, bool_value):
        """
        Set the status of Signal Active CheckButton.
        Args:
           bool_value = True/False or 0/1 which needed to set for changing the Signal Active status.
        """
        self.chkbtn_signal_active.set(bool_value)


def create_column_heading_signal_name(master, heading_text, column):
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
    lbl_column_signame = Label(master, text=heading_text, bg=COLUMN_COLOR_LIST[column], font='Helvetica 11 bold')
    lbl_column_signame.grid(row=0, column=column, columnspan=len(subheadings), sticky=W+E)
    for index, element in enumerate(subheadings):
        lbl = Label(master, text=element, bg=COLUMN_COLOR_LIST[column], font='Helvetica 9 bold')
        lbl.grid(row=1, column=column+index, sticky=W+E)


def create_column_heading_signal_widgets(master):
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
        heading_sig_widgets = Label(master, text=label, bg=COLUMN_COLOR_LIST[col], font='Helvetica 11 bold')
        empty_lbl = Label(master, text="", bg=COLUMN_COLOR_LIST[col], width=24)
        heading_sig_widgets.grid(row=0, column=col, sticky=W+E)
        empty_lbl.grid(row=1, column=col)


def bg_color_indicator(widget, status):
    if status == "OK":
        widget.config(bg="green")
    elif status == "WARNING":
        widget.config(bg="yellow")
    else:
        widget.config(bg="red")

def get_frame_inputs(frame):
    inputs = [frame.children[x].get() for x in frame.children if '!validatingentry' in x]
    #print(inputs)
    return inputs


def update_list():
    pass


if __name__ == '__main__':
    root = Tk()
    fr = Frame(master=root)
    #fr.bind('<Return>', get_frame_inputs)

    fr.grid()

    create_column_heading_signal_name(fr, heading_text="Signal Name 1", column=0)
    create_column_heading_signal_name(fr, heading_text="Signal Name 2", column=3)

    create_column_heading_signal_widgets(fr)

    row1 = SignalRow(fr, row=2,
                     signal_1=SignalDefinition(name="Temperature_D", minimum="-40", maximum="165", unit="°C",
                                               physical=Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=16)),
                     signal_2=SignalDefinition(name="Temperature_K", minimum="233.98", maximum="438.35", unit="Kelvin",
                                               physical=Physical(x1=-40, x2=165, y1=1, y2=26241, bitwidth=16)))

    row2 = SignalRow(fr, row=4,
                     signal_1=SignalDefinition(name="Air Pressure_Ps", minimum="0", maximum="600", unit="Pascal",
                                               physical=Physical(x1=0, x2=600, y1=1, y2=60001, bitwidth=16)),
                     signal_2=SignalDefinition(name="Air Pressure_lpb", minimum="149.98", maximum="548.35", unit="Pound",
                                               physical=Physical(x1=0, x2=600, y1=1, y2=60001, bitwidth=16)))

    row3 = SignalRow(fr, row=6,
                     signal_1=SignalDefinition(name="Temperature_D", minimum="-40", maximum="165", unit="°C",
                                               physical=spec_conti(minimum="-40", maximum="165", resolution="0.0078125",
                                                                offset="-40", bitwidth=16)),
                     signal_2=SignalDefinition(name="Temperature_K", minimum="233.98", maximum="438.35", unit="Kelvin",
                                               physical=spec_conti(minimum="233.98", maximum="438.35", resolution="0.0078125",
                                                                   offset="233.98", bitwidth=16)))

    row4 = SignalRow(fr, row=8,
                     signal_1=SignalDefinition(name="Supply Voltage_16", minimum="0", maximum="40.75", unit="V",
                                               physical=spec_conti(minimum="0", maximum="4"
                                                                                        "0.75", resolution="0.009949",
                                                                offset="0", bitwidth=16)),
                     signal_2=SignalDefinition(name="Supply Voltage_8", minimum="0", maximum="40.75", unit="V",
                                               physical=spec_conti(minimum="0", maximum="40.75", resolution="0.16",
                                                                   offset="0", bitwidth=8)))

    row5 = SignalRow(fr, row=10,
                     signal_1=SignalDefinition(name="Temperature_Bosch", minimum="-40.15", maximum="130.10", unit="°C",
                                               physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12)),
                     signal_2=SignalDefinition(name="Differential Air Pressure", minimum="-16", maximum="2", unit="KiloPascal",
                                               physical=Physical(x1=-16, x2=2, y1=193, y2=3896, bitwidth=12)))

    lst = []
    b_update = Button(root, text="Update", command=row1.get_user_value, state=NORMAL)
    b_update.grid(sticky='NE', padx=7)
    print(row2.get_user_value())
    print(SignalRow.row_num)
    root.mainloop()


