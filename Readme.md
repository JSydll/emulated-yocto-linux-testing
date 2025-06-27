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
test-run-pytest
```

If you want to build the `raspberrypi4-64` reference image, you need to
`export TARGET_MACHINE=raspberrypi-64`before sourcing the `env-init`.

The `labgrid` environment configuration is currently using hardcoded connection
settings. You need to setup your test host to share its network with the Raspberry Pi
[e.g. like described here](https://askubuntu.com/questions/996963/connecting-pc-and-raspberrypi-using-lan-cable).

### Parallel test execution

One of the main advantages of using an emulated target for testing is that
it allows scaling out - i.e. by spawning multiple QEMU instances.
This can be achieved by adding the `-n auto` option to the test execution command.

### Selection of tagged tests

As not every test has _meaningful results_ when executed in every development
scenario (such as merging feature PRs, running nightlies/weeklies or building a
product release), grouping tests along their applicable scenarios can bring significant
efficiency gains, too.
In this demo for example, you can select a subset of tests to be executed as a smoke
test by adding the `-m smoketest` option.
See the [pytest.ini](test/pytest.ini) for more details.

---

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

## Assumptions

- Tests are expected to be grouped by execution environment, i.e. individual pipeline stages
  would be used to run host/emulation or hardware tests.
- Each test scope (unit/component/integration/system/...) also runs in an individual stage,
  potentially building a test matrix against the different environments.


## Approach

- Use reference integrations for both `virt-aarch64` and a real board (Raspberry Pi 4). These do differ especially in the boot chain, but run the same `core-image-minimal`.
- Use of Yocto's `multiconfig` to mimic different software versions, resulting in one build producing three versions.
  > Attention: This wouldn't be done in a productive environment - time will produde multiple versions there instead
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
  (supposedly this also holds true for `qemu-system-aarch64` but was not verified)

### Test setup

- QEMU's `-snapshot` option allows to have ephemeral instances

## Limitations

For the sake of simplicity, this demonstration does not aim to reach full comparability
in the benchmarks between emulated and in-hardware setups. It simply uses off-the-shelf
reference integrations, so the findings have several limitations:

- "Hardware" differences:
  - Raspberry Pi 4: Cortex-A72 4x 1.8GHz, 4 GB LPDDR4-3200 SDRAM
  - `virt-aarch64`: Cortex-A72 4x up to 2GHz, 4 GB (V)RAM 
- Obvious differences between test and "productive" images
  - Target specific boot flow
  - Changes introduced in `meta-testing`
- Oversimplified hardware access setup for Raspberry Pi 4

## Benchmarks

To get some indication of performance and possible benefits of using emulation,
the update tests were executed on an Ubuntu24.04 WSL instance, running on a 8/16 core
Intel i9 laptop with a nominal 32GB of RAM.

### Short summary

The preliminary findings (keeping the above limitations in mind):

- tests executed in parallel on emulation can be **up to 4.5 times faster** than running them on hardware
- parallel execution alone brings a **speed gain of around 2.8 times**
- tests on hardware were observed more fragile, at times leading to every second run to fail
- speed gains in the emulated setup heavily depend on the host performance (i.e. running tests on less 
  performant hosts may diminish)
- for some tests it might actually be more efficient to execute them sequentially on the same (continuously
  running QEMU instance), because of the overhead of booting a dedicated instance for each

**Attention**: These results are of limited validity, given they were not acquired in a scientific
or cleanly reproducible way.

### Results on real hardware (Raspberry Pi 4)

```bash
$ time test-run-pytest --durations=8 -m update

=== slowest 8 durations ===
103.93s setup    test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.latest]
92.70s call     test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.latest]
87.21s call     test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.lts]
78.03s call     test_update/update_flow_test.py::test_update_from_latest_succeeds[SoftwareVersion.latest]
69.31s call     test_update/update_flow_test.py::test_update_from_lts_succeeds[SoftwareVersion.lts]
67.18s call     test_update/update_flow_test.py::test_update_from_lts_succeeds[SoftwareVersion.latest]
59.23s setup    test_update/update_flow_test.py::test_update_from_lts_succeeds[SoftwareVersion.lts]
2.57s setup    test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.lts]
=== 5 passed, 2 deselected in 561.19s (0:09:21) ===

real    9m22,318s
```

### Results when running emulated, with sequential execution

```bash
$ time test-run-pytest --durations=8 -m update

=== slowest 8 durations ===
47.26s setup    test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.latest]
46.61s call     test_update/update_flow_test.py::test_update_from_lts_succeeds[SoftwareVersion.latest]
46.03s call     test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.latest]
45.80s call     test_update/update_flow_test.py::test_update_from_lts_succeeds[SoftwareVersion.lts]
45.42s call     test_update/update_flow_test.py::test_update_from_latest_succeeds[SoftwareVersion.latest]
44.75s call     test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.lts]
25.62s setup    test_update/update_flow_test.py::test_update_from_lts_succeeds[SoftwareVersion.lts]
25.24s setup    test_update/update_flow_test.py::test_update_from_latest_succeeds[SoftwareVersion.latest]
=== 5 passed, 2 deselected in 352.67s (0:05:52) ===

real    5m54.555s
```

### Results when running emulated, with parallel execution

```bash
$ time test-run-pytest -n auto --durations=5 -m update

8 workers [5 items]     

=== slowest 5 durations ===
86.72s call     test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.lts]
83.69s call     test_update/update_flow_test.py::test_update_from_lts_succeeds[SoftwareVersion.lts]
82.80s call     test_update/update_flow_test.py::test_update_from_lts_succeeds[SoftwareVersion.latest]
82.55s call     test_update/update_flow_test.py::test_update_from_latest_succeeds[SoftwareVersion.latest]
80.90s call     test_update/update_flow_test.py::test_update_from_manufacturing_succeeds[SoftwareVersion.latest]
=== 5 passed in 125.16s (0:02:05) ===

real    2m6.806s
```

