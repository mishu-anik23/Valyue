import csv
import io
import pytest

from mockhw_ascii import *

sig_in_1st = SignalDefinition(name="prs_rag", minimum='-40.15', maximum='130.10', unit='C',
                              physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                              encoding=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                              default=-21.671875)

sig_in_2nd = SignalDefinition(name="state_com_sens_sent[UREA_PRS]",  minimum='-40.15', maximum='130.10', unit='C',
                              physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                              encoding=SignalEncoding(bitwidth=12, msn=6, lsn=4),
                              default=-21.671875)

sig_in_3rd = SignalDefinition(name="prs_rag_sent", minimum='-16', maximum='2', unit='kPa',
                              physical=Physical(x1=-16, x2=2, y1=193, y2=3896, bitwidth=12),
                              encoding=SignalEncoding(bitwidth=12, msn=1, lsn=3),
                              default=-16.938)

sig_in_4th = SignalDefinition(name="t_dly_diag_inh_sens_sent", minimum='-40.15', maximum='130.10', unit='C',
                              physical=Physical(x1=-40.15, x2=130.10, y1=264, y2=1626, bitwidth=12),
                              encoding=SignalEncoding(bitwidth=12, msn=6, lsn=4),
                              default=-21.671875)


@pytest.fixture()
def processed_ascii():
    ascii2csv_file_content =io.StringIO("""\
time,prs_rag,prs_rag_sent,state_com_sens_sent[UREA_PRS],t_dly_diag_inh_sens_sent
9.841098354638689e-002,-0.13671875,-0.1337890625,8.0,24.43
0.1085597930283484,-0.140625,-0.1474609375,8.0,24.44
0.1182596551076358,-0.13671875,-0.130859375,0.0,24.45
0.129234367556478,-0.140625,-0.1474609375,4.0,24.46
0.1383462984846346,-0.1435546875,-0.1474609375,4.0,24.47
0.1493690051530621,-0.14453125,-0.14453125,12.0,24.48
0.1592528453799105,-0.142578125,-0.140625,8.0,24.49
0.1685217577020239,-0.1416015625,-0.140625,12.0,24.50""")

    csv_row = csv.DictReader(ascii2csv_file_content)
    return csv_row


def test_translate_headers_ascii_to_sent():
    headers_in = ['A', 'B', 'X', 'W', 'C']
    conversion_dct = {'A': 'Apple', 'B': 'Ball', 'C': 'Cat'}

    assert translate_headers(headers=headers_in, mapping=conversion_dct) == ['Apple', 'Ball', 'X', 'W', 'Cat']


def test_signal_row_generator_with_time_and_one_signal_1(processed_ascii):
    signal_row = signal_row_generator(source=processed_ascii, signal1=sig_in_1st)

    assert next(signal_row) == {'time': '9.841098354638689e-002', 'prs_rag': '-0.13671875'}
    assert next(signal_row) == {'time': '0.1085597930283484', 'prs_rag': '-0.140625'}


def test_signal_row_generator_with_time_and_one_signal_2(processed_ascii):
    signal_row = signal_row_generator(source=processed_ascii, signal1=sig_in_2nd)

    assert next(signal_row) == {'time': '9.841098354638689e-002', 'state_com_sens_sent[UREA_PRS]': '8.0'}
    assert next(signal_row) == {'time': '0.1085597930283484', 'state_com_sens_sent[UREA_PRS]': '8.0'}


def test_signal_row_generator_with_time_and_one_signal_3(processed_ascii):
    signal_row = signal_row_generator(source=processed_ascii, signal1=sig_in_3rd)

    assert next(signal_row) == {'time': '9.841098354638689e-002', 'prs_rag_sent': '-0.1337890625'}
    assert next(signal_row) == {'time': '0.1085597930283484', 'prs_rag_sent': '-0.1474609375'}


