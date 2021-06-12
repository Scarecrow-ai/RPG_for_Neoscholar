def vector_subtraction(tuple1, tuple2):
    assert len(tuple1) == len(tuple2)
    res = ()
    for i in range(0, len(tuple1)):
        res += (tuple1[i] - tuple2[i],)
    return res


def vector_norm(tup):
    res = 0
    for num in tup:
        res += pow(num, 2)
    return pow(res, 0.5)


def vector_division(tup, divisor):
    assert divisor != 0
    res = ()
    for num in tup:
        res += (num / divisor,)
    return res
