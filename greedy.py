import json
import time
import random
import math
import sys

# -----------------------------
# ✅ Accept vehicle count
# -----------------------------
if len(sys.argv) < 2:
    print("Usage: python greedy.py <vehicle_count>")
    sys.exit(1)

vehicle_count = int(sys.argv[1])
input_file = f"filtered_candidates_{vehicle_count}.json"

# Load infrastructure (positions of edge servers)
with open("infrastructure.json") as f:
    infra = json.load(f)
edge_positions = {e["id"]: (e["x"], e["y"]) for e in infra["edges"]}

metrics = {"Greedy": []}


def calculate_delay(vehicle, edge):
    random.seed(hash(vehicle + edge) % 100000)
    return round(random.uniform(0.3, 1.0), 3)


def euclidean(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


print(f"\n🚦 Running simulation for {vehicle_count} vehicles")

with open(input_file) as f:
    vehicle_data = json.load(f)

print(f"➡️ Vehicles in JSON: {len(vehicle_data)}")

start_time = time.time()
assignments = []
total_delay = 0.0

print("📦 Offloading Path:")
print("-" * 40)

for v in vehicle_data:
    vehicle = v["vehicle_id"]
    target = v.get("target_vehicle_id", "Server")
    target_pos = (v.get("x", 0), v.get("y", 0))

    nearby_servers = v.get("nearby_edge_servers", []) + v.get("nearby_rsus", [])
    if not nearby_servers:
        continue

    best_server = None
    best_delay = float("inf")

    for server in nearby_servers:
        delay = calculate_delay(vehicle, server["id"])
        if delay < best_delay:
            best_delay = delay
            best_server = server["id"]

    if not best_server:
        continue

    total_delay += best_delay

    best_pos = edge_positions.get(best_server, (0, 0))
    dist_to_target = euclidean(best_pos, target_pos)

    if dist_to_target > 300:
        next_hop = min(
            [eid for eid in edge_positions if eid != best_server],
            key=lambda eid: euclidean(edge_positions[eid], target_pos)
        )
        print(f"🚗 {vehicle} → 🖥️ {best_server} → 🖥️ {next_hop} → 🎯 Vehicle {target}")
    else:
        print(f"🚗 {vehicle} → 🖥️ {best_server} → 🎯 Vehicle {target}")

    assignments.append((vehicle, best_server, target))

end_time = time.time()
total_time = round(end_time - start_time, 6)

assigned = len(assignments)
avg_delay = round(total_delay / assigned, 4) if assigned else 0
time_per_task = total_time / assigned if assigned else 0
throughput = round(1 / time_per_task, 4) if time_per_task else 0

print(f"\n✅ Assigned: {assigned} | 🕒 Time: {total_time}s | ⏱️ Avg Delay: {avg_delay} | ⏳ Time/Task: {round(time_per_task, 6)} | 📶 Throughput: {throughput}")

metrics["Greedy"].append({
    "vehicles": vehicle_count,
    "assigned": assigned,
    "throughput": throughput,
    "delay": avg_delay,
    "time": round(time_per_task, 6)
})

# -----------------------------
# ✅ Save to vehicle-count-specific file
# -----------------------------
with open(f"greedy_metrics_{vehicle_count}.json", "w") as f:
    json.dump(metrics, f, indent=4)

print(f"\n📊 Saved Greedy metrics to greedy_metrics_{vehicle_count}.json")

