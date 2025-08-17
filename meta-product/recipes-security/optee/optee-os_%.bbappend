SRC_URI:remove = " \
    file://0001-optee-enable-clang-support.patch \
    file://0002-Add-optee-ta-instanceKeepCrashed.patch \
"

# --- START of build hacks ---
S = "${UNPACKDIR}/git"
# --- END of build hacks ---