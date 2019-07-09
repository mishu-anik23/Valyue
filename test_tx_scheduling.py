import pytest
import sched
import time
from mockhw import *
from tx_scheduling import *


class DataContainer:
    def __init__(self):
        self.container = []
        self.time_info = []

    def trace_data(self, data):
        self.container.append(data)
        self.time_info.append(time.perf_counter())


@pytest.fixture()
def mockhw():
    file_content = io.StringIO("""\
Time;Bus;Typ;N0;N1;N2;N3;N4;N5;N6;CRC;Rx Time;Sync Time
0,01456917;1;0;1;11;7;4;15;4;15;9;122770661;31496
0,02996182;1;0;2;12;7;4;15;5;0;12;122777518;31496
0,02996182;1;0;3;13;7;4;14;5;1;12;122785429;31496
0,02996182;1;0;4;11;7;4;13;5;0;12;122792706;31496
0,06136637;1;0;5;14;7;11;0;12;0;2;122799773;31495
0,06136637;1;0;6;8;1;14;10;4;15;3;122807016;31495
0,06136637;1;0;7;2;8;0;4;2;3;3;122820800;31495
0,06136637;1;0;8;14;7;11;0;12;0;2;122840561;31495
""")
    csv_it = csv.DictReader(file_content, delimiter=';')

    mock_src = convert2int(source=csv_it)
    mockhw = MockHw(source=mock_src)
    return mockhw


def test_store_scheduled_time(mockhw):
    sched3 = sched.scheduler(time.time, time.sleep)
    dc3 = DataContainer()

    txsched3 = TxScheduler(mockhw, sched3, dc3.trace_data)
    sched3.enter(0, 1, txsched3.transmit_data)
    sched3.run()

    assert dc3.time_info[2] - dc3.time_info[1] == pytest.approx((122785429 * 2.56e-6) - (122777518 * 2.56e-6), 0.1)


def test_all_scheduled_data_in_a_container(mockhw):
    sched1 = sched.scheduler(time.time, time.sleep)
    dc1 = DataContainer()

    txsched1 = TxScheduler(mockhw, sched1, dc1.trace_data)
    sched1.enter(0, 1, txsched1.transmit_data)
    sched1.run()

    assert dc1.container == [[1, 11, 7, 4, 15, 4, 15, 9],
                             [2, 12, 7, 4, 15, 5, 0, 12],
                             [3, 13, 7, 4, 14, 5, 1, 12],
                             [4, 11, 7, 4, 13, 5, 0, 12],
                             [5, 14, 7, 11, 0, 12, 0, 2],
                             [6, 8, 1, 14, 10, 4, 15, 3],
                             [7, 2, 8, 0, 4, 2, 3, 3],
                             [8, 14, 7, 11, 0, 12, 0, 2]]


def test_store_scheduled_data_in_container(mockhw):
    sched2 = sched.scheduler(time.time, time.sleep)
    dc2 = DataContainer()

    txsched2 = TxScheduler(mockhw, sched2, dc2.trace_data)
    sched2.enter(0, 1, txsched2.transmit_data)
    sched2.run()

    assert dc2.container[0] == [1, 11, 7, 4, 15, 4, 15, 9]
    assert dc2.container[2] == [3, 13, 7, 4, 14, 5, 1, 12]

    assert dc2.container[-1] == [8, 14, 7, 11, 0, 12, 0, 2]
    assert dc2.container[-2] == [7, 2, 8, 0, 4, 2, 3, 3]






