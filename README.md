# Kigali Express — Driver Lookup Optimization

**Team Challenge** — comparing Linear Search, Binary Search, and Hash Map lookups for a 10,000-driver delivery fleet.

## 1. The Mission

A fast-food delivery app in Kigali has 10,000 drivers. Every customer request was scanning the driver list sequentially, causing high latency. This project compares three lookup strategies — **linear search**, **binary search**, and a **hash map** — with real, measured performance numbers.

**Task:** Convert the raw list of driver objects into a fast-lookup dictionary where the keys are driver IDs, replacing an O(N) scan with an O(1) lookup.

## 2. Sample Data Generation

10,000 sample driver records were generated (IDs `KGL-00001` … `KGL-10000`), each with a name, vehicle type, rating, and active status, then saved to `drivers.json`.

```python
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
```

## 3. Method 1 — Linear Search · O(N)

Scan the list one item at a time until it finds a match. Simple, but gets slower as the fleet grows — worst case checks all 10,000 drivers.

```python
def find_driver_linear(drivers, driver_id):
    for driver in drivers:
        if driver["driver_id"] == driver_id:
            return driver
    return None
```

## 4. Method 2 — Binary Search · O(log N)

Requires the list to be sorted by `driver_id` first, then repeatedly halves the search space.

```python
import bisect

sorted_drivers = sorted(drivers_list, key=lambda d: d["driver_id"])
sorted_ids = [d["driver_id"] for d in sorted_drivers]

def find_driver_binary(sorted_drivers, sorted_ids, driver_id):
    i = bisect.bisect_left(sorted_ids, driver_id)
    if i < len(sorted_ids) and sorted_ids[i] == driver_id:
        return sorted_drivers[i]
    return None
```

## 5. Method 3 — Hash Map (Dictionary) · O(1)

Converts the list into a dictionary keyed by `driver_id` once, up front. After that, every lookup is a direct, constant-time access — no scanning, regardless of fleet size. This is the core deliverable: the **mapping loop**.

```python
def build_driver_lookup(drivers):
    return {d["driver_id"]: d for d in drivers}

driver_lookup = build_driver_lookup(drivers_list)

def find_driver_hash(driver_map, driver_id):
    return driver_map.get(driver_id)
```

## 6. Measured Results

5,000 simulated lookups for driver `KGL-09999` (near the end of the list — worst case for linear search), run on the same 10,000-driver dataset:

| Method        | Big-O    | Total (5,000 lookups) | Avg per lookup | Speedup vs Linear |
|---------------|----------|------------------------|-----------------|---------------------|
| Linear Search | O(N)     | 4101.693 ms             | 820.339 µs      | 1x (baseline)       |
| Binary Search | O(log N) | 1.867 ms                | 0.373 µs        | 2,197x              |
| Hash Map      | O(1)     | 0.804 ms                | 0.161 µs        | 5,099x              |

All three methods were verified to return the identical, correct driver record — only the speed differs (`All methods returned the same driver? True`).

*Note: exact microsecond values vary by machine and Python version — what matters is the relative pattern (hash map fastest, then binary, then linear), which holds true consistently across test runs.*

## 7. Recommendation

- **Use the hash map** for the driver-matching endpoint — it's ~5,099x faster than a linear scan and the clear winner for a live, high-traffic API.
- **Binary search** (~2,197x faster) is a reasonable fallback if memory is extremely constrained and the list must stay array-based, but it needs the data kept sorted.
- **Linear search** should be retired from any request-path code — at 10,000 drivers it already costs ~820 µs per lookup, and that only gets worse as the fleet grows.


## Project Files

- `drivers.json` — 10,000 generated driver records
- Data generation script — builds and saves the sample dataset
- Lookup comparison script — implements all three methods and times 5,000 lookups each
