import os

vehicle_counts = [50, 100, 500, 1000]

for count in vehicle_counts:
    if count == 50:
        sumocfg = "map.sumocfg"  # Special case for 50 vehicles
    else:
        sumocfg = f"simulation_{count}.sumocfg"

    print(f"\n🚦 Running SUMO simulation for {count} vehicles")
    sumo_command = f"sumo -c {sumocfg}"
    os.system(sumo_command)

    print(f"\n🚀 Running Greedy logic for {count} vehicles")
    os.system(f"wsl python3 /mnt/c/Users/srina/greedy.py {count}")

