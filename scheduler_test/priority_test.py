import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from process import Process
from scheduler.priority_scheduler import PriorityScheduler

class TestPriorityScheduler(unittest.TestCase):

    def test_basic_equal_priority(self):
        # Same priority should follow FCFS order
        processes = [
            Process("A", 0, 4, weight=1),
            Process("B", 0, 4, weight=1),
            Process("C", 0, 4, weight=1)
        ]

        ps = PriorityScheduler()
        ps.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 4)
        self.assertEqual(processes[1].completion_time, 8)
        self.assertEqual(processes[2].completion_time, 12)
        self.assertEqual(processes[0].response_time, 0)
        self.assertEqual(processes[1].response_time, 4)
        self.assertEqual(processes[2].response_time, 8)

    def test_different_priorities(self):
        # Higher weight should execute first
        processes = [
            Process("Low", 0, 4, weight=1),
            Process("High", 0, 4, weight=3),
            Process("Medium", 0, 4, weight=2)
        ]
        ps = PriorityScheduler()
        ps.schedule(processes)
        
        self.assertEqual(processes[1].completion_time, 4, "High priority should finish first")
        self.assertEqual(processes[2].completion_time, 8, "Medium priority should finish second")
        self.assertEqual(processes[0].completion_time, 12, "Low priority should finish last")
        self.assertEqual(processes[1].response_time, 0)
        self.assertEqual(processes[2].response_time, 4)
        self.assertEqual(processes[0].response_time, 8)

    def test_priority_with_arrival_times(self):
        processes = [
            Process("A", 0, 5, weight=1),
            Process("B", 1, 3, weight=3),
            Process("C", 2, 2, weight=2)
        ]
        ps = PriorityScheduler()
        ps.schedule(processes)
        
        # A starts first, then B arrives with higher priority but non-preemptive
        self.assertEqual(processes[0].completion_time, 5)
        self.assertEqual(processes[1].completion_time, 8)
        self.assertEqual(processes[2].completion_time, 10)

    def test_priority_starvation(self):
        # Low priority process waits for all high priority processes
        processes = [
            Process("High1", 0, 2, weight=5),
            Process("High2", 0, 2, weight=5),
            Process("Low", 0, 2, weight=1),
            Process("High3", 0, 2, weight=5)
        ]
        ps = PriorityScheduler()
        ps.schedule(processes)
        
        self.assertEqual(processes[2].completion_time, 8, "Low priority should finish last")
        self.assertEqual(processes[2].response_time, 6, "Low priority waits for all high priority")

    def test_late_high_priority_arrival(self):
        # High priority arrives late, runs after current process completes
        processes = [
            Process("Low", 0, 10, weight=1),
            Process("High", 5, 2, weight=5)
        ]
        ps = PriorityScheduler()
        ps.schedule(processes)
        
        # Nonpreemptive: Low finishes first
        self.assertEqual(processes[0].completion_time, 10)
        self.assertEqual(processes[1].completion_time, 12)

    def test_same_priority_different_arrival(self):
        # Same priority, earlier arrival first
        processes = [
            Process("B", 2, 3, weight=2),
            Process("A", 1, 3, weight=2),
            Process("C", 0, 3, weight=2)
        ]
        ps = PriorityScheduler()
        ps.schedule(processes)
        
        self.assertEqual(processes[2].completion_time, 3, "C arrives first")
        self.assertEqual(processes[1].completion_time, 6, "A arrives second")
        self.assertEqual(processes[0].completion_time, 9, "B arrives third")

    def test_mixed_priorities_and_bursts(self):
        processes = [
            Process("P1", 0, 8, weight=1),
            Process("P2", 1, 4, weight=3),
            Process("P3", 2, 2, weight=2),
            Process("P4", 3, 1, weight=4)
        ]
        ps = PriorityScheduler()
        ps.schedule(processes)
        
        # P1 starts, then after it completes, others run by priority
        self.assertEqual(processes[0].completion_time, 8)
        self.assertEqual(processes[3].completion_time, 9, "P4 has highest priority")
        self.assertEqual(processes[1].completion_time, 13, "P2 has second highest")
        self.assertEqual(processes[2].completion_time, 15, "P3 has third highest")

    def test_zero_burst_high_priority(self):
        processes = [
            Process("P1", 0, 5, weight=1),
            Process("P2", 0, 0, weight=5),
            Process("P3", 0, 3, weight=2)
        ]
        ps = PriorityScheduler()
        ps.schedule(processes)
        
        self.assertEqual(processes[1].completion_time, 0)
        self.assertEqual(processes[2].completion_time, 3)
        self.assertEqual(processes[0].completion_time, 8)

    def test_single_high_priority_process(self):
        processes = [
            Process("Single", 5, 10, weight=10)
        ]
        ps = PriorityScheduler()
        ps.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 15)
        self.assertEqual(processes[0].turnaround_time, 10)
        self.assertEqual(processes[0].response_time, 0)

    def test_cpu_idle_then_priority(self):
        processes = [
            Process("A", 0, 3, weight=1),
            Process("B", 10, 2, weight=5),
            Process("C", 10, 3, weight=3)
        ]
        ps = PriorityScheduler()
        ps.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 3)
        self.assertEqual(processes[1].completion_time, 12, "High priority after idle")
        self.assertEqual(processes[2].completion_time, 15, "Lower priority last")

if __name__ == '__main__':
    unittest.main()
