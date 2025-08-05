do_deploy:append() {
    cp ${DEPLOYDIR}/lg-env-config.yml ${DEPLOYDIR}/lg-env-config-${RELEASE_TYPE}.yml
}