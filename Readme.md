# Emulated testing of Yocto-based projects using QEMU and Labgrid

To allow location-independent testing while still being closer to the target architecture,
this demo shows an end-to-end setup of a Yocto build, producing a `qemuarm` image that
is then used as a `Labgrid` target and tested using `PyTest`.

## Usage

Most of the environment is dockerized, so you should only need `Docker` and `bash`.

Simply source the `env-init` file and then execute, for example:

```bash
build-testimage
build-publish
test-run-pytest --lg-env local.yaml
```