def test_signal_row_generator_with_time_and_two_signal_1(processed_ascii):
    signal_row = signal_row_generator(source=processed_ascii, signal1=sig_in_1st, signal2=sig_in_3rd)

    assert next(signal_row) == {'time': '9.841098354638689e-002',
                                'prs_rag': '-0.13671875', 'prs_rag_sent': '-0.1337890625'}
    assert next(signal_row) == {'time': '0.1085597930283484',
                                'prs_rag': '-0.140625', 'prs_rag_sent': '-0.1474609375'}


def test_signal_row_generator_with_time_and_two_signal_2(processed_ascii):
    signal_row = signal_row_generator(source=processed_ascii, signal1=sig_in_2nd, signal2=sig_in_4th)

    assert next(signal_row) == {'time': '9.841098354638689e-002',
                                'state_com_sens_sent[UREA_PRS]': '8.0', 't_dly_diag_inh_sens_sent': '24.43'}
    assert next(signal_row) == {'time': '0.1085597930283484',
                                'state_com_sens_sent[UREA_PRS]': '8.0', 't_dly_diag_inh_sens_sent': '24.44'}


def test_signal_frame_generator_with_time_and_one_signal_1(processed_ascii):
    signal_frames = signal_frame_generator(source=processed_ascii, signal1=sig_in_1st)

    assert next(signal_frames) == (38441, [0, 2, 4, 8, 0, 0, 0, 0])
    assert next(signal_frames) == (42406, [0, 2, 4, 8, 0, 0, 0, 0])
    assert next(signal_frames) == (46195, [0, 2, 4, 8, 0, 0, 0, 0])
    assert next(signal_frames) == (50482, [0, 2, 4, 8, 0, 0, 0, 0])
    assert next(signal_frames) == (54041, [0, 2, 4, 8, 0, 0, 0, 0])


def test_signal_frame_generator_with_time_and_one_signal_2(processed_ascii):
    signal_frames = signal_frame_generator(source=processed_ascii, signal1=sig_in_3rd)

    assert next(signal_frames) == (38441, [0, 13, 8, 1, 0, 0, 0, 0])
    assert next(signal_frames) == (42406, [0, 13, 7, 14, 0, 0, 0, 0])
    assert next(signal_frames) == (46195, [0, 13, 8, 2, 0, 0, 0, 0])
    assert next(signal_frames) == (50482, [0, 13, 7, 14, 0, 0, 0, 0])
    assert next(signal_frames) == (54041, [0, 13, 7, 14, 0, 0, 0, 0])
    assert next(signal_frames) == (58347, [0, 13, 7, 15, 0, 0, 0, 0])


def test_signal_frame_generator_with_time_and_two_signal_1(processed_ascii):
    signal_frames = signal_frame_generator(source=processed_ascii, signal1=sig_in_1st, signal2=sig_in_2nd)

    assert next(signal_frames) == (38441, [0, 2, 4, 8, 9, 8, 2, 0])
    assert next(signal_frames) == (42406, [0, 2, 4, 8, 9, 8, 2, 0])
    assert next(signal_frames) == (46195, [0, 2, 4, 8, 9, 4, 2, 0])
    assert next(signal_frames) == (50482, [0, 2, 4, 8, 9, 6, 2, 0])
    assert next(signal_frames) == (54041, [0, 2, 4, 8, 9, 6, 2, 0])
    assert next(signal_frames) == (58347, [0, 2, 4, 8, 9, 10, 2, 0])


def test_signal_frame_generator_with_time_and_two_signal_2(processed_ascii):
    signal_frames = signal_frame_generator(source=processed_ascii, signal1=sig_in_3rd, signal2=sig_in_4th)

    assert next(signal_frames) == (38441, [0, 13, 8, 1, 13, 0, 3, 0])
    assert next(signal_frames) == (42406, [0, 13, 7, 14, 13, 0, 3, 0])
    assert next(signal_frames) == (46195, [0, 13, 8, 2, 13, 0, 3, 0])
    assert next(signal_frames) == (50482, [0, 2, 4, 8, 9, 6, 2, 0])
    assert next(signal_frames) == (54041, [0, 2, 4, 8, 9, 6, 2, 0])
    assert next(signal_frames) == (58347, [0, 2, 4, 8, 9, 10, 2, 0])