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
    get_test_case_5,
    get_test_case_6
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

def run_test_case(name: str, processes: List[Process], schedulers: List[Scheduler]):
    print(f"\n=== {name} ===")
    
    results = []
    for scheduler in schedulers:
        # Deep copy processes to ensure fresh state for each scheduler
        test_processes = [copy.deepcopy(p) for p in processes]
        scheduler_name = scheduler.name if hasattr(scheduler, 'name') else scheduler.__class__.__name__
        
        scheduler.schedule(test_processes)
        metrics = calculate_metrics(test_processes)
        results.append({
            "Scheduler": scheduler_name,
            "Avg Turnaround": metrics['avg_turnaround'],
            "Avg Response": metrics['avg_response'],
            "Throughput": metrics['throughput']
        })

    # Print Table
    headers = ["Scheduler", "Avg Turnaround", "Avg Response", "Throughput"]
    # Define column widths
    col_widths = [20, 18, 18, 15]
    
    # Print Header
    header_row = "".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
    print("-" * len(header_row))
    print(header_row)
    print("-" * len(header_row))
    
    # Print Rows
    for row in results:
        print(f"{row['Scheduler']:<{col_widths[0]}}"
              f"{row['Avg Turnaround']:<{col_widths[1]}.2f}"
              f"{row['Avg Response']:<{col_widths[2]}.2f}"
              f"{row['Throughput']:<{col_widths[3]}.2f}")
    print("-" * len(header_row))

if __name__ == "__main__":
    schedulers = [
        FCFS(),
        SJF(),
        PriorityScheduler(),
        RoundRobin(time_quantum=2),
        CFS("CFS", latency_buffer=6.0),
        CFS("CFS_NoBuffer", latency_buffer=-1)
    ]

    run_test_case("Test Case 1: Equal Weight Processes", get_test_case_1(), schedulers)
    run_test_case("Test Case 2: Different Weights", get_test_case_2(), schedulers)
    run_test_case("Test Case 3: Late Arrival Preemption", get_test_case_3(), schedulers)
    run_test_case("Test Case 4: Many Short Jobs + One Long Job", get_test_case_4(), schedulers)
    run_test_case("Test Case 5: CPU Idle Period + New Arrival", get_test_case_5(), schedulers)
    run_test_case("Test Case 6: Sleeper Fairness / Gaming the Scheduler", get_test_case_6(), schedulers)
