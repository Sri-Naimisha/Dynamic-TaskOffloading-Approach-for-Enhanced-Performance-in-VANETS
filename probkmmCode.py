import json
import time
import math
import numpy as np
from scipy.optimize import linear_sum_assignment

def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def run_prob_kmm(vehicle_file, infra_file):
    with open(vehicle_file) as vf:
        vehicles = json.load(vf)
    with open(infra_file) as inf:
        infra = json.load(inf)

    vehicle_positions = [(v["id"], (v["x"], v["y"])) for v in vehicles]
    server_positions = [(s["id"], (s["x"], s["y"])) for s in infra]

    # Step 1: Probabilistic Filtering — keep top N% nearest servers per vehicle
    filtered_map = []
    for _, v_pos in vehicle_positions:
        scored = []
        for sid, s_pos in server_positions:
            dist = euclidean(v_pos, s_pos)
            prob_score = math.exp(-dist / 1000)  # exponentially decay with distance
            scored.append((sid, s_pos, prob_score))
        
        scored.sort(key=lambda x: -x[2])  # highest score first
        top_k = scored[:min(10, len(scored))]  # take top 10 candidates
        filtered_map.append(top_k)

    # Step 2: Build Cost Matrix for KMM
    cost_matrix = []
    for i in range(len(vehicle_positions)):
        v_cost_row = []
        for sid, s_pos, score in filtered_map[i]:
            dist = euclidean(vehicle_positions[i][1], s_pos)
            v_cost_row.append(dist)
        cost_matrix.append(v_cost_row)

    # Padding matrix to make it square
    max_len = max(len(cost_matrix), max(len(row) for row in cost_matrix))
    for row in cost_matrix:
        while len(row) < max_len:
            row.append(9999)
    while len(cost_matrix) < max_len:
        cost_matrix.append([9999] * max_len)

    cost_matrix = np.array(cost_matrix)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    assigned = 0
    total_delay = 0
    start = time.time()

    for i, j in zip(row_ind, col_ind):
        if i < len(vehicle_positions) and j < len(filtered_map[i]):
            dist = cost_matrix[i][j]
            if dist < 9999:
                assigned += 1
                delay = 0.1 + (dist / 1000)
                total_delay += delay

    end = time.time()
    exec_time = end - start
    avg_delay = total_delay / assigned if assigned > 0 else 0
    throughput = assigned / exec_time if exec_time > 0 else 0

    return round(avg_delay, 4), round(exec_time, 6), round(throughput, 4)

# ==== Run for all vehicle counts ====

results = []
for count in [50, 100, 500, 1000]:
    print(f"🚦 Running Prob+KMM for {count} vehicles")
    v_file = f"vehicles_{count}.json"
    i_file = f"infrastructure_{count}.json"
    delay, exec_time, throughput = run_prob_kmm(v_file, i_file)
    results.append({
        "vehicles": count,
        "delay": delay,
        "time": exec_time,
        "throughput": throughput
    })

with open("probkmm_metrics.json", "w") as f:
    json.dump(results, f, indent=2)

print("✅ Metrics saved to probkmm_metrics.json")
