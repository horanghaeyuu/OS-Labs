import os


def simulate_hpc_cluster():
    weight_file = "production_resnet50.pth"

    # เตรียมไฟล์ใหม่เมื่อรันซ้ำ
    if os.path.exists(weight_file):
        os.chmod(weight_file, 0o600)
        os.remove(weight_file)

    # สร้างไฟล์น้ำหนักโมเดลจำลอง
    print("Creating simulated production model weights...")

    with open(weight_file, "w") as f:
        f.write("0101010101010101010")

    # ทุกคนอ่านได้ แต่ไม่มีสิทธิ์เขียนตาม permission bits
    print("AI Ops: Securing model weights as Read-Only (0o444)...")
    os.chmod(weight_file, 0o444)

    print("\n[Junior Dev] Running script: training_job.py")
    print("[Junior Dev] Attempting to overwrite production weights!")

    try:
        with open(weight_file, "w") as model:
            model.write("Initializing random weights... Overwriting!")

        print("Write succeeded: check whether you are running with elevated privileges.")
    except PermissionError:
        print(">>> [DISASTER AVERTED] OS Kernel denied write access.")
        print(">>> The production model file was protected.")


if __name__ == "__main__":
    simulate_hpc_cluster()