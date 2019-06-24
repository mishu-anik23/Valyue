from tx_scheduling import *
from mockhw import *

file_content = io.StringIO("""\
Time;Bus;Typ;N0;N1;N2;N3;N4;N5;N6;CRC;Rx Time;Sync Time
0,01456917;1;0;1;11;7;4;15;4;15;9;2;31496
0,02996182;1;0;2;12;7;4;15;5;0;12;3;31496
0,02996182;1;0;3;13;7;4;14;5;1;12;5;31496
0,02996182;1;0;4;11;7;4;13;5;0;12;6;31496
""")
csv_it = csv.DictReader(file_content, delimiter=';')
mock_src = convert2int(source=csv_it)
mockhw = MockHw(source=mock_src)

scheduler = sched.scheduler(time.time, time.sleep)


def test_txsched_previous_data():
    txsched = TxScheduler(mockhw, scheduler, trace_data)
    scheduler.enter(0, 1, txsched.transmit_data)


    assert scheduler.run() == []
