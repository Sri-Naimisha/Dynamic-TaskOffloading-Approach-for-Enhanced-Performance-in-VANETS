import json
import matplotlib.pyplot as plt

# === Load all metrics ===
with open("greedy_metrics.json") as f:
    greedy = json.load(f)
with open("kmm_metrics.json") as f:
    kmm = json.load(f)
with open("probkmm_metrics.json") as f:
    probkmm = json.load(f)

def extract(metric_list, key):
    return [m[key] for m in metric_list]

vehicles = extract(greedy, "vehicles")
xticks = [50, 100, 500, 1000]

# === Plot 1: Throughput ===
plt.figure(figsize=(9, 5))
plt.plot(vehicles, extract(greedy, "throughput"), 'o-', label="Greedy", linewidth=2, markersize=7)
plt.plot(vehicles, extract(kmm, "throughput"), 's-', label="KMM", linewidth=2, markersize=7)
plt.plot(vehicles, extract(probkmm, "throughput"), '^-', label="Prob + KMM", linewidth=2, markersize=7)

plt.title("Throughput vs. Number of Vehicles", fontsize=13)
plt.xlabel("Number of Vehicles", fontsize=12)
plt.ylabel("Throughput", fontsize=12)
plt.xticks(xticks)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("throughput_plot.png")
plt.show()

# === Plot 2: Delay ===
plt.figure(figsize=(9, 5))
plt.plot(vehicles, extract(greedy, "delay"), 'o-', label="Greedy", linewidth=2, markersize=7)
plt.plot(vehicles, extract(kmm, "delay"), 's-', label="KMM", linewidth=2, markersize=7)
plt.plot(vehicles, extract(probkmm, "delay"), '^-', label="Prob + KMM", linewidth=2, markersize=7)

plt.title("Delay vs. Number of Vehicles", fontsize=13)
plt.xlabel("Number of Vehicles", fontsize=12)
plt.ylabel("Average Delay", fontsize=12)
plt.xticks(xticks)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("delay_plot.png")
plt.show()

# === Plot 3: Execution Time in ms (log scale) ===
greedy_ms = [t * 1000 for t in extract(greedy, "time")]
kmm_ms = [t * 1000 for t in extract(kmm, "time")]
probkmm_ms = [t * 1000 for t in extract(probkmm, "time")]

plt.figure(figsize=(9, 5))
plt.plot(vehicles, greedy_ms, 'o-', label="Greedy", linewidth=2, markersize=7)
plt.plot(vehicles, kmm_ms, 's-', label="KMM", linewidth=2, markersize=7)
plt.plot(vehicles, probkmm_ms, '^-', label="Prob + KMM", linewidth=2, markersize=7)

# Add value annotations with slight offset
for i, v in enumerate(vehicles):
    plt.text(v, greedy_ms[i]*1.2, f"{greedy_ms[i]:.2f}", ha='center', fontsize=9)
    plt.text(v, kmm_ms[i]*1.2, f"{kmm_ms[i]:.2f}", ha='center', fontsize=9)
    plt.text(v, probkmm_ms[i]*1.2, f"{probkmm_ms[i]:.2f}", ha='center', fontsize=9)

plt.yscale("log")
plt.title("Execution Time vs. Number of Vehicles", fontsize=13)
plt.xlabel("Number of Vehicles", fontsize=12)
plt.ylabel("Execution Time (ms, log scale)", fontsize=12)
plt.xticks(xticks)
plt.grid(True, which="both", linestyle="--", linewidth=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("execution_time_plot_ms_log.png")
plt.show()
