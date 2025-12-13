from typing import List, Any
from process import Process
from scheduler.scheduler_base import Scheduler
from RBTree import RedBlackTree

class CFS_NoBuffer(Scheduler):
    def schedule(self, processes: List[Process]) -> List[Any]:
        current_time = 0
        completed = set()
        ready_queue = RedBlackTree()
        # Sort by arrival time
        incoming = sorted(processes, key=lambda p: p.arrival_time)
        min_vruntime = 0.0
        
        while len(completed) < len(processes):
            # 1. Handle Arrivals
            while incoming and incoming[0].arrival_time <= current_time:
                p = incoming.pop(0)
                
                # NO Sleeper Fairness / Latency Buffer:
                # We do NOT adjust vruntime based on min_vruntime.
                # The process keeps its initial vruntime (0.0) or whatever it had.
                # This allows late arrivals to potentially monopolize the CPU 
                # if min_vruntime is high.
                
                self.add_to_tree(ready_queue, p)

            # 2. Select and Run Process
            if ready_queue.pids:
                # Get task with lowest vruntime
                process = ready_queue.get_min()
                ready_queue.remove(process.vruntime)
                
                # First run bookkeeping
                if process.start_time == -1:
                    process.start_time = current_time
                    process.response_time = current_time - process.arrival_time
                
                # Execute for 1 unit
                process.remaining_time -= 1
                
                # Update vruntime
                # vruntime += delta_exec * (weight_0 / weight)
                # Assuming weight_0 = 1.0
                process.vruntime += 1.0 / process.weight
                
                # Check completion
                if process.remaining_time <= 0:
                    process.completion_time = current_time + 1
                    process.turnaround_time = process.completion_time - process.arrival_time
                    process.waiting_time = process.turnaround_time - process.duration
                    completed.add(process.pid)
                else:
                    # Re-insert into tree
                    self.add_to_tree(ready_queue, process)
                
                # Update min_vruntime
                if ready_queue.pids:
                    min_vruntime = max(min_vruntime, ready_queue.get_min().vruntime)

            else:
                # Idle
                pass
            
            current_time += 1
            
        return []

    def add_to_tree(self, tree, process):
        # Handle vruntime collisions by adding small epsilon
        while not tree.add(process):
            process.vruntime += 1e-5
