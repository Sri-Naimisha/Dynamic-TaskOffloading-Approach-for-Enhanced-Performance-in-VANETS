import json
import time
import math
import numpy as np
from scipy.optimize import linear_sum_assignment

def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def run_kmm(vehicle_file, infra_file):
    with open(vehicle_file) as vf:
        vehicles = json.load(vf)
    with open(infra_file) as inf:
        infra = json.load(inf)

    vehicle_positions = [(v["id"], (v["x"], v["y"])) for v in vehicles]
    server_positions = [(s["id"], (s["x"], s["y"])) for s in infra]

    if not vehicle_positions or not server_positions:
        return 0.0, 0.0, 0.0

    # Build cost matrix
    cost_matrix = []
    for _, v_pos in vehicle_positions:
        row = [euclidean(v_pos, s_pos) for _, s_pos in server_positions]
        cost_matrix.append(row)

    cost_matrix = np.array(cost_matrix)

    start = time.time()
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    end = time.time()

    total_delay = 0
    assigned = len(row_ind)
    for i, j in zip(row_ind, col_ind):
        delay = 0.1 + (cost_matrix[i][j] / 1000)  # Same delay logic as greedy
        total_delay += delay

    exec_time = end - start
    avg_delay = total_delay / assigned if assigned > 0 else 0
    throughput = assigned / exec_time if exec_time > 0 else 0

    return round(avg_delay, 4), round(exec_time, 6), round(throughput, 4)

# ==== Run for all vehicle counts ====

results = []
for count in [50, 100, 500, 1000]:
    print(f"🚦 Running KMM for {count} vehicles")
    v_file = f"vehicles_{count}.json"
    i_file = f"infrastructure_{count}.json"
    delay, exec_time, throughput = run_kmm(v_file, i_file)
    results.append({
        "vehicles": count,
        "delay": delay,
        "time": exec_time,
        "throughput": throughput
    })

with open("kmm_metrics.json", "w") as f:
    json.dump(results, f, indent=2)

print("✅ Metrics saved to kmm_metrics.json")
