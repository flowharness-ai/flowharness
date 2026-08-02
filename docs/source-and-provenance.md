# Source and provenance

FlowHarness 0.1.2 Python source is distributed in six PyPI source distributions. The rows below
were selected from each release's authoritative PyPI JSON response as the sole artifact whose
`packagetype` is `sdist`. Every listed sdist is Apache-2.0.

| Distribution | sdist filename | Direct PyPI URL | SHA-256 | License |
| --- | --- | --- | --- | --- |
| flowharness | flowharness-0.1.2.tar.gz | https://files.pythonhosted.org/packages/23/f3/769098b150a9cb74fb0e821a5f43fc31d0fd3ef044604545b98c2f2eeb86/flowharness-0.1.2.tar.gz | 22aa011394c3724596b3cefadd79209254454befddc8c774b863beb3284c1b9a | Apache-2.0 |
| flowharness-ci-runner | flowharness_ci_runner-0.1.2.tar.gz | https://files.pythonhosted.org/packages/4a/91/be715d7b789d4137280e5925a0a0954d752bfbbe50228c677c6b9e5b7fcf/flowharness_ci_runner-0.1.2.tar.gz | 0dbe4cd4f9d033f3b90c558d104092755d16e485d01382dbc203c8ee10b9e862 | Apache-2.0 |
| flowharness-core | flowharness_core-0.1.2.tar.gz | https://files.pythonhosted.org/packages/f3/28/4ec191d523985d698ea2a31c0a19d0d6ec6b18839d7ba207aad7b0532660/flowharness_core-0.1.2.tar.gz | f9ae6640ea254e6df6905230470f70b027ec58b6d689a03afa96077d4bae5f8a | Apache-2.0 |
| flowharness-inspection | flowharness_inspection-0.1.2.tar.gz | https://files.pythonhosted.org/packages/76/72/da782bb1e4cb0af47a53a0701a0de0f20b3d5e7a73e447468798dbfcd99b/flowharness_inspection-0.1.2.tar.gz | 539bfafecda148a0b1f6db2a06d5d481e2b266333578abf4e64ece692ad29643 | Apache-2.0 |
| flowharness-evaluation | flowharness_evaluation-0.1.2.tar.gz | https://files.pythonhosted.org/packages/88/17/a02bb845fd543ab78443aba4c36cb5e61f9b8a50d505f8eeb5268d2fcfa4/flowharness_evaluation-0.1.2.tar.gz | 2c00ed71d360c25b5839ba048dc70e42bce2c2a6f40646980ea3c5884f914cf1 | Apache-2.0 |
| flowharness-portability | flowharness_portability-0.1.2.tar.gz | https://files.pythonhosted.org/packages/c7/b5/2c3c1734cc8322b488c5daa90ed0ee4e0a829fa8ab06d07fcf90145c6705/flowharness_portability-0.1.2.tar.gz | 9d83492d93730bb5cb37d2352d50a3d2a3b4d3ca818fe6fdff9af403d3877af2 | Apache-2.0 |

After downloading an artifact, compare its digest before inspection or build:

```console
shasum -a 256 flowharness-0.1.2.tar.gz
```

The result must exactly match the corresponding table value. A hash proves byte identity with the
artifact recorded here; review the source and apply your own release-trust policy before execution.

## What each public surface contains

- **Released Python source:** the six Apache-2.0 sdists above are the source artifacts for Python
  release 0.1.2. PyPI project pages and wheels are useful release surfaces, but this table pins the
  source-distribution bytes directly.
- **Public Action source:** the public
  [Scan Action repository](https://github.com/flowharness-ai/scan-action) and
  [Vibe Check Action repository](https://github.com/flowharness-ai/vibe-check-action) contain the
  browsable composite Action source. Their stable `v1` tags identify the supported Action line;
  security-sensitive consumers can pin the release commit SHA shown in each repository.
- **This public hub:** the hub contains product documentation, operational guides, examples, and
  entry points for the free tools. It is not a VCS source mirror and does not replace the sdists or
  the Action repositories as their source distribution points.
- **Commercial platform:** the organization-wide governance and evaluation control plane is a
  separate commercial product. Its implementation is not included in this hub, the public Action
  repositories, or these Python sdists. See
  [Organization-wide governance](organizational-platform.md) for the product boundary.

Published 0.1.2 metadata and artifacts are immutable. Documentation URL changes belong in a next
normal release rather than a rewritten 0.1.2 artifact.
