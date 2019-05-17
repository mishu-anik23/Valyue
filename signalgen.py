def signal_generator(min, step, max=None):
    result = type(min + step)(min)
    forever = max is None
    index = 0
    while forever or result < max:
        yield result
        index += 1
        result = min + step * index
    #print(result)

if __name__ == '__main__':
    print(list(signal_generator(-10, 0.5, 1)))
    sg = signal_generator(-10, 3, 89)
    print(next(sg))
    print(list(sg))
