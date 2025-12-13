import unittest
from process import Process
from scheduler.round_robin import RoundRobin

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestRoundRobin(unittest.TestCase):

    def test_basic(self):
        # arrive at the same time should go in order A, B, C
        processes = [
            Process("A", 0, 4),
            Process("B", 0, 4),
            Process("C", 0, 4)
        ]

        rr = RoundRobin(time_slice=2)
        rr.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 8)
        self.assertEqual(processes[1].completion_time, 10)
        self.assertEqual(processes[2].completion_time, 12)
        self.assertEqual(processes[0].turnaround_time, 8)
        self.assertEqual(processes[1].turnaround_time, 10)
        self.assertEqual(processes[2].turnaround_time, 12)
        self.assertEqual(processes[0].response_time, 0)
        self.assertEqual(processes[1].response_time, 2)
        self.assertEqual(processes[2].response_time, 4)

    def test_arrival_times(self):
        processes = [
            Process("A", 0, 5),
            Process("B", 1, 3)
        ]
        rr = RoundRobin(time_slice=2)
        rr.schedule(processes)
        
        self.assertEqual(processes[1].completion_time, 7, "Process B should finish at 7")
        self.assertEqual(processes[0].completion_time, 8, "Process A should finish at 8")
        self.assertEqual(processes[1].turnaround_time, 6)
        self.assertEqual(processes[0].turnaround_time, 8)
        self.assertEqual(processes[1].response_time, 1)
        self.assertEqual(processes[0].response_time, 0)

    def test_large_time_slice(self):
        processes = [
            Process("A", 0, 4),
            Process("B", 2, 2)
        ]
        rr = RoundRobin(time_slice=10)
        rr.schedule(processes)

        self.assertEqual(processes[0].completion_time, 4)
        self.assertEqual(processes[1].completion_time, 6)

    def test_different_burst_times(self):
        processes = [
            Process("A", 0, 5),
            Process("B", 0, 2),
            Process("C", 0, 8),
            Process("D", 0, 1)
        ]
        rr = RoundRobin(time_slice=3)
        rr.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 11)
        self.assertEqual(processes[1].completion_time, 5)
        self.assertEqual(processes[2].completion_time, 16)
        self.assertEqual(processes[3].completion_time, 9)

    def test_time_slice_equals_burst_time(self):
        processes = [
            Process("P1", 0, 5),
            Process("P2", 0, 2),
            Process("P3", 0, 3)
        ]
        rr = RoundRobin(time_slice=2)
        rr.schedule(processes)

        self.assertEqual(processes[0].completion_time, 10)
        self.assertEqual(processes[1].completion_time, 4)
        self.assertEqual(processes[2].completion_time, 9)
        self.assertEqual(processes[1].turnaround_time, 4)
        self.assertEqual(processes[1].response_time, 2)

    def test_single_unit_time_slice(self):
        processes = [
            Process("X", 0, 3),
            Process("Y", 0, 2),
            Process("Z", 0, 4)
        ]
        rr = RoundRobin(time_slice=1)
        rr.schedule(processes)
        
        # X, Y, Z, X, Y, Z, X, Z
        self.assertEqual(processes[0].completion_time, 7)
        self.assertEqual(processes[1].completion_time, 5)
        self.assertEqual(processes[2].completion_time, 9)
        self.assertEqual(processes[0].response_time, 0)
        self.assertEqual(processes[1].response_time, 1)
        self.assertEqual(processes[2].response_time, 2)

    def test_process_arrival_during_execution(self):
        processes = [
            Process("P1", 0, 8),
            Process("P2", 3, 2),
            Process("P3", 5, 4),
            Process("P4", 7, 1)
        ]
        rr = RoundRobin(time_slice=3)
        rr.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 14)
        self.assertEqual(processes[1].completion_time, 5) 
        self.assertEqual(processes[2].completion_time, 15)
        self.assertEqual(processes[3].completion_time, 12)

    def test_late_arrival_process(self):
        processes = [
            Process("A", 0, 4),
            Process("B", 0, 2),
            Process("C", 10, 3)
        ]
        rr = RoundRobin(time_slice=3)
        rr.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 6)
        self.assertEqual(processes[1].completion_time, 5)
        self.assertEqual(processes[2].completion_time, 13)

    def test_zero_burst_time_edge_case(self):
        processes = [
            Process("P1", 0, 5),
            Process("P2", 0, 0),
            Process("P3", 0, 3)
        ]
        rr = RoundRobin(time_slice=2)
        rr.schedule(processes)
        
        self.assertEqual(processes[1].completion_time, 2)
        self.assertEqual(processes[0].completion_time, 8)
        self.assertEqual(processes[2].completion_time, 7)
        
        self.assertEqual(processes[1].turnaround_time, 2)
        self.assertEqual(processes[1].response_time, 2)

if __name__ == '__main__':
    unittest.main()