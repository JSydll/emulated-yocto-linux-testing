# Extends the uki class with the ability to create (commandline) profiles.
#
inherit uki

UKI_PROFILES[doc] = ""
UKI_PROFILES ?= ""

UKIFY_BASE_CMD = "ukify build"
# As tasks are executed independently from each other, the new ukify command needs to be set on recipe level:
UKIFY_CMD = "${UKIFY_BASE_CMD} \
    ${@ ''.join([' --join-profile=%s/%s.efi' % (d.getVar('DEPLOY_DIR_IMAGE'), d.getVarFlag('UKI_PROFILE_%s' % profile, 'name') or profile) \
        for profile in d.getVar('UKI_PROFILES').split(' ')])}"

python do_uki_profiles() {
    import bb.process

    profiles = d.getVar('UKI_PROFILES')
    if not profiles:
        return

    target_arch = d.getVar('EFI_ARCH')
    deploy_dir_image = d.getVar('DEPLOY_DIR_IMAGE')
    build_cmd = "%s --efi-arch %s --stub='%s/addon%s.efi.stub'" % (d.getVar('UKIFY_BASE_CMD'), target_arch, deploy_dir_image, target_arch)

    for profile in profiles.split(' '):
        bb.debug(2, "Creating UKI profile '%s'..." % (profile))
        name = d.getVarFlag('UKI_PROFILE_%s' % profile, 'name') or profile
        meta = d.getVarFlag('UKI_PROFILE_%s' % profile, 'meta')
        cmdline = d.getVarFlag('UKI_PROFILE_%s' % profile, 'cmdline')
        if not meta or not cmdline:
            bb.error("Missing required varflag on UKI_PROFILE_%s!" % (profile))

        cmd =  "%s --profile='%s' --cmdline='%s' --output='%s/%s.efi'" % (build_cmd, meta, cmdline, deploy_dir_image, name)
        out, err = bb.process.run(cmd, shell=True)
        bb.debug(2, "%s\n%s" % (out, err))
    
    bb.debug(2, "ukify base command to generate UKI with set to: '%s'" % (d.getVar('UKIFY_CMD')))
}
addtask uki_profiles after do_rootfs before do_uki