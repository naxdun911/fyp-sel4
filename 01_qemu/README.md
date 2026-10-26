# Test 1: QEMU (emulated)

Result status: NOT valid evidence. QEMU TCG emulation does not model real
cache or memory behaviour. Kept only to show the benchmark ran end to end.

- Benchmark: sel4bench SMP benchmark (apps/smp), IPC per second, 1 to 4
  ping/pong pairs, RUNS=10, SAMPLE_TIME=100 ms.
- Code: unmodified upstream sel4bench (commit 18f9d5f).
  Files here: smp.h (delays 500, 4000, 32000 cycles) and main.c (pairs are
  same-core: ping and pong on the same core).
- Platform: qemu-arm-virt, AArch64, cortex-a53, 4 CPUs, 1024 MB.

Configure (from ~/sel4bench-arm, build folder build_smp_tmr):

    ../init-build.sh -DPLATFORM=qemu-arm-virt -DAARCH64=TRUE -DARM_HYP=TRUE -DSMP=TRUE -DIRQUSER=OFF -DSCHED=OFF -DSIGNAL=OFF -DMAPPING=OFF -DSYNC=OFF -DAllowUnstableOverhead=ON -DKernelArmExportPCNTUser=ON -DKernelArmExportPTMRUser=ON -DCROSS_COMPILER_PREFIX=aarch64-linux-gnu-
    ninja

Run (from build_smp_tmr):

    qemu-system-aarch64 -machine virt,virtualization=on,highmem=off,secure=off,gic-version=2 -cpu cortex-a53 -nographic -m size=1024 -smp 4 -kernel images/sel4benchapp-image-arm-qemu-arm-virt

Log: ../logs/qemu-emulated/smp_arm_tmr_run1.log (workbook sheet "SMP Scaling").
Other files in ../logs/qemu-emulated are other QEMU attempts.
