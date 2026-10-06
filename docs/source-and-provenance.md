# Source and provenance

FlowHarness 0.3.0 Python source is distributed in six PyPI source distributions. The rows below
were selected from each release's authoritative PyPI JSON response as the sole artifact whose
`packagetype` is `sdist`. Every listed sdist is Apache-2.0.

| Distribution | sdist filename | Direct PyPI URL | SHA-256 | License |
| --- | --- | --- | --- | --- |
| flowharness | flowharness-0.3.0.tar.gz | https://files.pythonhosted.org/packages/88/65/1ba7a68c84d4b434a82b6df7e046611a22f53476c9db7f8d0ed6450284a6/flowharness-0.3.0.tar.gz | ba05d5927f29ad25a2d5cc340e987b4a1a7918c3df442bb44f009cb919c46a5d | Apache-2.0 |
| flowharness-ci-runner | flowharness_ci_runner-0.3.0.tar.gz | https://files.pythonhosted.org/packages/f2/1f/a021f27e8c23e27a222216f4489fe33e4b1d9841960794f48eaea0e28cbd/flowharness_ci_runner-0.3.0.tar.gz | 79f89c646a2e34343c1926a47979b6830d112abcb3fff709316aa5e61cd68604 | Apache-2.0 |
| flowharness-core | flowharness_core-0.3.0.tar.gz | https://files.pythonhosted.org/packages/70/f6/d6cb39c0f6344d7eba6ae3c9882f20c7f0359b4af2bb252b0a962fa09371/flowharness_core-0.3.0.tar.gz | cf04e0c594c0b4cdf9034e11909f4b09b01d988f17ed91dc25c13f564cfe0d5f | Apache-2.0 |
| flowharness-inspection | flowharness_inspection-0.3.0.tar.gz | https://files.pythonhosted.org/packages/88/20/2786a8ec9bec5b599c558b53dda3b4bed61e56240eb0515252c233a14fc5/flowharness_inspection-0.3.0.tar.gz | e23fe1f4e6b7f467f008c54434f9b7a766883a07ff91fd593ed340ff66f21829 | Apache-2.0 |
| flowharness-evaluation | flowharness_evaluation-0.3.0.tar.gz | https://files.pythonhosted.org/packages/20/06/5191f47cf9739145ccd6558ad59019ba16788c04c147aaf7f9bb421d8193/flowharness_evaluation-0.3.0.tar.gz | 488b22b72080f976fe5e9b4fa0d140230dccadd1bfec442cbe678eb8cceedf2b | Apache-2.0 |
| flowharness-portability | flowharness_portability-0.3.0.tar.gz | https://files.pythonhosted.org/packages/d3/2e/07a9f2d57e4ad0457ebf7634a56395a98a2807cbd402cfbf635ffbe88234/flowharness_portability-0.3.0.tar.gz | 20583b266aad2c6002d219e015d743c96c78172be16283bca878410cc8bf8086 | Apache-2.0 |

After downloading an artifact, compare its digest before inspection or build:

```console
shasum -a 256 flowharness-0.3.0.tar.gz
```

The result must exactly match the corresponding table value. A hash proves byte identity with the
artifact recorded here; review the source and apply your own release-trust policy before execution.

## What each public surface contains

- **Released Python source:** the six Apache-2.0 sdists above are the source artifacts for Python
  release 0.3.0. PyPI project pages and wheels are useful release surfaces, but this table pins the
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

Published metadata and artifacts are immutable. Documentation URL changes belong in a next normal
release rather than a rewritten artifact. Earlier releases, such as 0.1.2, stay available on PyPI
with their own hashes.
