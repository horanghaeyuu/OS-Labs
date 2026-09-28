import os
import stat
import time


def inspect_file(filename):
    print(f"--- OS Inode Inspection for: {filename} ---")

    file_stats = os.stat(filename)

    inode_number = file_stats.st_ino
    file_size_bytes = file_stats.st_size

    # Linux: ctime คือเวลาที่สถานะไฟล์เปลี่ยน ไม่ใช่เวลาสร้างไฟล์
    status_changed_time = time.ctime(file_stats.st_ctime)
    modified_time = time.ctime(file_stats.st_mtime)

    permissions = stat.filemode(file_stats.st_mode)

    print(f"Inode Number:     {inode_number}")
    print(f"File Size:        {file_size_bytes} bytes")
    print(f"Status Changed:   {status_changed_time}")
    print(f"Last Modified:    {modified_time}")
    print(f"OS Permissions:   {permissions}")


def main():
    test_file = "dataset_sample.csv"

    with open(test_file, "w") as f:
        f.write("id,feature_1,feature_2,label\n")
        f.write("1,0.5,0.8,cat\n")

    inspect_file(test_file)


if __name__ == "__main__":
    main()