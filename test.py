import json
import time
import bisect

# ---- Load the data we already generated ----
with open("drivers.json", "r") as f:
    drivers_list = json.load(f)

TARGET_ID = "KGL-09999"   # near the end of the list -> worst case for linear search
NUM_LOOKUPS = 5000        # simulate 5,000 customer requests


# ---- Method 1: Linear Search O(N) ----
def find_driver_linear(drivers, driver_id):
    for driver in drivers:
        if driver["driver_id"] == driver_id:
            return driver
    return None


# ---- Method 2: Binary Search O(log N) ----
sorted_drivers = sorted(drivers_list, key=lambda d: d["driver_id"])
sorted_ids = [d["driver_id"] for d in sorted_drivers]

def find_driver_binary(sorted_drivers, sorted_ids, driver_id):
    i = bisect.bisect_left(sorted_ids, driver_id)
    if i < len(sorted_ids) and sorted_ids[i] == driver_id:
        return sorted_drivers[i]
    return None


# ---- Method 3: Hash Map O(1) ----
def build_driver_lookup(drivers):
    return {d["driver_id"]: d for d in drivers}

driver_lookup = build_driver_lookup(drivers_list)

def find_driver_hash(driver_map, driver_id):
    return driver_map.get(driver_id)


# ---- Timing helper ----
def time_it(label, func, *args):
    start = time.perf_counter()
    for _ in range(NUM_LOOKUPS):
        result = func(*args)
    end = time.perf_counter()
    total_ms = (end - start) * 1000
    avg_us = (total_ms / NUM_LOOKUPS) * 1000
    print(f"{label:15s} | total: {total_ms:10.3f} ms | avg/lookup: {avg_us:10.3f} µs")
    return total_ms, result


# ---- Run all three ----
print(f"Running {NUM_LOOKUPS} lookups each for driver {TARGET_ID}\n")

linear_ms, r1 = time_it("Linear Search", find_driver_linear, drivers_list, TARGET_ID)
binary_ms, r2 = time_it("Binary Search", find_driver_binary, sorted_drivers, sorted_ids, TARGET_ID)
hash_ms,  r3  = time_it("Hash Map",      find_driver_hash, driver_lookup, TARGET_ID)

print("\nAll methods returned the same driver?", r1 == r2 == r3)
print(f"\nSpeedup vs Linear:")
print(f"  Binary Search: {linear_ms / binary_ms:,.0f}x")
print(f"  Hash Map:      {linear_ms / hash_ms:,.0f}x")