from bintrees import RBTree
from process import Process
from typing import List

class RedBlackTree:
    def __init__(self):
        self.tree = RBTree()
        self.pids = set()
        self.vruntimes = set()

    # add a process to the tree, return True if added successfully, False otherwise
    def add(self, process: Process) -> bool:
        # we need this because bintrees.RBTree does not allow duplicate keys and it will override the existing one
        if process.pid in self.pids or process.vruntime in self.vruntimes:
            return False
        self.tree.insert(process.vruntime, process)
        self.pids.add(process.pid)
        self.vruntimes.add(process.vruntime)
        return True

    # return True if the process is removed successfully, False if not found
    # we assume that vruntime is unique
    def remove(self, vruntime: float) -> bool:
        process = self.tree.get(vruntime)
        if process is None:
            return False

        self.tree.remove(vruntime)
        self.pids.remove(process.pid)
        self.vruntimes.remove(vruntime)
        return True

    # return the process object that has the minimum vruntime
    def get_min(self) -> Process:
        return self.tree.min_item()[1]

    def find(self, vruntime: float) -> Process:
        return self.tree.get(vruntime)
    
    def get_all_vruntime(self) -> List[float]:
        return list(self.tree.keys())

if __name__ == "__main__":
    rbt = RedBlackTree()

    p1 = Process("process1", 0, 10, 1.0)
    p2 = Process("process2", 0, 15, 1.0)
    p3 = Process("process3", 0, 20, 1.0)

    p1.vruntime = 5
    p2.vruntime = 3
    p3.vruntime = 8

    rbt.add(p1)
    rbt.add(p2)
    rbt.add(p3)

    print(rbt.get_min()) # process2
    print(rbt.find(5)) # process1
    print(rbt.find(10)) # None
    print(rbt.remove(3)) # True
    print(rbt.remove(3)) # False
    print(rbt.get_min()) # process1
    print(rbt.get_all_vruntime()) # [5, 8]