from abc import ABC, abstractmethod
from typing import List, Any
from process import Process

class Scheduler(ABC):
    @abstractmethod
    def schedule(self, processes: List[Process]):
        """
        Simulates the scheduling algorithm.
        Should update the metrics in the processes and return the execution schedule.
        """
        pass
