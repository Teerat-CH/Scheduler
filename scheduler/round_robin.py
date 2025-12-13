from typing import List, Any
from process import Process
from scheduler.scheduler_base import Scheduler
from collections import deque

class RoundRobin(Scheduler):
    def __init__(self, time_quantum: int = 2):
        self.time_quantum = time_quantum

    def schedule(self, processes: List[Process]):
        current_time = 0
        completed_count = 0
        n = len(processes)
        
        ready_queue = deque() 
        
        sorted_processes = sorted(processes, key=lambda process: process.arrival_time)
        arrival_queue = deque(sorted_processes) 

        while completed_count < n:
            # move the processes that have arrived to the ready queue
            while arrival_queue and arrival_queue[0].arrival_time <= current_time:
                arriving_process = arrival_queue.popleft()
                ready_queue.append(arriving_process)

            if not ready_queue:
                # if no process is ready we can fast forward to the next arrival time
                if arrival_queue:
                    current_time = arrival_queue[0].arrival_time
                continue

            process = ready_queue.popleft()

            # if this is the first execution set response time and start time
            if process.response_time == -1:
                process.start_time = current_time
                process.response_time = current_time - process.arrival_time

            execution_time = min(self.time_quantum, process.remaining_time)
            
            current_time += execution_time
            process.remaining_time -= execution_time

            # add all the processes that have arrived during this execution
            while arrival_queue and arrival_queue[0].arrival_time <= current_time:
                arriving_process = arrival_queue.popleft()
                ready_queue.append(arriving_process)

            # add the process back to the ready queue or mark as completed
            if process.remaining_time > 0:
                ready_queue.append(process)
            else:
                process.completion_time = current_time

                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.duration
                
                completed_count += 1