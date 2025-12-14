import copy
import csv
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
    get_test_case_6,
    get_test_case_7
)

def calculate_metrics(processes: List[Process]):
    total_turnaround = 0
    total_response = 0
    total_waiting = 0
    n = len(processes)
    
    if n == 0:
        return {"avg_turnaround": 0, "avg_response": 0, "avg_waiting": 0, "throughput": 0}

    max_completion_time = 0
    min_arrival_time = float('inf')

    for p in processes:
        total_turnaround += p.turnaround_time
        total_response += p.response_time
        total_waiting += p.waiting_time
        max_completion_time = max(max_completion_time, p.completion_time)
        min_arrival_time = min(min_arrival_time, p.arrival_time)

    total_time = max_completion_time - min_arrival_time
    # 1000 since time in milliseconds
    throughput = 1000 * n / total_time if total_time > 0 else 0

    return {
        "avg_turnaround": total_turnaround / n,
        "avg_response": total_response / n,
        "avg_waiting": total_waiting / n,
        "throughput": throughput
    }

def run_test_case(name: str, processes: List[Process], schedulers: List[Scheduler]):
    print(f"\n=== {name} ===")
    
    results = []
    for scheduler in schedulers:
        # deep copy processes
        test_processes = [copy.deepcopy(p) for p in processes]
        scheduler_name = scheduler.name if hasattr(scheduler, 'name') else scheduler.__class__.__name__
        
        scheduler.schedule(test_processes)
        metrics = calculate_metrics(test_processes)
        results.append({
            "Scheduler": scheduler_name,
            "Avg Turnaround": metrics['avg_turnaround'],
            "Avg Response": metrics['avg_response'],
            "Avg Waiting": metrics['avg_waiting'],
            "Throughput": metrics['throughput']
        })

    headers = ["Scheduler", "Avg Turnaround", "Avg Response", "Avg Waiting", "Throughput"]
    col_widths = [20, 18, 18, 18, 15]
    
    header_row = "".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
    print("-" * len(header_row))
    print(header_row)
    print("-" * len(header_row))
    
    for row in results:
        print(f"{row['Scheduler']:<{col_widths[0]}}"
              f"{row['Avg Turnaround']:<{col_widths[1]}.0f}"
              f"{row['Avg Response']:<{col_widths[2]}.2f}"
              f"{row['Avg Waiting']:<{col_widths[3]}.1f}"
              f"{row['Throughput']:<{col_widths[4]}.2f}")
    print("-" * len(header_row))    
    return results
if __name__ == "__main__":
    schedulers = [
        FCFS(),
        SJF(),
        PriorityScheduler(),
        RoundRobin(time_slice=10),
        CFS("CFS", latency_buffer=10),
        CFS("CFS_NoBuffer", latency_buffer=-1)
    ]

    all_results = []

    def run_and_store(name, processes):
        results = run_test_case(name, processes, schedulers)
        for r in results:
            r['Test Case'] = name
            all_results.append(r)

    run_and_store("Test Case 1: Equal Weight Processes", get_test_case_1())
    run_and_store("Test Case 2: Different Weights", get_test_case_2())
    run_and_store("Test Case 3: Late Arrival Preemption", get_test_case_3())
    run_and_store("Test Case 4: Many Short Jobs + One Long Job", get_test_case_4())
    run_and_store("Test Case 5: CPU Idle Period + New Arrival", get_test_case_5())
    run_and_store("Test Case 6: Sleeper Fairness / Gaming the Scheduler", get_test_case_6())
    run_and_store("Test Case 7: Many Equal Processes", get_test_case_7())

    # csv export
    if all_results:
        fieldnames = ["Test Case", "Scheduler", "Avg Turnaround", "Avg Response", "Avg Waiting", "Throughput"]
        with open('scheduler_results.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_results)
        print(f"\nResults exported to scheduler_results.csv")
