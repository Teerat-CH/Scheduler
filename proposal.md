Here is the content of the PDF converted into Markdown format.

# CS377 Group Project Proposal
**Tung V. Le, Minh T. Nguyen, Teerat Chanromyen**

### What is the algorithm that your team plans to implement?
We plan to implement a Completely Fair Scheduler (CFS) as it is very effective and is one of the most popular algorithms used today (default for linux kernel since 2007).

### What is the baseline algorithm that your time will compare with?
We will compare our implementation with FCFS, SJF, Priority scheduling, and Round Robin.

### What are the metrics that your team will use to compare the algorithms?
We plan to compare scheduling algorithms using Average Response Time, Average Turnaround Time, and Throughput as our primary evaluation metrics. To assess performance across different workload sizes, we will run simulations over a range of job counts (e.g., 10, 50, 100, 500 jobs) and plot the results to visualize how each algorithm scales under increasing load.

### Lastly, think about 5 cases your team will provide to show that the algorithm is implemented correctly?

#### Test Case 1: Equal Weight Processes (baseline fairness)
*   **Input:** All processes same arrival + same weights
    *   A: arrival=0, duration=6, weight=1
    *   B: arrival=0, duration=6, weight=1
    *   C: arrival=0, duration=6, weight=1
*   **Expected:** Each process gets ~1/3 of the CPU fairly.
    *   Process A total CPU time: 6
    *   Process B total CPU time: 6
    *   Process C total CPU time: 6

#### Test Case 2: Different Weights (weighted fairness)
*   **Input:** Processes with different priorities (weights)
    *   A: arrival=0, duration=12, weight=1
    *   B: arrival=0, duration=12, weight=2
*   **Expected:** B should get twice as much CPU time as A (because weight=2 -> higher priority).
    *   CPU(B) ≈ 2 × CPU(A)
    *   Process A total CPU time ≈ 8
    *   Process B total CPU time ≈ 16
    *   This allow runtime(A) ≈ runtime(B)

#### Test Case 3: Late Arrival Preemption (runtime jump test)
*   **Input:** A long-running task, and a short task arriving late.
    *   A: arrival=0, duration=20, weight=1
    *   B: arrival=10, duration=4, weight=1
*   **Expected:**
    *   When B arrives at t=10, its runtime = 0
    *   A already has runtime ≈ 10
    *   So B should run immediately, preempting A
    *   After B finishes (~t=14), A resumes
    *   Runtime:
        *   Process A total CPU time: 20
        *   Process B total CPU time: 4
    *   Schedule:
        *   A runs from t=0 to t=10
        *   B preempts and runs from t=10 to t=14
        *   A runs again from t=14 to t=24

#### Test Case 4: Many Short Jobs + One Long Job (no starvation)
*   **Input:** One long job, several short ones.
    *   A: arrival=0, duration=30, weight=1
    *   B: arrival=0, duration=2, weight=1
    *   C: arrival=0, duration=2, weight=1
    *   D: arrival=0, duration=2, weight=1
*   **Expected:**
    *   Short jobs should finish first, but **A must be interleaved between them**
    *   CFS prevents A from starving
    *   CPU alternates between the shortest runtime processes
    *   Runtime:
        *   Process A total CPU time: 30
        *   Process B total CPU time: 2
        *   Process C total CPU time: 2
        *   Process D total CPU time: 2
    *   t=0 → all runtime = 0 → any process may start, usually A
*   **Schedule behaviour:**
    *   Short jobs quickly raise their runtime and finish
    *   A fills in the gaps **every time its runtime becomes smallest**

#### Test Case 5: CPU Idle Period + New Arrival
*   **Input:** Job arrives long after CPU has been idle
    *   A: arrival=0, duration=5, weight=1
    *   B: arrival=20, duration=3, weight=1
*   **Expected:**
    *   A finishes at t=5
    *   CPU idle from t=5 to t=20
    *   At t=20, B arrives and runs instantly with runtime=0
    *   No leftover state incorrectly affects B
    *   Runtime:
        *   Process A total CPU time: 5
        *   Process B total CPU time: 3
    *   Schedule:
        *   No scheduling activity between t=5–20
        *   B is scheduled immediately and completes normally