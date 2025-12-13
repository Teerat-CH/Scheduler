from process import Process

def get_test_case_1():
    return [
        Process("A", 0, 6, 1),
        Process("B", 0, 6, 1),
        Process("C", 0, 6, 1)
    ]

def get_test_case_2():
    return [
        Process("A", 0, 12, 1),
        Process("B", 0, 12, 2)
    ]

def get_test_case_3():
    return [
        Process("A", 0, 20, 1),
        Process("B", 10, 4, 1)
    ]

def get_test_case_4():
    return [
        Process("A", 0, 30, 1),
        Process("B", 0, 2, 1),
        Process("C", 0, 2, 1),
        Process("D", 0, 2, 1)
    ]

def get_test_case_5():
    return [
        Process("A", 0, 5, 1),
        Process("B", 20, 3, 1)
    ]
