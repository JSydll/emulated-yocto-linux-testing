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
`export BUILD_MACHINE=raspberrypi`before sourcing the `env-init`.

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