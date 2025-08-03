# Reconfigure EDK2 to only build the UEFI shell.

# Machine overrides are required here as the defaults for the machine would override any change of the base variables.
EDK2_PLATFORM:qemuarm64     = "Shell"
EDK2_PLATFORM_DSC:qemuarm64 = " ShellPkg/ShellPkg.dsc"
EDK2_BIN_NAME:qemuarm64     = "Shell.efi"

EDK2_BUILD_ARTIFACTS_DIR    = "Build/${EDK2_PLATFORM}/${EDK2_BUILD_MODE}_${EDK_COMPILER}"

# There are two configurations of the shell in the EDK2 tree, identified by GUIDs:
# - a general shell, specified in ShellPkg/Application/Shell/Shell.inf
GENERAL_SHELL_GUID = "7C04A583-9E3E-4f1c-AD65-E05268D0B4D1"
# - an extended shell, specified in ShellPkg/ShellPkg.dsc
FULL_SHELL_GUID    = "EA4BB293-2D7F-4456-A681-1F22F42CD0BC"
# We use the extended shell for now.

# The do install task expects a file with EDK2_BIN_NAME in a specific directory, so we manually provide it there.
do_install:prepend:qemuarm64() {
    install -d ${B}/${EDK2_BUILD_ARTIFACTS_DIR}/FV
    cp ${B}/${EDK2_BUILD_ARTIFACTS_DIR}/${EDK2_ARCH}/Shell_${FULL_SHELL_GUID}.efi ${B}/${EDK2_BUILD_ARTIFACTS_DIR}/FV/Shell.efi
}

do_deploy:append:qemuarm64(){
    mv ${DEPLOYDIR}/uefi.bin ${DEPLOYDIR}/shell.efi
}