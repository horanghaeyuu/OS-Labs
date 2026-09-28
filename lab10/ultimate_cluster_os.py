import threading
import time
import os
import queue


class AIClusterOS:
    def __init__(self, total_ram_gb, num_gpus):
        # ทรัพยากรจำลอง
        self.total_ram_gb = total_ram_gb
        self.available_ram_gb = total_ram_gb
        self.ram_lock = threading.Lock()

        self.gpu_locks = {
            i: threading.Lock() for i in range(num_gpus)
        }
        self.gpu_status = {
            i: "IDLE" for i in range(num_gpus)
        }

        self.job_queue = queue.Queue()
        self.active_jobs = []
        self.is_running = True

        self.dash_thread = threading.Thread(
            target=self._dashboard_loop,
            daemon=True,
        )
        self.dash_thread.start()

        self.scheduler_thread = threading.Thread(
            target=self._os_scheduler_loop
        )
        self.scheduler_thread.start()

    def _dashboard_loop(self):
        while self.is_running:
            time.sleep(1.5)

            print("\n" + "=" * 50)
            print(
                f"[LIVE DASHBOARD] RAM Available: "
                f"{self.available_ram_gb}/{self.total_ram_gb} GB"
            )

            gpu_str = " | ".join(
                f"GPU {i}: {self.gpu_status[i]}"
                for i in self.gpu_locks
            )
            print(f"[LIVE DASHBOARD] {gpu_str}")
            print(
                f"[LIVE DASHBOARD] Queue Size: "
                f"{self.job_queue.qsize()} | "
                f"Active Jobs: {len(self.active_jobs)}"
            )
            print("=" * 50 + "\n")

    def submit_job(
        self, job_name, dataset_path, req_ram, req_gpus, duration
    ):
        self.job_queue.put(
            (job_name, dataset_path, req_ram, req_gpus, duration)
        )
        print(f"[API] Submitted: {job_name} -> Queued.")

    def _os_scheduler_loop(self):
        while self.is_running or not self.job_queue.empty():
            try:
                job_data = self.job_queue.get(timeout=1)
            except queue.Empty:
                continue

            worker = threading.Thread(
                target=self._execute_job,
                args=job_data,
            )
            worker.start()

    def _execute_job(
        self, job_name, dataset_path, req_ram, req_gpus, duration
    ):
        # 1. ตรวจว่าไฟล์มีอยู่
        if not os.path.exists(dataset_path):
            print(
                f"[{job_name}] FAILED: "
                f"Dataset '{dataset_path}' not found or inaccessible."
            )
            self.job_queue.task_done()
            return

        self.active_jobs.append(job_name)

        # 2. รอจน RAM จำลองเพียงพอ
        print(f"[{job_name}] Waiting for {req_ram}GB RAM...")

        while True:
            with self.ram_lock:
                if self.available_ram_gb >= req_ram:
                    self.available_ram_gb -= req_ram
                    break

            time.sleep(0.5)

        print(f"[{job_name}] Allocated {req_ram}GB RAM.")

        # 3. ขอ GPU ตามลำดับหมายเลขเดียวกันทุกงาน
        sorted_gpus = sorted(req_gpus)

        if sorted_gpus:
            print(f"[{job_name}] Waiting for GPUs {sorted_gpus}...")

        for gpu in sorted_gpus:
            self.gpu_locks[gpu].acquire()
            self.gpu_status[gpu] = f"BUSY ({job_name})"

        if sorted_gpus:
            print(f"[{job_name}] Acquired GPUs {sorted_gpus}. Running!")
        else:
            print(f"[{job_name}] Running on CPU only!")

        # 4. จำลองเวลาทำงาน
        time.sleep(duration)
        print(f"[{job_name}] Finished successfully.")

        # 5. คืน GPU และ RAM
        for gpu in reversed(sorted_gpus):
            self.gpu_status[gpu] = "IDLE"
            self.gpu_locks[gpu].release()

        with self.ram_lock:
            self.available_ram_gb += req_ram

        self.active_jobs.remove(job_name)
        self.job_queue.task_done()

    def shutdown(self):
        self.job_queue.join()
        self.is_running = False
        self.scheduler_thread.join()
        self.dash_thread.join()

        print("\n=== Cluster OS Shutdown Gracefully ===")


def main():
    with open("secure_dataset.csv", "w") as f:
        f.write("dummy data")

    print("=== Booting AI Cluster OS (64GB RAM, 4 GPUs) ===")
    os_system = AIClusterOS(total_ram_gb=64, num_gpus=4)

    # A: Training ใช้ RAM มาก และ GPU 3 ตัว
    os_system.submit_job(
        "Workload_A_LLaMA",
        "secure_dataset.csv",
        req_ram=40,
        req_gpus=[2, 1, 0],
        duration=8,
    )
    time.sleep(1)

    # B: Preprocessing ไม่ใช้ GPU
    os_system.submit_job(
        "Workload_B_Preproc",
        "secure_dataset.csv",
        req_ram=16,
        req_gpus=[],
        duration=6,
    )
    time.sleep(1)

    # C: Inference ใช้ GPU 3 ที่ยังว่างอยู่
    os_system.submit_job(
        "Workload_C_Infer",
        "secure_dataset.csv",
        req_ram=2,
        req_gpus=[3],
        duration=3,
    )
    time.sleep(1)

    # D: ใช้ชื่อไฟล์ที่ไม่มีอยู่
    os_system.submit_job(
        "Workload_D_Hacker",
        "secret_keys.txt",
        req_ram=1,
        req_gpus=[],
        duration=1,
    )

    os_system.shutdown()
    os.remove("secure_dataset.csv")


if __name__ == "__main__":
    main()