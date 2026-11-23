import debugger as mydbg


def foo(a, b):
    for i in range(3):
        a += i
        print(a)

    return a + b


if __name__ == '__main__':

    mydbg.set_trace()
    result = foo(1, 2)
    a = result + 3
    print(result)
