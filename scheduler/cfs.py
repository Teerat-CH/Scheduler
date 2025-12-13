from typing import List, Any
from process import Process
from scheduler.scheduler_base import Scheduler
from RBTree import RedBlackTree

class CFS(Scheduler):
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
            # 1. Handle Arrivals
            while incoming and incoming[0].arrival_time <= current_time:
                p = incoming.pop(0)
                
                if self.latency_buffer != -1:
                    if p.arrival_time > 0:
                        p.vruntime = max(0.0, min_vruntime - self.latency_buffer)
                    else:
                        p.vruntime = 0.0
                
                self.add_to_tree(ready_queue, p)
                
                # Preemption check: if new process has lower vruntime than current,
                # we might want to switch. But for simplicity in this discrete sim,
                # we'll just add to tree and let the scheduler pick next time slice.

            # 2. Select Process
            if current_process is None or time_slice_remaining <= 0:
                # If we were running a process and it's not done, put it back
                if current_process and current_process.remaining_time > 0:
                    self.add_to_tree(ready_queue, current_process)
                    current_process = None

                if ready_queue.pids:
                    current_process = ready_queue.get_min()
                    ready_queue.remove(current_process.vruntime)
                    
                    # Calculate Time Slice
                    num_runnable = len(ready_queue.pids) + 1 # +1 for current_process
                    
                    # Target Latency Logic
                    if num_runnable * self.min_time_slice > self.target_latency:
                        # Too many processes, stretch the window
                        period = num_runnable * self.min_time_slice
                    else:
                        period = self.target_latency
                        
                    # Slice for this process (weighted)
                    # For simplicity assuming equal weights for now in slice calc, 
                    # or you can do: slice = period * (weight / total_weight)
                    # Using basic equal slice for now as per prompt description logic
                    time_slice = period / num_runnable
                    
                    # Enforce Minimum Granularity
                    time_slice = max(time_slice, self.min_time_slice)
                    
                    time_slice_remaining = int(time_slice) # Discrete simulation steps
                else:
                    current_process = None

            # 3. Run Process
            if current_process:
                # First run bookkeeping
                if current_process.start_time == -1:
                    current_process.start_time = current_time
                    current_process.response_time = current_time - current_process.arrival_time
                
                # Execute for 1 unit
                current_process.remaining_time -= 1
                time_slice_remaining -= 1
                
                # Update vruntime
                current_process.vruntime += 1.0 / current_process.weight
                
                # Check completion
                if current_process.remaining_time <= 0:
                    current_process.completion_time = current_time + 1
                    current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                    current_process.waiting_time = current_process.turnaround_time - current_process.duration
                    completed.add(current_process.pid)
                    current_process = None
                    time_slice_remaining = 0
                
                # Update min_vruntime
                if ready_queue.pids:
                    min_vruntime = max(min_vruntime, ready_queue.get_min().vruntime)
                elif current_process:
                     min_vruntime = max(min_vruntime, current_process.vruntime)

            current_time += 1
            

    def add_to_tree(self, tree, process):
        # dbtree should expect deterministic, so add a small value
        while not tree.add(process):
            process.vruntime += 1e-5
