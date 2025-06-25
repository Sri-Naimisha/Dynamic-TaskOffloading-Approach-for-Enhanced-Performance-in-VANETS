# Dynamic Task Offloading in VANETs

This project implements a dynamic task offloading system in Vehicular Ad-hoc Networks (VANETs), using **probabilistic filtering** and the **Kuhn-Munkres (Hungarian) algorithm** to optimize task assignment from vehicles to edge servers and RSUs.

---

## Overview

Vehicles in a VANET generate computational tasks. These tasks can be offloaded to nearby vehicles, edge servers, or RSUs based on factors such as node availability, queue length, mobility, delay, execution time, and overall communication cost.
Our approach enhances performance by:

- Filtering candidate nodes using **probabilistic logic** 
- Assigning tasks optimally using the **Kuhn-Munkres (KMM)** algorithm

---

## 🔧 Technologies Used

- Python
- SUMO (Simulation of Urban Mobility)
- TraCI (Traffic Control Interface)
- Matplotlib, NumPy, Scikit-learn (for analysis and plotting)

---

## 🧠 Core Logic

1. **SUMO** is used to simulate real-time vehicle mobility.
2. **TraCI (Python)** extracts live vehicle and task data from SUMO.
3. **Probabilistic filtering** ranks possible offloading nodes (vehicles, RSUs, edge servers).
4. **Kuhn-Munkres algorithm** computes the optimal task-node assignment.
5. Performance is compared against:
   - Greedy offloading
   - KMM-only strategy

---

## Results

Our hybrid approach outperforms baselines by achieving:

- Lower average delay  
- Faster execution time  
- Higher throughput



