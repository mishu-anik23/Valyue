from tx_scheduling import *
from mockhw import *


file_content_g = io.StringIO("""\
Time;Bus;Typ;N0;N1;N2;N3;N4;N5;N6;CRC;Rx Time;Sync Time
0,01456917;1;0;1;11;7;4;15;4;15;9;122770661;31496
0,02996182;1;0;2;12;7;4;15;5;0;12;122777518;31496
0,02996182;1;0;3;13;7;4;14;5;1;12;122785429;31496
0,02996182;1;0;4;11;7;4;13;5;0;12;122792706;31496
""")
csv_it_g = csv.DictReader(file_content_g, delimiter=';')

mock_src_g = convert2int(source=csv_it_g)
mockhw_g = MockHw(source=mock_src_g)

scheduler_g = sched.scheduler(time.time, time.sleep)


def test_dcobj_previous_data_attrs_only_stores_last_data():
    txsched = TxScheduler(mockhw_g, scheduler_g, tracing_data)
    scheduler_g.enter(0, 1, txsched.transmit_data)
    scheduler_g.run()

    assert txsched.storage.previous_data == [4, 11, 7, 4, 13, 5, 0, 12]
    assert txsched.storage.previous_data == [4, 11, 7, 4, 13, 5, 0, 12]


def test_trace_func_returns_none():
    txsched = TxScheduler(mockhw_g, scheduler_g, tracing_data)
    scheduler_g.enter(0, 1, txsched.transmit_data)
    scheduler_g.run()

    assert tracing_data(txsched.storage.previous_data) is None


def test_dcobj_previous_ts_attrs_only_stores_last_rx_time():
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

    txsched = TxScheduler(mockhw, scheduler, tracing_data)
    scheduler.enter(0, 1, txsched.transmit_data)
    scheduler.run()

    assert txsched.storage.previous_ts == 122792706 * 2.56e-6

    assert txsched.storage.interval == 122792706 * 2.56e-6 - 122785429 * 2.56e-6



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

    txsched = TxScheduler(mockhw, scheduler, tracing_data)
    scheduler.enter(0, 1, txsched.transmit_data)
    scheduler.run()

    assert txsched.storage.container == [[1, 11, 7, 4, 15, 4, 15, 9],
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
""")
    csv_it = csv.DictReader(file_content, delimiter=';')
    mock_src = convert2int(source=csv_it)
    mockhw = MockHw(source=mock_src)

    scheduler1 = sched.scheduler(time.time, time.sleep)

    txsched1 = TxScheduler(mockhw, scheduler1, tracing_data)
    scheduler1.enter(0, 1, txsched1.transmit_data)
    scheduler1.run()

    assert txsched1.storage.container[0] == [1, 11, 7, 4, 15, 4, 15, 9]
    assert txsched1.storage.container[1] == [2, 12, 7, 4, 15, 5, 0, 12]
    assert txsched1.storage.container[2] == [3, 13, 7, 4, 14, 5, 1, 12]





