# Rationale for this layer

## Modifying the images under test

While you'd normally want to keep your images under test unmodified,
this demo requires a few adjustments to the reference configurations
for the sake of simplicity.

## Providing multiple software versions

For demonstrating the test of update permutations, we need some differing software versions to start from and to go to.
Therefore, three software variants (`latest`, `lts` and `manufacturing`) are artificially created that only differ in the 
deployed `/etc/buildinfo` file. To identify the produced artifacts in the deployment, they are suffixed with the respective
identifier.

In production, those software versions would of course only evolve over time, and you'd probably rather use some sort of branching strategy to maintain the variants.