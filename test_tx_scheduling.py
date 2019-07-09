from tx_scheduling import *
from mockhw import *


def test_all_scheduled_data_in_a_container():
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
    dc = DataContainer()

    txsched = TxScheduler(mockhw, scheduler, dc.trace_data)
    scheduler.enter(0, 1, txsched.transmit_data)
    scheduler.run()

    assert dc.container == [[1, 11, 7, 4, 15, 4, 15, 9],
                            [2, 12, 7, 4, 15, 5, 0, 12],
                            [3, 13, 7, 4, 14, 5, 1, 12],
                            [4, 11, 7, 4, 13, 5, 0, 12]]


def test_store_scheduled_data_in_container():
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

    scheduler = sched.scheduler(time.time, time.sleep)
    dc = DataContainer()

    txsched = TxScheduler(mockhw, scheduler, dc.trace_data)
    scheduler.enter(0, 1, txsched.transmit_data)
    scheduler.run()

    assert dc.container[0] == [1, 11, 7, 4, 15, 4, 15, 9]
    assert dc.container[2] == [3, 13, 7, 4, 14, 5, 1, 12]

    assert dc.container[-1] == [8, 14, 7, 11, 0, 12, 0, 2]
    assert dc.container[-2] == [7, 2, 8, 0, 4, 2, 3, 3]





