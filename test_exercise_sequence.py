def test_sequence_generator_1():
    input = [1,2,3,0,5,6]
    assert generate_sequence(input) == [1*(2+3), 2*(3+0), 3*(0+5), (5+6)]