from typing import List, Any
from process import Process
from scheduler.scheduler_base import Scheduler
from RBTree import RedBlackTree

class CFS(Scheduler):
    def __init__(self, name, latency_buffer: float = 6.0):
        self.name = name
        self.latency_buffer = latency_buffer

    def schedule(self, processes: List[Process]):
        current_time = 0
        completed = set()
        ready_queue = RedBlackTree()
        incoming = sorted(processes, key=lambda p: p.arrival_time)
        min_vruntime = 0.0
        
        while len(completed) < len(processes):
            while incoming and incoming[0].arrival_time <= current_time:
                p = incoming.pop(0)
                
                if self.latency_buffer != -1:
                    if p.arrival_time > 0:
                        p.vruntime = max(0.0, min_vruntime - self.latency_buffer)
                    else:
                        p.vruntime = 0.0
                
                self.add_to_tree(ready_queue, p)

            if ready_queue.pids:
                process = ready_queue.get_min()
                ready_queue.remove(process.vruntime)
                
                if process.start_time == -1:
                    process.start_time = current_time
                    process.response_time = current_time - process.arrival_time
                
                process.remaining_time -= 1
                
                process.vruntime += 1.0 / process.weight
                
                if process.remaining_time <= 0:
                    process.completion_time = current_time + 1
                    process.turnaround_time = process.completion_time - process.arrival_time
                    process.waiting_time = process.turnaround_time - process.duration
                    completed.add(process.pid)
                else:
                    self.add_to_tree(ready_queue, process)
                
                # update the new lowest vruntime
                if ready_queue.pids:
                    min_vruntime = max(min_vruntime, ready_queue.get_min().vruntime)

            current_time += 1
            

    def add_to_tree(self, tree, process):
        # dbtree should expect deterministic, so add a small value
        while not tree.add(process):
            process.vruntime += 1e-5
