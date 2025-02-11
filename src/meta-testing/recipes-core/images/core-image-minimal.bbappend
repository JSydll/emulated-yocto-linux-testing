# Inject an indicator of change into the image
inherit image-buildinfo

IMAGE_BUILDINFO_VARS:append = " SOFTWARE_VERSION"
