def simulate_fcfs(processes):
    print("\n--- Running FCFS Scheduler ---")
    current_time = 0
    total_wait_time = 0
    total_turnaround_time = 0

    for pid, burst_time in processes:
        wait_time = current_time
        total_wait_time += wait_time

        turnaround_time = wait_time + burst_time
        total_turnaround_time += turnaround_time

        print(
            f"[Time {current_time:02d}] Process {pid} starts. "
            f"(Wait time: {wait_time})"
        )

        current_time += burst_time

        print(
            f"[Time {current_time:02d}] Process {pid} finishes. "
            f"(Turnaround time: {turnaround_time})"
        )

    avg_wait = total_wait_time / len(processes)
    avg_turnaround = total_turnaround_time / len(processes)

    print(f">> FCFS Average Waiting Time: {avg_wait:.2f}")
    print(f">> FCFS Average Turnaround Time: {avg_turnaround:.2f}")


def simulate_round_robin(processes, quantum):
    print(f"\n--- Running Round Robin Scheduler (Quantum = {quantum}) ---")

    remaining_burst = {pid: burst for pid, burst in processes}
    wait_times = {pid: 0 for pid, burst in processes}
    last_run_time = {pid: 0 for pid, burst in processes}
    finish_times = {}

    current_time = 0
    queue = [pid for pid, burst in processes]

    while queue:
        pid = queue.pop(0)
        wait_times[pid] += current_time - last_run_time[pid]

        time_to_run = min(quantum, remaining_burst[pid])
        print(
            f"[Time {current_time:02d}] Process {pid} "
            f"runs for {time_to_run} units."
        )

        current_time += time_to_run
        remaining_burst[pid] -= time_to_run
        last_run_time[pid] = current_time

        if remaining_burst[pid] > 0:
            queue.append(pid)
        else:
            finish_times[pid] = current_time
            print(f"[Time {current_time:02d}] Process {pid} finishes.")

    avg_wait = sum(wait_times.values()) / len(processes)

    # ทุก Process มาถึงเวลา 0 จึงใช้เวลาที่เสร็จเป็น Turnaround Time
    avg_turnaround = sum(finish_times.values()) / len(processes)

    print(f">> Round Robin Average Waiting Time: {avg_wait:.2f}")
    print(f">> Round Robin Average Turnaround Time: {avg_turnaround:.2f}")


def main():
    os_ready_queue = [
        ("P1", 10),
        ("P2", 2),
        ("P3", 3),
    ]

    simulate_fcfs(os_ready_queue)
    simulate_round_robin(os_ready_queue, quantum=3)


if __name__ == "__main__":
    main()