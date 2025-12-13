class Process:
    def __init__(self, pid: str, arrival_time: int, duration: int, weight: int = 1):
        self.pid = pid
        self.arrival_time = arrival_time
        self.duration = duration
        self.remaining_time = duration
        self.weight = weight
        
        # Metrics
        self.start_time = -1
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1
        
        # CFS specific
        self.vruntime = 0.0

    def __repr__(self):
        return f"Process(pid={self.pid}, arrival={self.arrival_time}, duration={self.duration}, weight={self.weight})"

    def reset(self):
        self.remaining_time = self.duration
        self.start_time = -1
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1
        self.vruntime = 0.0