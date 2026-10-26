import sys, json, statistics as st

def load(path):
    t = open(path, errors="ignore").read()
    a = t.find("JSON OUTPUT")
    if a < 0:
        return None
    b = t.find("END JSON OUTPUT", a)
    seg = t[a + len("JSON OUTPUT"): b if b > 0 else len(t)]
    idx = [k for k in (seg.find("["), seg.find("{")) if k >= 0]
    if not idx:
        return None
    try:
        obj, _ = json.JSONDecoder().raw_decode(seg[min(idx):])
    except ValueError:
        return None
    rows = {}
    def walk(o):
        if isinstance(o, dict):
            if "Cycles" in o and "Cores" in o and "Mean" in o:
                rows[(int(o["Cycles"]), int(o["Cores"]))] = float(o["Mean"])
            else:
                for v in o.values():
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(obj)
    return rows or None

runs = []
for p in sys.argv[1:]:
    r = load(p)
    if r is None:
        print("skipped (no JSON):", p)
    else:
        runs.append(r)
print("Runs parsed:", len(runs))
if not runs:
    sys.exit(1)

delays = sorted({d for r in runs for (d, c) in r})
for d in delays:
    print("\n=== Victim delay %d cycles (Core_0 IPC/s) ===" % d)
    print("Noise cores   Mean IPC/s   SD(runs)  Spread%   Drop vs 0 noise   Drop range over runs")
    base = st.mean(r[(d, 1)] for r in runs)
    for c in (1, 2, 3, 4):
        v = [r[(d, c)] for r in runs]
        m = st.mean(v)
        sd = st.stdev(v) if len(v) > 1 else 0.0
        drops = [100.0 * (1 - r[(d, c)] / r[(d, 1)]) for r in runs]
        print("%6d %16.0f %10.0f %8.2f%% %12.1f%% %12.1f%% to %.1f%%" % (
            c - 1, m, sd, 100.0 * sd / m, 100.0 * (1 - m / base), min(drops), max(drops)))

print("\n=== Check: more noise gave HIGHER victim throughput (per run) ===")
found = False
for d in delays:
    for c in (2, 3, 4):
        n = sum(1 for r in runs if r[(d, c)] > r[(d, c - 1)])
        if n:
            found = True
            print("%6d cycles: %d noise cores higher than %d in %d/%d runs" % (d, c - 1, c - 2, n, len(runs)))
if not found:
    print("none, victim throughput fell with every added noise core in all runs")
