import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from process import Process
from scheduler.sjf import SJF

class TestSJF(unittest.TestCase):

    def test_basic_equal_duration(self):
        # Equal duration should follow FCFS order
        processes = [
            Process("A", 0, 4),
            Process("B", 0, 4),
            Process("C", 0, 4)
        ]

        sjf = SJF()
        sjf.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 4)
        self.assertEqual(processes[1].completion_time, 8)
        self.assertEqual(processes[2].completion_time, 12)
        self.assertEqual(processes[0].response_time, 0)
        self.assertEqual(processes[1].response_time, 4)
        self.assertEqual(processes[2].response_time, 8)

    def test_different_durations(self):
        # Shortest job should execute first
        processes = [
            Process("Long", 0, 8),
            Process("Short", 0, 2),
            Process("Medium", 0, 5)
        ]
        sjf = SJF()
        sjf.schedule(processes)
        
        self.assertEqual(processes[1].completion_time, 2, "Shortest job should finish first")
        self.assertEqual(processes[2].completion_time, 7, "Medium job should finish second")
        self.assertEqual(processes[0].completion_time, 15, "Longest job should finish last")

    def test_arrival_times_shortest_job(self):
        processes = [
            Process("A", 0, 8),
            Process("B", 1, 2),
            Process("C", 2, 4)
        ]
        sjf = SJF()
        sjf.schedule(processes)
        
        # A starts first (only one available)
        # After A completes, B and C are ready, B is shortest
        self.assertEqual(processes[0].completion_time, 8)
        self.assertEqual(processes[1].completion_time, 10)
        self.assertEqual(processes[2].completion_time, 14)

    def test_optimal_average_waiting_time(self):
        # SJF minimizes average waiting time
        processes = [
            Process("P1", 0, 6),
            Process("P2", 0, 3),
            Process("P3", 0, 1),
            Process("P4", 0, 7)
        ]
        sjf = SJF()
        sjf.schedule(processes)
        
        self.assertEqual(processes[2].completion_time, 1, "Shortest first")
        self.assertEqual(processes[1].completion_time, 4, "Second shortest")
        self.assertEqual(processes[0].completion_time, 10, "Third shortest")
        self.assertEqual(processes[3].completion_time, 17, "Longest last")
        
        # Calculate average waiting time
        avg_waiting = (processes[0].waiting_time + processes[1].waiting_time + 
                      processes[2].waiting_time + processes[3].waiting_time) / 4
        self.assertLess(avg_waiting, 5.5, "SJF should have low average waiting time")

    def test_late_short_job_arrival(self):
        # Short job arrives late, non preemptive means current job continues
        processes = [
            Process("Long", 0, 10),
            Process("Short", 5, 2)
        ]
        sjf = SJF()
        sjf.schedule(processes)
        
        # Long starts at 0, completes at 10 (non preemptive)
        self.assertEqual(processes[0].completion_time, 10)
        self.assertEqual(processes[1].completion_time, 12)
        self.assertEqual(processes[1].response_time, 5)

    def test_multiple_short_jobs_arriving(self):
        processes = [
            Process("P1", 0, 8),
            Process("P2", 1, 1),
            Process("P3", 2, 2),
            Process("P4", 3, 3)
        ]
        sjf = SJF()
        sjf.schedule(processes)
        
        # P1 completes first (started before others arrived)
        # Then shortest of waiting: P2, P3, P4
        self.assertEqual(processes[0].completion_time, 8)
        self.assertEqual(processes[1].completion_time, 9, "Shortest waiting job")
        self.assertEqual(processes[2].completion_time, 11, "Second shortest")
        self.assertEqual(processes[3].completion_time, 14, "Third shortest")

    def test_starvation_scenario(self):
        # Long job may starve if short jobs keep arriving
        processes = [
            Process("VeryLong", 0, 10),
            Process("Short1", 0, 1),
            Process("Short2", 0, 1),
            Process("Short3", 0, 1)
        ]
        sjf = SJF()
        sjf.schedule(processes)
        
        # All short jobs execute before long job
        self.assertEqual(processes[1].completion_time, 1)
        self.assertEqual(processes[2].completion_time, 2)
        self.assertEqual(processes[3].completion_time, 3)
        self.assertEqual(processes[0].completion_time, 13, "Long job executes last")

    def test_zero_burst_time(self):
        processes = [
            Process("P1", 0, 5),
            Process("P2", 0, 0),
            Process("P3", 0, 3)
        ]
        sjf = SJF()
        sjf.schedule(processes)
        
        self.assertEqual(processes[1].completion_time, 0, "Zero duration completes immediately")
        self.assertEqual(processes[2].completion_time, 3, "Shorter job next")
        self.assertEqual(processes[0].completion_time, 8, "Longer job last")

    def test_cpu_idle_period(self):
        processes = [
            Process("A", 0, 3),
            Process("B", 10, 2),
            Process("C", 10, 5)
        ]
        sjf = SJF()
        sjf.schedule(processes)
        
        self.assertEqual(processes[0].completion_time, 3)
        self.assertEqual(processes[1].completion_time, 12, "Shorter job after idle")
        self.assertEqual(processes[2].completion_time, 17, "Longer job last")

    def test_tie_breaking_by_arrival(self):
        # Same duration, earlier arrival should go first
        processes = [
            Process("B", 2, 5),
            Process("A", 1, 5),
            Process("C", 0, 5)
        ]
        sjf = SJF()
        sjf.schedule(processes)
        
        self.assertEqual(processes[2].completion_time, 5, "C arrives first")
        self.assertEqual(processes[1].completion_time, 10, "A arrives second")
        self.assertEqual(processes[0].completion_time, 15, "B arrives third")

if __name__ == '__main__':
    unittest.main()
