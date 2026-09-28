def simulate_fcfs(requests, initial_position):
    print("\n--- FCFS Disk Scheduling ---")
    current_pos = initial_position
    total_head_movement = 0
    path = [current_pos]

    for req in requests:
        total_head_movement += abs(current_pos - req)
        current_pos = req
        path.append(current_pos)

    print(f"Path: {' -> '.join(map(str, path))}")
    print(f">> Total Head Movement: {total_head_movement} cylinders")


def simulate_scan(requests, initial_position, max_cylinder=199):
    print("\n--- SCAN (Elevator) Disk Scheduling ---")

    sorted_requests = sorted(requests)
    left = [req for req in sorted_requests if req < initial_position]
    right = [req for req in sorted_requests if req >= initial_position]

    current_pos = initial_position
    total_head_movement = 0
    path = [current_pos]

    # เคลื่อนไปทางหมายเลข Cylinder ที่สูงขึ้นก่อน
    for req in right:
        total_head_movement += abs(current_pos - req)
        current_pos = req
        path.append(current_pos)

    # ไปถึงปลายดิสก์ก่อนกลับทิศทาง
    if current_pos != max_cylinder:
        total_head_movement += abs(current_pos - max_cylinder)
        current_pos = max_cylinder
        path.append(current_pos)

    # กลับลงมารับคำขอที่เหลือ
    for req in reversed(left):
        total_head_movement += abs(current_pos - req)
        current_pos = req
        path.append(current_pos)

    print(f"Path: {' -> '.join(map(str, path))}")
    print(f">> Total Head Movement: {total_head_movement} cylinders")


def main():
    io_requests = [98, 183, 37, 122, 14, 124, 65, 67]
    start_pos = 53

    print(f"Initial Head Position: {start_pos}")
    print(f"Incoming OS I/O Requests: {io_requests}")

    simulate_fcfs(io_requests, start_pos)
    simulate_scan(io_requests, start_pos)


if __name__ == "__main__":
    main()