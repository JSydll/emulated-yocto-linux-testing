# Emulated testing of Yocto-based projects using QEMU and Labgrid

To allow location-independent testing while still being closer to the target architecture,
this demo shows an end-to-end setup of a Yocto build, producing a `qemuarm` image that
is then used as a `labgrid` target and tested using `PyTest`.

## Usage

Most of the environment is dockerized, so you should only need `Docker` and `bash`.

Simply source the `env-init` file and then execute, for example:

```bash
build-image
build-publish
test-run-pytest --lg-env config/qemuarm.yaml
```

If you want to build the `raspberrypi4` reference image, you need to
`export TARGET_MACHINE=raspberrypi`before sourcing the `env-init`.

The `labgrid` environment configuration is currently using hardcoded connection
settings. You need to setup your test host to share its network with the Raspberry Pi
[e.g. like described here](https://askubuntu.com/questions/996963/connecting-pc-and-raspberrypi-using-lan-cable).

### Parallel test execution

One of the main advantages of using an emulated target for testing is that
it allows scaling out - i.e. by spawning multiple QEMU instances.
This can be achieved by adding the `-n auto` option to the test execution command.

## Solution requirements

To be of value, the proposed solution aims to fulfill a set of requirements:

- _Reproducible tests_: Obviously, each test should produce the same result given
  the same input image when run repeatedly. However, this can be non-trivial in
  practice, if the DUT might be in a random starting state. This leads to another
  desired characteristic of the test environment:

- _Ephemeral DUT state_: To avoid complex logic to put the DUT in a deterministic
  starting state, it can be beneficial to (optionally) start from scratch on every
  run. This might come with some setup/teardown overhead in itself, though.

- _Target-independent tests_: It should be possible to have an unified test implementation
  for both real-hardware and emulated targets. If necessary, tests that only apply on
  either one can be marked and excluded on a global level.

## Approach

- Use reference integrations for both `qemuarm` and a real board (Raspberry Pi 4). These do differ especially in the boot chain, but run the same `core-image-minimal`.
- Use of Yocto's `multiconfig` to mimic different software versions, resulting in one build producing three versions.
- Publish build artifacts into a mount-volume of the test environment Docker container.
- Mount the volume read-only to ensure artifacts are not modified.
- Provide a `labgrid` environment config for emulated targets, one target per software version to have that "preinstalled".
- Use the built images as disks with the `-snapshot` option, making the QEMU instances ephemeral. This provides deterministic start conditions for tests, reduces test setup time, and eliminates the need for cleanup after tests.
- Use of function-scoped fixtures for running complex feature tests, such as software updates.
- Allow parallel execution of tests using `pytest-xdist` - this is only possible with read-only images and clean start on each test case.

## Insights

### Yocto integration

- getting pflash to work was a bit painful as it requires according kernel configuration
- some machine-related variables can only be set when using an machine override
- `qemu-system-arm` has an unresolved bug in allowing writes to the pflash in versions 5.9 to 9.1

### Test setup

- QEMU's `-snapshot` option allows to have ephemeral instances

## Limitations

For the sake of simplicity, this demonstration does not aim to reach full comparability
in the benchmarks between emulated and in-hardware setups. It simply uses off-the-shelf
reference integrations, so the findings have several limitations:

- Performance differences:
  - Raspberry Pi 4: Cortex-A72 4x 1.8GHz, 4 GB LPDDR4-3200 SDRAM (in 32bit mode, though)
  - QEMUarm: Cortex-A15, 3 GB RAM 
- Obvious differences between test and "productive" images
  - Target specific Boot flow
  - Changes introduced in `meta-testing`
- Oversimplified HW access setup for Raspberry Pi 4

## Benchmarks

Running the update tests on

**Real hardware (Raspberry Pi 4)**

```bash
$ time test-run-pytest --durations=8 --lg-env config/raspberrypi4.yaml -m update
...
=== slowest 8 durations ===
96.52s call     test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.latest]
93.81s call     test_update/update_flow_test.py::test_update_from_lts_succeeds[SoftwareVersion.latest]
91.91s setup    test_update/update_flow_test.py::test_update_from_lts_succeeds[SoftwareVersion.lts]
88.03s setup    test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.latest]
78.18s call     test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.lts]
76.54s call     test_update/update_flow_test.py::test_update_from_latest_succeeds[SoftwareVersion.latest]
72.81s call     test_update/update_flow_test.py::test_update_from_lts_succeeds[SoftwareVersion.lts]
26.42s setup    test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.lts]
=== 5 passed, 2 deselected in 627.57s (0:10:27) ===

real    10m28,726s
```

**Emulated, with sequential execution**

```bash
$ time test-run-pytest --durations=8 --lg-env config/qemuarm.yaml -m update

=== slowest 8 durations ===
154.11s setup    test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.latest]
153.63s call     test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.lts]
145.26s call     test_update/update_flow_test.py::test_update_from_latest_succeeds[SoftwareVersion.latest]
142.39s call     test_update/update_flow_test.py::test_update_from_lts_succeeds[SoftwareVersion.lts]
141.36s call     test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.latest]
141.02s call     test_update/update_flow_test.py::test_update_from_lts_succeeds[SoftwareVersion.latest]
61.11s setup    test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.lts]
58.99s setup    test_update/update_flow_test.py::test_update_from_latest_succeeds[SoftwareVersion.latest]
=== 5 passed, 2 deselected in 1057.99s (0:17:37) ===

real    17m39,257s
```

**Emulated, with parallel execution**

```bash
$ time test-run-pytest -n auto --durations=5 --lg-env config/qemuarm.yaml -m update

4 workers [5 items]     
scheduling tests via LoadScheduling

=== slowest 5 durations ===
188.41s call     test_update/update_flow_test.py::test_update_from_lts_succeeds[SoftwareVersion.latest]
187.38s call     test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.latest]
187.04s call     test_update/update_flow_test.py::test_update_from_lts_succeeds[SoftwareVersion.lts]
186.63s call     test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.lts]
152.17s call     test_update/update_flow_test.py::test_update_from_latest_succeeds[SoftwareVersion.latest]
=== 5 passed in 472.65s (0:07:52) ===

real    7m53,984s
```