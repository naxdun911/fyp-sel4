Test 05: Raspberry Pi 4B, noise interference on Core_0 (same-core pairs)

Design
- Pair 0 (ping and pong on Core_0) is the victim, using the swept delay (0, 500, 4000, 32000 cycles).
- Pairs 1 to 3 (Cores 1 to 3) are noise, always back-to-back IPC (0 cycle delay).
- Noise levels 0, 1, 2, 3. The Cores column in the JSON output means 1 + noise cores.
- Only Core_0 IPC/s is measured. Clock pinned (force_turbo=1).

Changes vs upstream: see main.c.patch and smp.h.

Build: ninja in build_rpi4, image saved as images/sel4benchapp-image-noise.
Run: copy image to the SD card as sel4benchapp-image-arm-bcm2711, capture serial with picocom to logs/noiseNN_<timestamp>.log, full power cycle per run.
Parse: python3 extract_noise.py logs/noise0[1-6]_*.log > 05_rpi4_noise/results_summary.txt

Results: 6 valid runs, see results_summary.txt.
