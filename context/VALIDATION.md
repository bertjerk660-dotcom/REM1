# Validation Gates

A meaningful build should record applicable checks:
- extraction/decompilation completed correctly;
- expected files/assets exist;
- references resolve;
- scripts/code compile;
- transformations produced expected output;
- no unexpected missing resources;
- no new high-severity errors;
- game boots;
- target area/menu loads;
- imported feature is reachable;
- imported feature behaves correctly;
- saving/loading still works;
- progression is not obviously broken;
- previous regression tests still pass.

Feature-specific checks should be added as integrations become verifiable.
