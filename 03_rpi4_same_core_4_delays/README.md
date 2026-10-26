# Test 3: Raspberry Pi 4B, same-core pairs, delays 0 / 500 / 4000 / 32000

- Change from test 2: one row added to the delay table in smp.h,
  { .name = "0 cycles", .delay = 0.00000 }, so IPC runs back to back.
  Patch: smp_h_vs_upstream.patch. main.c is the unmodified upstream file
  (sel4bench commit 18f9d5f), pairs are same-core.
- Second change: force_turbo=1 added to config.txt to pin the ARM clock.
- Platform and benchmark settings as in test 2.

Rebuild: ninja only, in build_rpi4 (no reconfigure). The image was kept
locally as images/sel4benchapp-image-samecore (not in the repo).

Logs: ../zero01_*.log to ../zero06_*.log. That is 7 valid runs, because two
logs are named zero04 (timestamps 210536 and 211730). Workbook sheet
"SMP Scaling (RPi4B pinned)". One empty log from a run where picocom was
closed is excluded.
