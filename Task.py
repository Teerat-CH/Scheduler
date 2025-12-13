class Task:
    def __init__(self, task_id: str, vruntime=0, work_unit=10, weight=1.0):
        self.name = task_id
        self.vruntime = vruntime
        self.work_units = work_unit
        self.weight = weight
    
    def __repr__(self):
        return f"Task(name={self.task_id}, vruntime={self.vruntime}, work_units={self.work_units}, weight={self.weight})"
    
    def run(self, time):
        actual = min(self.work_units, time)
        self.work_units -= actual
        self.vruntime += actual * self.weight
        return actual