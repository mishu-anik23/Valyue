import sched
import time
from mockhw import *



#Scheduler: A.act()
# A: get row from file
#A: B.act()
#B: Scheduler.enter()
#A: C.act()

def a():
    #row = mockhw.get_value_from_row()
    currrent_time = time.ctime(time.time())
    print(" Time = {t}.".format(t=currrent_time))
    b()

def b():
    scheduler.enter(2, 1, a)

def print_data(data):
    currrent_time = time.ctime(time.time())
    print("on Time = {t} sending Data = {d}.".format(t=currrent_time, d=data))


class TxScheduler:
    def __init__(self, mockhw, scheduler):
        self.mockhw = mockhw
        self.scheduler = scheduler

    def a(self):
        row = mockhw.get_value_from_row()
        currrent_time = time.ctime(time.time())
        print(" Time = {t}.".format(t=currrent_time))
        self.b()

    def b(self):
        scheduler.enter(2, 1, self.a)


if __name__ == '__main__':
    file_content = io.StringIO("""\
Time;Bus;Typ;N0;N1;N2;N3;N4;N5;N6;CRC;Rx Time;Sync Time
2,47e-6;1;0;8;10;7;5;10;1;1;1;5;31495
0,01456917;1;0;8;11;7;4;15;4;15;9;10;31496
0,02996182;1;0;0;12;7;4;15;5;0;12;12;31496
""")
    csv_it = csv.DictReader(file_content, delimiter=';')
    mock_src = convert2int(source=csv_it)
    mockhw = MockHw(source=mock_src)

    scheduler = sched.scheduler(time.time, time.sleep)

    now = time.ctime(time.time())

    print("Start :", now)

    txsched = TxScheduler(mockhw, scheduler)

    scheduler.enter(0, 1, txsched.a)

    scheduler.run()
