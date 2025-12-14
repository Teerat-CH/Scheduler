from typing import List, Any
from process import Process
from scheduler.scheduler_base import Scheduler
from RBTree import RedBlackTree

class CFS(Scheduler):
    # latency_buffer = target_latency / 2
    def __init__(self, name="CFS", latency_buffer: float = 10, target_latency: float = 20, min_time_slice: float = 4):
        self.name = name
        self.latency_buffer = latency_buffer
        self.target_latency = target_latency
        self.min_time_slice = min_time_slice

    def schedule(self, processes: List[Process]):
        current_time = 0
        completed = set()
        ready_queue = RedBlackTree()
        incoming = sorted(processes, key=lambda p: p.arrival_time)
        min_vruntime = 0.0
        
        current_process = None
        time_slice_remaining = 0
        
        while len(completed) < len(processes):
            while incoming and incoming[0].arrival_time <= current_time:
                p = incoming.pop(0)
                
                if self.latency_buffer != -1:
                    if p.arrival_time > 0:
                        p.vruntime = max(0.0, min_vruntime - self.latency_buffer)
                    else:
                        p.vruntime = 0.0
                
                self.add_to_tree(ready_queue, p)
                

            if current_process is None or time_slice_remaining <= 0:
                if current_process and current_process.remaining_time > 0:
                    self.add_to_tree(ready_queue, current_process)
                    current_process = None

                if ready_queue.pids:
                    current_process = ready_queue.get_min()
                    ready_queue.remove(current_process.vruntime)
                    
                    num_runnable = len(ready_queue.pids) + 1 
                    
                    if num_runnable * self.min_time_slice > self.target_latency:
                        period = num_runnable * self.min_time_slice
                    else:
                        period = self.target_latency
                        
                    time_slice = period / num_runnable
                    
                    time_slice = max(time_slice, self.min_time_slice)
                    
                    time_slice_remaining = int(time_slice)
                else:
                    current_process = None

            if current_process:
                if current_process.start_time == -1:
                    current_process.start_time = current_time
                    current_process.response_time = current_time - current_process.arrival_time
                
                current_process.remaining_time -= 1
                time_slice_remaining -= 1
                
                current_process.vruntime += 1.0 / current_process.weight
                
                if current_process.remaining_time <= 0:
                    current_process.completion_time = current_time + 1
                    current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.duration
                    completed.add(current_process.pid)
                    current_process = None
                    time_slice_remaining = 0
                
                if ready_queue.pids:
                    min_vruntime = max(min_vruntime, ready_queue.get_min().vruntime)
                elif current_process:
                     min_vruntime = max(min_vruntime, current_process.vruntime)

            current_time += 1
            

    def add_to_tree(self, tree, process):
        # dbtree should expect deterministic, so add a small value
        while not tree.add(process):
            process.vruntime += 1e-5
