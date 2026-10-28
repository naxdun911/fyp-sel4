# fyp-sel4

Performance Isolation for Multicore seL4 (final year project).
Group 20

seL4 serialises kernel execution with a Big Kernel Lock (BKL), so IPC load on
one core can interfere with other cores. This repo holds the baseline
measurements taken before any kernel change: how IPC throughput scales with
core count on real hardware (Raspberry Pi 4 Model B, 8GB, 4x Cortex-A72), and
how much one core loses when the other cores are busy with IPC.

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
| 05_rpi4_noise | Pi 4B, victim pair on Core_0 only, noise from 0 to 3 other cores, 6 runs |

## Scaling (tests 2 to 4)

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

## Isolation under noise (test 5)

One victim pair runs same-core on Core_0 and is the only pair measured. Pairs
on Cores 1 to 3 are the noise and always run back-to-back IPC (0 cycle delay),
added one core at a time. Drop in Core_0 throughput against the same run with
no noise, mean of 6 runs:

| Victim delay (cycles) | 1 noise core | 2 noise cores | 3 noise cores |
|---|---|---|---|
| 0 | 30.1% | 57.0% | 69.1% |
| 500 | 29.6% | 24.3% | 47.2% |
| 4000 | 8.3% | 10.3% | 19.3% |
| 32000 | 1.3% | 1.9% | 3.9% |

The 0-noise rows reproduce the test 3 1-core means within 0.5%, so the code
change affected nothing but the noise. With 3 noise cores the victim settles
near 318,500 IPC/s at both 0 and 500 cycles, although alone it reached
1.03M and 603k; four times that is about 1.27M, the same ceiling seen in
test 3. Even a light IPC user (32000 cycles) still loses 3.9%.

Other files:
- logs/ : raw serial logs of every valid run, plus the earlier QEMU attempts.
- sel4_smp_scaling.xlsx : results workbook (one sheet per test, a same-core vs
  cross-core comparison sheet, a noise sheet, and notes).
- extract_smp.py : reads the logs and prints means, run-to-run spread and
  efficiency. Example: python3 extract_smp.py logs/zero0*.log
- extract_noise.py : same for test 5, printing Core_0 means and the drop
  against the 0-noise row. Example: python3 extract_noise.py logs/noise0*.log

Not in the repo: the built boot images (regenerated with ninja) and empty or
incomplete logs.

Known limits: the QEMU numbers are not evidence about BKL contention. The
explanation that cross-core IPC takes the slowpath and needs inter-processor
interrupts has not been checked in the kernel source. The BKL lock type has
not been checked either, and it matters because a queue-based fair lock would
explain the roughly equal shares seen in test 5. The build type (release or
debug, MCS or not) is unconfirmed. At 500 cycles the victim is faster with 2
noise cores than with 1 in 6 of 6 runs, unexplained. A brk-region warning
printed at startup has not been investigated.