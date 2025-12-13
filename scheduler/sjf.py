from typing import List, Any
from process import Process
from scheduler.scheduler_base import Scheduler

class SJF(Scheduler):
    def schedule(self, processes: List[Process]):
        """
        Shortest Job First (SJF) scheduling algorithm (non-preemptive).
        Selects the process with the shortest duration from the ready queue.
        """
        execution_schedule = []
        current_time = 0
        
        # processes sorted by arrival time
        workload = sorted(processes, key=lambda p: (p.arrival_time, p.pid))
        
        #  will hold processes ready to run
        ready_queue = []
        
        workload_index = 0
        n = len(workload)
        
        while workload_index < n or ready_queue:
            # Add all processes that have arrived by current_time to ready queue
            while workload_index < n and workload[workload_index].arrival_time <= current_time:
                ready_queue.append(workload[workload_index])
                workload_index += 1
            
            if ready_queue:
                # Sort by duration (shortest first), then by arrival time for tie breaking
                ready_queue.sort(key=lambda p: (p.duration, p.arrival_time))
                
                # Get shortest job
                process = ready_queue.pop(0)
                
                # Set first_run time
                if process.start_time == -1:
                    process.start_time = current_time
                    process.response_time = current_time - process.arrival_time
                
                # Execute the process completely (non-preemptive)
                execution_schedule.append({
                    'process': process.pid,
                    'start_time': current_time,
                    'duration': process.duration
                })
                
                current_time += process.duration
                
                # Update completion metrics
                process.completion_time = current_time
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.duration
                process.remaining_time = 0
                
            else:
                # CPU idle: jump to next process arrival
                if workload_index < n:
                    current_time = workload[workload_index].arrival_time
        
        return execution_schedule
