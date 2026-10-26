# Test 4: Raspberry Pi 4B, CROSS-core pairs, delays 0 / 500 / 4000 / 32000

- Change from test 3: in main.c the pong thread of pair i is pinned to core
  (i + PONG_CORE_OFFSET) % nr_cores with PONG_CORE_OFFSET 2, so every IPC
  crosses cores. Setting the offset to 0 gives test 3 again.
  Patch: main_c_vs_upstream.patch. smp.h is the same as test 3
  (smp_h_vs_upstream.patch). Upstream is sel4bench commit 18f9d5f.
- Thread layout: 1 pair uses cores 0 and 2. 2 pairs use all four cores with
  one thread each. 3 and 4 pairs put two threads on some or all cores, so
  those rows are a different workload from test 3. The Cores column in the
  workbook counts pairs.
- Platform, build and boot as in test 3, with force_turbo=1.

Rebuild: ninja only, in build_rpi4. The image was kept locally as
images/sel4benchapp-image-crosscore (not in the repo).

Logs: ../logs/cross01_20261022_082313.log, ../logs/cross02_*.log (2 files),
../logs/cross03_*.log, ../logs/cross04_*.log and ../logs/cross05_*.log. That is 6 valid
runs. Two empty cross01 logs are excluded. Workbook sheets
"SMP Scaling (RPi4B cross-core)" and "Same vs Cross Core".

Not verified: the explanation that cross-core IPC takes the slowpath and
needs inter-processor interrupts has not been checked in the kernel source.
