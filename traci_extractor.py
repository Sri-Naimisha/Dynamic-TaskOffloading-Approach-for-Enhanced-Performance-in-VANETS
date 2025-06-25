import sys
import traci
import json

sumocfg_file = sys.argv[1]  # e.g., simulation_100.sumocfg
output_vehicle_json = f"vehicles_{sys.argv[2]}.json"
output_infra_json = f"infrastructure_{sys.argv[2]}.json"

traci.start(["sumo", "-c", sumocfg_file])

vehicles = []
infra = []

step = 0
extracted = False
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    step += 1

    if step == 100 and not extracted:
        # Vehicles
        for vid in traci.vehicle.getIDList():
            x, y = traci.vehicle.getPosition(vid)
            vehicles.append({"id": vid, "x": x, "y": y})
        # RSU / Edge POIs
        for poi_id in traci.poi.getIDList():
            x, y = traci.poi.getPosition(poi_id)
            infra.append({"id": poi_id, "x": x, "y": y})
        extracted = True

traci.close()

# Save both files
with open(output_vehicle_json, "w") as f:
    json.dump(vehicles, f, indent=2)

with open(output_infra_json, "w") as f:
    json.dump(infra, f, indent=2)

print(f"✅ Step #{step} — Extracted {len(vehicles)} vehicles and {len(infra)} infrastructure points")
