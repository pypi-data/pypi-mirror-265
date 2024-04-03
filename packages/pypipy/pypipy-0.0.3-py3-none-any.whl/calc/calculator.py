def addAll(*args):
    return sum(args)


def mulAll(*args):
    result = 1
    for i in range(len(args)):
        result *= args[i]
    return result


def aMinusB(a, b):
    return a - b
