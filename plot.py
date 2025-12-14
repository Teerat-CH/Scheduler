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
        return {"times": [], "counts": [], "max_time": 0}

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
    return {"times": times, "counts": counts, "max_time": max_time}

def pad_to_global_max(series_times, series_counts, global_max):
    if not series_times:
        return list(range(0, global_max + 1)), [0] * (global_max + 1)
    last_count = series_counts[-1] if series_counts else 0
    if series_times[-1] < global_max:
        # Extend to global max, holding the last count constant
        extra_times = list(range(series_times[-1] + 1, global_max + 1))
        series_times = series_times + extra_times
        series_counts = series_counts + [last_count] * len(extra_times)
    return series_times, series_counts

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

def average_metrics_over_sizes(sizes: List[int], schedulers):
    results = {
        "labels": [sched.name if hasattr(sched, "name") else sched.__class__.__name__ for sched in schedulers],
        "sizes": sizes,
        "avg_response": { },
        "avg_waiting": { },
        "avg_throughput": { },
    }

    for sched in schedulers:
        label = sched.name if hasattr(sched, "name") else sched.__class__.__name__
        results["avg_response"][label] = []
        results["avg_waiting"][label] = []
        results["avg_throughput"][label] = []

        for sz in sizes:
            procs = generate_random_processes(sz, seed=123 + sz)  # vary seed by size
            test_procs = [copy.deepcopy(p) for p in procs]
            sched_inst = sched  # reuse is fine if schedulers hold no state across runs
            sched_inst.schedule(test_procs)

            # averages
            avg_resp = sum(p.response_time for p in test_procs) / max(1, len(test_procs))
            avg_wait = sum(p.waiting_time for p in test_procs) / max(1, len(test_procs))

            # throughput: completed tasks per unit time (makespan)
            makespan = max((p.completion_time for p in test_procs), default=0)
            throughput = (len(test_procs) / makespan) if makespan > 0 else 0.0

            results["avg_response"][label].append(avg_resp)
            results["avg_waiting"][label].append(avg_wait)
            results["avg_throughput"][label].append(throughput)

    return results

def plot_metric_lines(results, metric_key, title, ylabel, colors):
    plt.figure(figsize=(10, 6))
    sizes = results["sizes"]
    for i, label in enumerate(results["labels"]):
        series = results[metric_key][label]
        plt.plot(sizes, series, marker="o", linewidth=2, color=colors[i % len(colors)], label=label)
    plt.title(title)
    plt.xlabel("Number of Tasks")
    plt.ylabel(ylabel)
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.legend()
    plt.tight_layout()

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

    series = []
    global_max = 0
    for sched in schedulers:
        data = cumulative_completion_over_time(processes, sched)
        series.append((sched, data["times"], data["counts"]))
        global_max = max(global_max, data["max_time"])

    plt.figure(figsize=(12, 7))
    for i, (sched, times, counts) in enumerate(series):
        times, counts = pad_to_global_max(times, counts, global_max)
        label = sched.name if hasattr(sched, "name") else sched.__class__.__name__
        plt.step(
            times,
            counts,
            where="post",
            label=label,
            color=colors[i % len(colors)],
            linewidth=2,
        )
    plt.title("Cumulative Tasks Completed Over Time (shared time scale)")
    plt.xlabel("Time (ms)")
    plt.ylabel("Completed Tasks")
    plt.ylim(0, n)
    plt.xlim(0, global_max)
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

    sizes = [10, 50, 100, 500, 1000]
    results = average_metrics_over_sizes(sizes, schedulers)

    plot_metric_lines(results, "avg_response", "Average Response Time vs Task Count", "Response Time (unit)", colors)
    plot_metric_lines(results, "avg_waiting", "Average Waiting Time vs Task Count", "Waiting Time (unit)", colors)
    plot_metric_lines(results, "avg_throughput", "Average Throughput vs Task Count", "Throughput (tasks/unit)", colors)

    plt.show()

if __name__ == "__main__":
    main()