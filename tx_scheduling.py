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
#     b()
#
# def b():
#     scheduler.enter(2, 1, a)
#
# def print_time():
#     currrent_time = time.ctime(time.time())
#     print("Time = {t}".format(t=currrent_time))


class TxScheduler:
    def __init__(self, mockhw, scheduler):
        self.mockhw = mockhw
        self.scheduler = scheduler
        self.previous_data = None
        self.previous_ts = 0

    def a(self):
        try:
            row = mockhw.get_value_from_row()
        except StopIteration:
            currrent_time = time.ctime(time.time())
            print("on Time = {t} sending Last Data = {d}.".format(t=currrent_time, d=self.previous_data))
            return

        if self.previous_data is None:
            # this is the very first time we are called
            self.previous_ts = row[4]
            interval = self.previous_ts
        else:
            currrent_time = time.ctime(time.time())
            print("on Time = {t} sending Data = {d}.".format(t=currrent_time, d=self.previous_data))
            interval = row[4] - self.previous_ts
            self.previous_ts = row[4]
        self.previous_data = row[3]
        self.b(interval)

    def b(self, interval):
        scheduler.enter(interval, 1, self.a)


if __name__ == '__main__':
    file_content = io.StringIO("""\
Time;Bus;Typ;N0;N1;N2;N3;N4;N5;N6;CRC;Rx Time;Sync Time
0,01456917;1;0;1;11;7;4;15;4;15;9;2;31496
0,02996182;1;0;2;12;7;4;15;5;0;12;3;31496
0,02996182;1;0;3;13;7;4;14;5;1;12;5;31496
0,02996182;1;0;4;11;7;4;13;5;0;12;7;31496
""")
    csv_it = csv.DictReader(file_content, delimiter=';')
    mock_src = convert2int(source=csv_it)
    mockhw = MockHw(source=mock_src)

    scheduler = sched.scheduler(time.time, time.sleep)

    now = time.ctime(time.time())

    print("Start :", now)

    txsched = TxScheduler(mockhw, scheduler)

    scheduler.enter(0, 1, txsched.a)
    #scheduler.enter(0, 1, txsched.c)

    scheduler.run()
