from typing import List, Any
from process import Process
from scheduler.scheduler_base import Scheduler

class RoundRobin(Scheduler):
    def __init__(self, time_quantum: int = 2):
        self.time_quantum = time_quantum

    def schedule(self, processes: List[Process]):
        # TODO: Implement Round Robin scheduling
        pass
