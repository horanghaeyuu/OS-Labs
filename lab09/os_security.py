import os
import stat


def main():
    secure_file = "secret_config.json"

    # จัดการไฟล์จากการรันครั้งก่อน
    if os.path.exists(secure_file):
        os.chmod(secure_file, 0o600)
        os.remove(secure_file)

    # สร้างไฟล์ข้อมูลจำลอง
    with open(secure_file, "w") as f:
        f.write('{"api_key": "DEMO_KEY_ONLY"}')

    print(f"Created {secure_file}.")

    # ให้เจ้าของอ่านได้อย่างเดียว
    print("Locking file permissions to Read-Only (0o400)...")
    os.chmod(secure_file, 0o400)

    permissions = stat.filemode(os.stat(secure_file).st_mode)
    print(f"New Permissions: {permissions}")

    # ทดลองเขียนเพิ่มลงในไฟล์ที่ล็อกแล้ว
    print("\nAttempting to write to the file...")

    try:
        with open(secure_file, "a") as f:
            f.write("\nMALICIOUS HACKER DATA")

        print("Success! Data written.")
    except PermissionError as e:
        print(f">>> [OS KERNEL BLOCKED] PermissionError: {e}")
        print(">>> The Operating System successfully protected the file!")


if __name__ == "__main__":
    main()