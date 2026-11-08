# Versioning

The kit follows [Semantic Versioning](https://semver.org/). Its public interface is `spec/` and the layout of
`workspace/`, because the engine reads the first and every workspace is built from the second.

| Change | Version |
| --- | --- |
| An ID kind, pattern or home changes; a gate's criteria tighten; a deliverable moves; a front-matter field or status changes meaning; a template file is renamed or moved | **major** |
| A new optional template section, a new skill or agent capability, a new trace rule at `warning` severity, a new target pack | **minor** |
| Wording, guidance comments, fixes that do not change what a workspace must contain | **patch** |

A workspace records the kit version it was created from in `modernizer.json`. The engine embeds exactly one kit
version and refuses a workspace whose kit major version is newer than its own; an older major version needs the
migration the release notes describe.

## Releasing

1. Update [CHANGELOG.md](../CHANGELOG.md) and [VERSION](../VERSION) on a `release/` branch.
2. Merge into `main` and tag `vX.Y.Z`.
3. The release workflow publishes `kit-vX.Y.Z.zip` and `SHA256SUMS`.
4. Point the engine's `kit` submodule at the tag in a pull request; the engine's CI runs its tests against the new kit.
