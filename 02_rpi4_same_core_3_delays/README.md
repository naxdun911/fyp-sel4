# Test 2: Raspberry Pi 4B, same-core pairs, delays 500 / 4000 / 32000

- Benchmark: sel4bench SMP benchmark (apps/smp), IPC per second, 1 to 4
  ping/pong pairs, RUNS=10, SAMPLE_TIME=100 ms.
- Code: unmodified upstream sel4bench (commit 18f9d5f).
  Files here: smp.h (delays 500, 4000, 32000 cycles) and main.c (ping and
  pong of each pair pinned to the same core).
- Platform: Raspberry Pi 4 Model B, 8GB, BCM2711, 4x Cortex-A72, passive
  heatsink, no fan. ARM clock not pinned (force_turbo not set).

Configure (from ~/sel4bench-arm, build folder build_rpi4):

    ../init-build.sh -DPLATFORM=rpi4 -DAARCH64=TRUE -DSMP=TRUE -DRPI4_MEMORY=8192 -DCROSS_COMPILER_PREFIX=aarch64-linux-gnu- -DKernelArmExportPCNTUser=ON -DKernelArmExportPTMRUser=ON -DIRQUSER=OFF -DSCHED=OFF -DSIGNAL=OFF -DMAPPING=OFF -DSYNC=OFF
    cmake -DElfloaderImage=elf -DSel4benchAllowSettingsOverride=ON .
    ninja

Boot: Pi firmware loads U-Boot 2024.01 from the SD card, which runs
fatload mmc 0 0x30000000 sel4benchapp-image-arm-bcm2711 then bootelf
0x30000000. config.txt: arm_64bit=1, enable_uart=1, enable_gic=1,
kernel=u-boot.bin, device_tree=bcm2711-rpi-4-b.dtb.
Output captured over a USB-TTL serial cable with picocom at 115200 baud.

Logs: ../run01_*.log to ../run05_*.log (5 full power-cycle runs, workbook
sheet "SMP Scaling (RPi4B)"). run06 is an extra complete run on the same
image and is not part of the 5-run means.
