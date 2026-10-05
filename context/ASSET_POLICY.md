# Asset and Source Preservation Policy

The repository should preserve everything needed to understand and reproduce the project while respecting redistribution constraints.

## Store directly
- project-authored source code;
- scripts and converters;
- configuration;
- documentation;
- manifests;
- mappings;
- patches/diffs where appropriate;
- reverse-engineering notes;
- validation reports;
- hashes and provenance metadata;
- build orchestration.

## Do not silently depend on local-only knowledge
If a build depends on a local proprietary asset, document enough provenance and transformation information to recreate that dependency from the user's own legally obtained copy.

## Large/generated artifacts
Generated builds may be retained outside ordinary Git history when size makes Git unsuitable, but their manifest, checksums, provenance and validation outcome must remain in GitHub.
