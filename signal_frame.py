from signaldef import *
from collections import OrderedDict as OD
from parsexml import *

def valid_frames_from_xml():
    xml_file_path = os.path.join(os.getcwd(), "signaldefinition.xml")
    sig_conf = read_sigdef(xml_file_path)
    frames = []
    for fc in range(16):
        frame = get_sig_by_fc(sig_conf, fc)
        if frame:
            frames.append(frame)
    return frames


def signal_details_from_frames():
    signal_details = []
    signal_frames = valid_frames_from_xml()
    for sigs in signal_frames:
        if len(sigs) > 1:
            signal_details.append((sigs[0].get_signal_details(), sigs[1].get_signal_details()))
        else:
            signal_details.append((sigs[0].get_signal_details(), None))
    return signal_details


class SignalFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.sigrows = OD([])
        self._create_button_widget((len(self.sigrows) + 1) * 2)
        self._create_column_heading_signal_frame(column=0)
        self._create_column_heading_signal_name(heading_text="Signal Name 1", column=1)
        self._create_column_heading_signal_name(heading_text="Signal Name 2", column=4)
        self._create_column_heading_signal_widgets()

    def commit(self, dummy=None):
        for row_obj in self.sigrows:
            row_obj.commit()

    def add_signal_row(self, signal_details):
        sigrow = SignalRow(self, row=((len(self.sigrows) + 1) * 2), signal_details=signal_details)
        self.sigrows[signal_details[0].frame_number] = sigrow

    def _create_button_widget(self, row):
        self.b_update = Button(self, text="Update", command=self.commit, state=NORMAL)
        self.b_update.grid(row=row, column=13, sticky='NE', padx=7)

    def get_values(self):
        lst = [row_obj.get_user_value() for row_obj in self.sigrows]
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

    def _create_column_heading_signal_frame(self, column):
        lbl_column_sigframe = Label(self, text="#", bg=COLUMN_COLOR_LIST[column], font='Helvetica 11 bold')
        lbl_column_sigframe.grid(row=0, column=column)

    def _create_column_heading_signal_widgets(self):
        """
        Create the heading of column to display the respective widgets for signal 1 & 2 and also to display the headings of
        the common widgets, which is applicable for both signal 1 & 2.
        Args:
            master = Main tkinter frame
        """
        column_headings_sig_widgets = ["Measured Value 1", "User Value 1", "Measured Value 2", "User Value 2",
                                       "Gateway", "Signal Active"]
        start_index = 7
        for col, label in enumerate(column_headings_sig_widgets, start_index):
            heading_sig_widgets = Label(self, text=label, bg=COLUMN_COLOR_LIST[col], font='Helvetica 11 bold')
            empty_lbl = Label(self, text="", bg=COLUMN_COLOR_LIST[col], width=24)
            heading_sig_widgets.grid(row=0, column=col, sticky=W + E)
            empty_lbl.grid(row=1, column=col)


if __name__ == '__main__':
    root = Tk()
    sigframe = SignalFrame(master=root)
    sigframe.grid()
    for signal_details in signal_details_from_frames():
        sigframe.add_signal_row(signal_details)
    root.mainloop()