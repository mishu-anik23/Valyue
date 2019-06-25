from tx_scheduling import *
from mockhw import *

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


def test_scheduled_data_storage():
    txsched = TxScheduler(mockhw, scheduler, store_data)
    scheduler.enter(0, 1, txsched.transmit_data)
    scheduler.run()

    assert txsched.data_container == [[1, 11, 7, 4, 15, 4, 15, 9],
                                      [2, 12, 7, 4, 15, 5, 0, 12],
                                      [3, 13, 7, 4, 14, 5, 1, 12],
                                      [4, 11, 7, 4, 13, 5, 0, 12]]
