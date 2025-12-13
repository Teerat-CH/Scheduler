from abc import ABC, abstractmethod
from typing import List, Any
from process import Process

class Scheduler(ABC):
    @abstractmethod
    def schedule(self, processes: List[Process]):
        """
        just signature for scheduler
        """
        pass
