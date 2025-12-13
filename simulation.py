import copy
from typing import List, Dict, Any
from process import Process
from scheduler.scheduler_base import Scheduler
from scheduler.fcfs import FCFS
from scheduler.sjf import SJF
from scheduler.priority_scheduler import PriorityScheduler
from scheduler.round_robin import RoundRobin
from scheduler.cfs import CFS
from test_cases import (
    get_test_case_1,
    get_test_case_2,
    get_test_case_3,
    get_test_case_4,
    get_test_case_5
)

def calculate_metrics(processes: List[Process]):
    total_turnaround = 0
    total_response = 0
    n = len(processes)
    
    if n == 0:
        return {"avg_turnaround": 0, "avg_response": 0, "throughput": 0}

    max_completion_time = 0
    min_arrival_time = float('inf')

    for p in processes:
        total_turnaround += p.turnaround_time
        total_response += p.response_time
        max_completion_time = max(max_completion_time, p.completion_time)
        min_arrival_time = min(min_arrival_time, p.arrival_time)

    total_time = max_completion_time - min_arrival_time
    throughput = n / total_time if total_time > 0 else 0

    return {
        "avg_turnaround": total_turnaround / n,
        "avg_response": total_response / n,
        "throughput": throughput
    }

def print_metrics(name: str, processes: List[Process]):
    metrics = calculate_metrics(processes)
    print(f"--- {name} Results ---")
    print(f"Average Turnaround Time: {metrics['avg_turnaround']:.2f}")
    print(f"Average Response Time: {metrics['avg_response']:.2f}")
    print(f"Throughput: {metrics['throughput']:.2f} processes/unit time")
    print("-" * 30)

def run_test_case(name: str, processes: List[Process], schedulers: List[Scheduler]):
    for scheduler in schedulers:
        test_processes = [copy.deepcopy(p) for p in processes]
        scheduler_name = scheduler.__class__.__name__
        print(f"Running {scheduler_name}...")
        scheduler.schedule(test_processes)
        print_metrics(scheduler_name, test_processes)
    print("\n")

if __name__ == "__main__":
    schedulers = [
        FCFS(),
        SJF(),
        PriorityScheduler(),
        RoundRobin(time_quantum=2),
        CFS()
    ]

    run_test_case("Test Case 1: Equal Weight Processes", get_test_case_1(), schedulers)
    run_test_case("Test Case 2: Different Weights", get_test_case_2(), schedulers)
    run_test_case("Test Case 3: Late Arrival Preemption", get_test_case_3(), schedulers)
    run_test_case("Test Case 4: Many Short Jobs + One Long Job", get_test_case_4(), schedulers)
    run_test_case("Test Case 5: CPU Idle Period + New Arrival", get_test_case_5(), schedulers)
