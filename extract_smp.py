#!/usr/bin/env python3
"""Extract SMP benchmark means from sel4bench picocom logs.

Usage: python3 extract_smp.py ~/fyp-results/run*.log
"""
import json
import re
import sys
from collections import defaultdict


def extract_json(path):
    """Pull the JSON blob between the JSON OUTPUT markers."""
    with open(path, "r", errors="replace") as fh:
        text = fh.read()
    m = re.search(r"JSON OUTPUT\s*(\[.*\])\s*END JSON OUTPUT", text, re.S)
    if not m:
        return None
    blob = m.group(1)
    # strip stray CR and any console line-wrapping artefacts
    blob = blob.replace("\r", "")
    return json.loads(blob)


def smp_rows(doc):
    """Yield (cycles, cores, mean) for the SMP benchmark section."""
    for bench in doc:
        if bench.get("Benchmark") != "SMP Benchmark":
            continue
        for r in bench.get("Results", []):
            yield r["Cycles"], r["Cores"], r["Mean"]


def main(paths):
    # data[(cycles, cores)] = [mean per run]
    data = defaultdict(list)
    ok_runs = []

    for p in paths:
        try:
            doc = extract_json(p)
        except json.JSONDecodeError as e:
            print(f"SKIP {p}: JSON parse failed ({e})", file=sys.stderr)
            continue
        if doc is None:
            print(f"SKIP {p}: no JSON OUTPUT block found", file=sys.stderr)
            continue
        rows = list(smp_rows(doc))
        if not rows:
            print(f"SKIP {p}: no SMP Benchmark section", file=sys.stderr)
            continue
        ok_runs.append(p)
        for cycles, cores, mean in rows:
            data[(cycles, cores)].append(mean)

    if not ok_runs:
        print("No usable logs.", file=sys.stderr)
        return 1

    n = len(ok_runs)
    print(f"Runs parsed: {n}")
    for p in ok_runs:
        print(f"  {p}")
    print()

    cycle_vals = sorted({c for c, _ in data})
    core_vals = sorted({k for _, k in data})

    for cycles in cycle_vals:
        print(f"=== Delay {cycles} cycles ===")
        print(f"{'Cores':>5} {'Mean IPC/s':>14} {'SD(runs)':>10} "
              f"{'Spread%':>8} {'vs linear':>10}")
        base = None
        for cores in core_vals:
            vals = data.get((cycles, cores))
            if not vals:
                continue
            avg = sum(vals) / len(vals)
            if len(vals) > 1:
                var = sum((v - avg) ** 2 for v in vals) / (len(vals) - 1)
                sd = var ** 0.5
            else:
                sd = 0.0
            spread = (max(vals) - min(vals)) / avg * 100 if avg else 0.0
            if cores == 1:
                base = avg
            eff = (avg / (base * cores) * 100) if base else float("nan")
            print(f"{cores:>5} {avg:>14.1f} {sd:>10.1f} "
                  f"{spread:>7.2f}% {eff:>9.1f}%")
        print()

    # Monotonicity check: does adding a core ever reduce throughput?
    print("=== Monotonicity check (per run) ===")
    for cycles in cycle_vals:
        for i in range(len(core_vals) - 1):
            a, b = core_vals[i], core_vals[i + 1]
            va = data.get((cycles, a), [])
            vb = data.get((cycles, b), [])
            if len(va) != len(vb) or not va:
                continue
            drops = sum(1 for x, y in zip(va, vb) if y < x)
            if drops:
                print(f"  {cycles:>6} cycles: {b} cores SLOWER than {a} "
                      f"in {drops}/{len(va)} runs")
    print("  (no lines above means throughput rose with every added core)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    sys.exit(main(sys.argv[1:]))
