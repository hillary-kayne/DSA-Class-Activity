import random
import json

def generate_drivers(n=10000):
    drivers = []
    for i in range(1, n + 1):
        drivers.append({
            "driver_id": f"KGL-{i:05d}",
            "name": f"Driver_{i}",
            "vehicle": random.choice(["Moto", "Car", "Bike"]),
            "rating": round(random.uniform(3.5, 5.0), 2),
            "active": random.choice([True, False]),
        })
    return drivers

drivers_list = generate_drivers(10000)

with open("drivers.json", "w") as f:
    json.dump(drivers_list, f, indent=2)

print(f"Wrote {len(drivers_list)} drivers to drivers.json")
