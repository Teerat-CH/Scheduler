from process import Process

def get_test_case_1():
    return [
        Process("A", 0, 6000, 1),
        Process("B", 0, 6000, 1),
        Process("C", 0, 6000, 1)
    ]

def get_test_case_2():
    # Right now this test case don't really show the difference between priority scheduling because no matter out your prioritize,
    # the turn around and response time will be the same since we have same duration for all processes.
    return [
        Process("A", 0, 12000, 1),
        Process("B", 0, 36000, 2)
    ]

def get_test_case_3():
    return [
        Process("A", 0, 20000, 1),
        Process("B", 10000, 4000, 1)
    ]

def get_test_case_4():
    return [
        Process("A", 0, 30000, 1),
        Process("B", 0, 2000, 1),
        Process("C", 0, 2000, 1),
        Process("D", 0, 2000, 1)
    ]

def get_test_case_5():
    return [
        Process("A", 0, 5000, 1),
        Process("B", 20000, 3000, 1)
    ]

def get_test_case_6():
    # Sleeper Fairness / Gaming the Scheduler
    # Process A runs for a while. Process B arrives late (simulating waking up).
    # If B's vruntime starts at 0, it will monopolize the CPU until it catches up to A.
    # Expected behavior with sleeper fairness: B should not monopolize the CPU; they should share it.
    return [
        Process("A", 0, 50000, 1),
        Process("B", 49000, 50000, 1),
        Process("C", 49000, 30000, 1),
    ]
