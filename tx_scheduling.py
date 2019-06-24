import sched
import time
from mockhw import *



#Scheduler: A.act()
# A: get row from file
#A: B.act()
#B: Scheduler.enter()
#A: C.act()

# def a():
#     #row = mockhw.get_value_from_row()
#     currrent_time = time.ctime(time.time())
#     print(" Time = {t}.".format(t=currrent_time))
#     event_scheduler()
#
# def event_scheduler():
#     scheduler.enter(2, 1, a)
#
# def print_time():
#     currrent_time = time.ctime(time.time())
#     print("Time = {t}".format(t=currrent_time))

def trace_data(data, val):
    #all_data = []
    #all_data.extend(data)
    #return all_data
    data.append(val)
    return data

def scale_timestamp(time):
    return time * 2.56e-6



class TxScheduler:
    def __init__(self, mockhw, scheduler, trace):
        self.mockhw = mockhw
        self.scheduler = scheduler
        self.previous_data = None
        self.previous_ts = scale_timestamp(0)
        self.trace = trace
        self.data = []

    def transmit_data(self):
        try:
            row = self.mockhw.get_value_from_row()
        except StopIteration:
            #currrent_time = time.ctime(time.time())
            currrent_time = time.time()
            # print("on Time = {t} sending Last Data = {d}.".format(t=currrent_time, d=self.previous_data))
            self.trace(self.data, self.previous_data)
            print(self.data)
            return

        if self.previous_data is None:
            # this is the very first time we are called
            self.previous_ts = scale_timestamp(row[4])
            interval = self.previous_ts
        else:
            currrent_time = time.ctime(time.time())
            #print("on Time = {t} sending Data = {d}.".format(t=currrent_time, d=self.previous_data))
            self.trace(self.data, self.previous_data)
            interval = scale_timestamp(row[4]) - self.previous_ts
            self.previous_ts = scale_timestamp(row[4])
        self.previous_data = row[3]
        self.event_scheduler(interval)
        print(self.data)
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
    mock_src = convert2int(source=csv_it)
    mockhw = MockHw(source=mock_src)

    scheduler = sched.scheduler(time.time, time.sleep)

    now = time.ctime(time.time())

    print("Start :", now)

    txsched = TxScheduler(mockhw, scheduler, trace=trace_data)

    scheduler.enter(0, 1, txsched.transmit_data)
    #scheduler.enter(0, 1, txsched.c)

    scheduler.run()
