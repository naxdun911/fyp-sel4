# fyp-sel4

Performance Isolation for Multicore seL4 (final year project).
E/21/254 - Manilgama N.C.

seL4 serialises kernel execution with a Big Kernel Lock (BKL), so IPC load on
one core can interfere with other cores. This repo holds the baseline
measurements taken before any kernel change: how IPC throughput scales with
core count on real hardware (Raspberry Pi 4 Model B, 8GB, 4x Cortex-A72).

Benchmark: the upstream sel4bench SMP benchmark (apps/smp). It runs 1 to 4
ping/pong thread pairs and reports IPC per second, with a busy-wait delay
between calls (0, 500, 4000 or 32000 cycles). Each test folder holds the exact
code used, a README with the build and run commands, and the patch against
upstream where the code was changed.

| Folder | Test |
|---|---|
| 01_qemu | QEMU emulation, same-core pairs, delays 500/4000/32000 (not valid evidence) |
| 02_rpi4_same_core_3_delays | Pi 4B, same-core pairs, delays 500/4000/32000, 5 runs |
| 03_rpi4_same_core_4_delays | Pi 4B, same-core pairs, delays 0/500/4000/32000, clock pinned, 7 runs |
| 04_rpi4_cross_core_4_delays | Pi 4B, ping and pong on different cores, delays 0/500/4000/32000, 6 runs |

Efficiency at 4 cores (4 pairs for the cross-core test), measured mean divided
by the 1-core mean times 4:

| Delay (cycles) | Same-core | Cross-core |
|---|---|---|
| 0 | 30.8% | 34.4% |
| 500 | 52.5% | 42.9% |
| 4000 | 97.1% | 83.4% |
| 32000 | 99.6% | 97.4% |

One cross-core pair is slower than one same-core pair by 2.90x at 0 cycles
and 1.04x at 32000 cycles. The cross-core 3 and 4 pair rows put two threads on
some cores, so they are a different workload from the same-core rows.

Other files:
- logs/ : raw serial logs of every valid run, plus the earlier QEMU attempts.
- sel4_smp_scaling.xlsx : results workbook (one sheet per test, a same-core vs
  cross-core comparison sheet, and notes).
- extract_smp.py : reads the logs and prints means, run-to-run spread and
  efficiency. Example: python3 extract_smp.py logs/zero0*.log

Not in the repo: the built boot images (regenerated with ninja) and empty or
incomplete logs.

Known limits: the QEMU numbers are not evidence about BKL contention. The
explanation that cross-core IPC takes the slowpath and needs inter-processor
interrupts has not been checked in the kernel source. A brk-region warning
printed at startup has not been investigated.
