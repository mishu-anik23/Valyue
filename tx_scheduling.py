import sched
import time
from mockhw import *


def store_data(container, data):
    container.append(data)
    return container


def scale_timestamp(time):
    return time * 2.56e-7



class TxScheduler:
    def __init__(self, mockhw, scheduler, trace):
        self.mockhw = mockhw
        self.scheduler = scheduler
        self.previous_data = None
        self.previous_ts = scale_timestamp(0)

        self.trace = trace
        self.data_container = []

    def transmit_data(self):
        try:
            row = self.mockhw.get_value_from_row()
        except StopIteration:
            self.trace(self.data_container, self.previous_data)
            print(self.data_container)
            return

        if self.previous_data is None:
            # this is the very first time we are called
            self.previous_ts = scale_timestamp(row[4])
            start_time = scale_timestamp(row[4]) - self.previous_ts
            interval = start_time
        else:
            self.trace(self.data_container, self.previous_data)
            interval = scale_timestamp(row[4]) - self.previous_ts
            self.previous_ts = scale_timestamp(row[4])

        self.previous_data = row[3]
        self.event_scheduler(interval)
        print(self.data_container)
        print(len(self.data_container))
        print(interval)

    def event_scheduler(self, interval):
        self.scheduler.enter(interval, 1, self.transmit_data)


if __name__ == '__main__':
    file_content = io.StringIO("""\
Time;Bus;Typ;N0;N1;N2;N3;N4;N5;N6;CRC;Rx Time;Sync Time
0,01456917;1;0;1;11;7;4;15;4;15;9;122770661;31496
0,02996182;1;0;2;12;7;4;15;5;0;12;122777518;31496
0,02996182;1;0;3;13;7;4;14;5;1;12;122785429;31496
0,02996182;1;0;4;11;7;4;13;5;0;12;122792706;31496
""")
    csv_it = csv.DictReader(file_content, delimiter=';')
    #mock_src = convert2int(source=csv_it)

    in_file_pth = os.path.join(os.getcwd(), 'data/SENT_Trace_MUX_2016-11-14.csv')
    to_remove = ['Stat/Err', 'Skipped']
    rows_d = discard_rows(source=csv_read_from_file(in_file_pth), criterion=type_is_512)
    rows_dc = discard_columns(rows_d, to_remove)

    mock_src = convert2int(source=rows_dc)

    mockhw = MockHw(source=mock_src)

    scheduler = sched.scheduler(time.time, time.sleep)

    now = time.ctime(time.time())

    print("Start :", now)

    txsched = TxScheduler(mockhw, scheduler, trace=store_data)

    scheduler.enter(0, 1, txsched.transmit_data)
    #scheduler.enter(0, 1, txsched.c)

    scheduler.run()
