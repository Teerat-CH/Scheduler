from typing import List, Any
from process import Process
from scheduler.scheduler_base import Scheduler

class FCFS(Scheduler):
    def schedule(self, processes: List[Process]):
        """
        First-Come-First-Served (FCFS) scheduling algorithm.
        Non-preemptive: processes are executed in order of arrival time.
        """
        # Sort processes by arrival time (pid for tie-breaking)
        sorted_processes = sorted(processes, key=lambda p: (p.arrival_time, p.pid))
        
        execution_schedule = []
        current_time = 0
        
        for process in sorted_processes:
            # CPU is idle, jump to the next process arrival time
            if current_time < process.arrival_time:
                current_time = process.arrival_time
            
            # Set start time (first time process gets CPU)
            if process.start_time == -1:
                process.start_time = current_time
                process.response_time = current_time - process.arrival_time
            
            # Execute the entire process
            execution_schedule.append({
                'process': process.pid,
                'start_time': current_time,
                'duration': process.duration
            })
            
            # Update current time
            current_time += process.duration
            
            # Update process metrics
            process.completion_time = current_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.duration
            process.remaining_time = 0
        
        return execution_schedule
