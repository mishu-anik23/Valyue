def signal_generator(min, step, max=None):
    result = type(min + step)(min)
    forever = max is None
    index = 0
    while forever or result < max:
        yield result
        index += 1
        result = min + step * index
    #print(result)


import pytest


def test_string_manipulator_1():
    f = make_reverser()
    assert f('Hello') == 'olleH'


def test_string_manipulator_2():
    f = make_upper_reverser()
    assert f('Hello') == 'OLLEH'


def make_reverser():
    def func(str_in):
        return ''.join(reversed(str_in))
    return func


def make_upper_reverser():
    def func_upper(str_in):
        return str_in.upper()
    def func_reverse(str_in):
        return ''.join(reversed(str_in))
    return lambda str_in: func_reverse(func_upper(str_in))


def compose(f2, f1):
    """
    if  f1: 2 -> 3   [lambda x: x+1]
    and f2: 3 -> 0.3333...  [lambda x: 1/x]
    then compose(f2, f1): 2 -> 0.3333...
    """
    return lambda x: f2(f1(x))


if __name__ == '__main__':
    print(list(signal_generator(-10, 0.5, 1)))
    sg = signal_generator(-1, 3, 89)
    print(next(sg))
    #print(list(sg))



