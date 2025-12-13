import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from process import Process
from scheduler.fcfs import FCFS

class TestFCFS(unittest.TestCase):

    def test_basic(self):
        # arrive at the same time should go in order A, B, C
        processes = [
            Process("A", 0, 4),
            Process("B", 0, 4),
            Process("C", 0, 4)
        ]

        fcfs = FCFS()
        fcfs.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 4)
        self.assertEqual(processes[1].completion_time, 8)
        self.assertEqual(processes[2].completion_time, 12)
        self.assertEqual(processes[0].turnaround_time, 4)
        self.assertEqual(processes[1].turnaround_time, 8)
        self.assertEqual(processes[2].turnaround_time, 12)
        self.assertEqual(processes[0].response_time, 0)
        self.assertEqual(processes[1].response_time, 4)
        self.assertEqual(processes[2].response_time, 8)

    def test_arrival_times(self):
        processes = [
            Process("A", 0, 5),
            Process("B", 1, 3)
        ]
        fcfs = FCFS()
        fcfs.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 5, "Process A should finish at 5")
        self.assertEqual(processes[1].completion_time, 8, "Process B should finish at 8")
        self.assertEqual(processes[0].turnaround_time, 5)
        self.assertEqual(processes[1].turnaround_time, 7)
        self.assertEqual(processes[0].response_time, 0)
        self.assertEqual(processes[1].response_time, 4)

    def test_different_burst_times(self):
        processes = [
            Process("A", 0, 5),
            Process("B", 0, 2),
            Process("C", 0, 8),
            Process("D", 0, 1)
        ]
        fcfs = FCFS()
        fcfs.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 5)
        self.assertEqual(processes[1].completion_time, 7)
        self.assertEqual(processes[2].completion_time, 15)
        self.assertEqual(processes[3].completion_time, 16)

    def test_process_arrival_during_execution(self):
        processes = [
            Process("P1", 0, 8),
            Process("P2", 3, 2),
            Process("P3", 5, 4),
            Process("P4", 7, 1)
        ]
        fcfs = FCFS()
        fcfs.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 8)
        self.assertEqual(processes[1].completion_time, 10)
        self.assertEqual(processes[2].completion_time, 14)
        self.assertEqual(processes[3].completion_time, 15)

    def test_late_arrival_process(self):
        processes = [
            Process("A", 0, 4),
            Process("B", 0, 2),
            Process("C", 10, 3)
        ]
        fcfs = FCFS()
        fcfs.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 4)
        self.assertEqual(processes[1].completion_time, 6)
        self.assertEqual(processes[2].completion_time, 13)

    def test_cpu_idle_period(self):
        # CPU should idle and jump to next arrival
        processes = [
            Process("A", 0, 3),
            Process("B", 10, 4)
        ]
        fcfs = FCFS()
        fcfs.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 3)
        self.assertEqual(processes[1].completion_time, 14)
        self.assertEqual(processes[1].response_time, 0)
        self.assertEqual(processes[1].waiting_time, 0)

    def test_convoy_effect(self):
        # Long process arriving first causes convoy effect
        processes = [
            Process("Long", 0, 10),
            Process("Short1", 1, 1),
            Process("Short2", 2, 1)
        ]
        fcfs = FCFS()
        fcfs.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 10)
        self.assertEqual(processes[1].completion_time, 11)
        self.assertEqual(processes[2].completion_time, 12)
        self.assertEqual(processes[1].response_time, 9)
        self.assertEqual(processes[2].response_time, 9)

    def test_zero_burst_time_edge_case(self):
        processes = [
            Process("P1", 0, 5),
            Process("P2", 0, 0),
            Process("P3", 0, 3)
        ]
        fcfs = FCFS()
        fcfs.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 5)
        self.assertEqual(processes[1].completion_time, 5)
        self.assertEqual(processes[2].completion_time, 8)
        self.assertEqual(processes[1].turnaround_time, 5)
        self.assertEqual(processes[1].response_time, 5)

    def test_single_process(self):
        processes = [
            Process("Single", 5, 10)
        ]
        fcfs = FCFS()
        fcfs.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 15)
        self.assertEqual(processes[0].turnaround_time, 10)
        self.assertEqual(processes[0].response_time, 0)
        self.assertEqual(processes[0].waiting_time, 0)

if __name__ == '__main__':
    unittest.main()
