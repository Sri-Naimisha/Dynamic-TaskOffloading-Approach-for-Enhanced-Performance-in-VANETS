import json
import time
import math

def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def run_greedy(vehicle_file, infra_file):
    with open(vehicle_file) as vf:
        vehicles = json.load(vf)
    with open(infra_file) as inf:
        infra = json.load(inf)

    assigned = 0
    total_delay = 0
    start = time.time()

    for v in vehicles:
        vx, vy = v["x"], v["y"]
        distances = []
        for s in infra:
            sx, sy = s["x"], s["y"]
            dist = euclidean((vx, vy), (sx, sy))
            distances.append((dist, s["id"]))
        
        if distances:
            nearest = min(distances, key=lambda x: x[0])
            assigned += 1
            # Simulated delay as function of distance
            delay = 0.1 + (nearest[0] / 1000)
            total_delay += delay

    end = time.time()
    exec_time = end - start
    avg_delay = total_delay / assigned if assigned > 0 else 0
    throughput = assigned / exec_time if exec_time > 0 else 0

    return round(avg_delay, 4), round(exec_time, 6), round(throughput, 4)

# ==== Run for all vehicle counts ====

results = []
for count in [50, 100, 500, 1000]:
    print(f"🚦 Running Greedy for {count} vehicles")
    v_file = f"vehicles_{count}.json"
    i_file = f"infrastructure_{count}.json"
    delay, exec_time, throughput = run_greedy(v_file, i_file)
    results.append({
        "vehicles": count,
        "delay": delay,
        "time": exec_time,
        "throughput": throughput
    })

with open("greedy_metrics.json", "w") as f:
    json.dump(results, f, indent=2)

print("✅ Metrics saved to greedy_metrics.json")
