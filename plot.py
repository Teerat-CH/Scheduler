import random
import copy
import math
from typing import List, Dict
import matplotlib.pyplot as plt

from process import Process
from scheduler.fcfs import FCFS
from scheduler.sjf import SJF
from scheduler.priority_scheduler import PriorityScheduler
from scheduler.round_robin import RoundRobin
from scheduler.cfs import CFS

def generate_random_processes(n: int, seed: int = 42) -> List[Process]:
    random.seed(seed)
    processes = []
    for i in range(n):
        pid = f"P{i+1}"
        arrival = random.randint(0, 5000)
        duration = random.randint(10, 2000)
        weight = random.randint(1, 3)
        processes.append(Process(pid, arrival, duration, weight))
    return processes

def cumulative_completion_over_time(processes: List[Process], scheduler) -> Dict[str, List[int]]:
    test_processes = [copy.deepcopy(p) for p in processes]
    scheduler.schedule(test_processes)

    completion_times = sorted([p.completion_time for p in test_processes])
    if not completion_times:
        return {"times": [], "counts": []}

    max_time = completion_times[-1]
    times = list(range(0, max_time + 1))
    counts = []
    idx = 0
    completed = 0
    for t in times:
        while idx < len(completion_times) and completion_times[idx] <= t:
            completed += 1
            idx += 1
        counts.append(completed)
    return {"times": times, "counts": counts}

def collect_metrics(processes: List[Process], scheduler):
    test_processes = [copy.deepcopy(p) for p in processes]
    scheduler.schedule(test_processes)
    waiting = [p.waiting_time for p in test_processes]
    response = [p.response_time for p in test_processes]

    runs = []
    if isinstance(scheduler, RoundRobin):
        ts = getattr(scheduler, "time_slice", 1)
        runs = [math.ceil(max(0, p.duration) / max(1, ts)) for p in test_processes]
    elif isinstance(scheduler, (FCFS, SJF, PriorityScheduler)):
        runs = [1 for _ in test_processes]
    elif isinstance(scheduler, CFS):
        lb = getattr(scheduler, "latency_buffer", 1)
        runs = [max(1, math.ceil(max(0, p.duration) / max(1, lb))) for p in test_processes]
    else:
        runs = [1 for _ in test_processes]

    return waiting, response, runs

def main():
    n = 100
    processes = generate_random_processes(n, seed=123)

    schedulers = [
        FCFS(),
        SJF(),
        PriorityScheduler(),
        RoundRobin(time_slice=10),
        CFS("CFS", latency_buffer=10),
        CFS("CFS_NoBuffer", latency_buffer=-1)
    ]

    colors = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
    ]

    plt.figure(figsize=(12, 7))
    for i, sched in enumerate(schedulers):
        data = cumulative_completion_over_time(processes, sched)
        label = sched.name if hasattr(sched, "name") else sched.__class__.__name__
        plt.step(
            data["times"],
            data["counts"],
            where="post",
            label=label,
            color=colors[i % len(colors)],
            linewidth=2,
        )
    plt.title("Cumulative Tasks Completed Over Time (n=100, randomized)")
    plt.xlabel("Time (unit)")
    plt.ylabel("Completed Tasks")
    plt.ylim(0, n)
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.3)
    plt.tight_layout()

    labels = [sched.name if hasattr(sched, "name") else sched.__class__.__name__ for sched in schedulers]
    waiting_data = []
    response_data = []
    runs_data = []

    for sched in schedulers:
        waiting, response, runs = collect_metrics(processes, sched)
        waiting_data.append(waiting)
        response_data.append(response)
        runs_data.append(runs)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=False)

    def colorful_boxplot(ax, data, title, ylabel):
        bp = ax.boxplot(
            data,
            labels=labels,
            showfliers=False,
            patch_artist=True,
            medianprops=dict(color="#000000", linewidth=1.5),
            whiskerprops=dict(color="#555555"),
            capprops=dict(color="#555555"),
        )

        for i, box in enumerate(bp["boxes"]):
            box.set(facecolor=colors[i % len(colors)], alpha=0.5, edgecolor=colors[i % len(colors)])

        for i, whisk in enumerate(bp["whiskers"]):
            whisk.set(color=colors[(i // 2) % len(colors)])
        for i, cap in enumerate(bp["caps"]):
            cap.set(color=colors[(i // 2) % len(colors)])

        for med in bp["medians"]:
            med.set(color="#222222")
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.tick_params(axis='x', rotation=25)

    colorful_boxplot(axes[0], waiting_data, "Waiting Time per Scheduler", "Time (unit)")
    colorful_boxplot(axes[1], response_data, "Response Time per Scheduler", "Time (unit)")
    colorful_boxplot(axes[2], runs_data, "Times a Process Runs (approx.)", "Run count")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()