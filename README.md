# FlowHarness

The agent governance and evaluation control plane for organizations.

Govern the prompts, rules, skills, tools, and evaluations behind every AI agent—from proposed
change to signed release, fleet rollout, and audit evidence.

## The problem

Agent behavior is shaped by files spread across repositories and harnesses. Those files accumulate
contradictions, unsafe instructions, unreviewed imports, and evaluation drift. FlowHarness makes
that agent-context sprawl visible locally, then gives organizations a path to govern changes,
releases, rollout, and evidence across a fleet.

FlowHarness is not an agent runtime or an ordinary linter. The free tools combine deterministic
agent-context inspection with replay evaluation. The commercial platform connects those local
results to shared policy, human approval, distribution, observability, and audit evidence.

## Run a repository scan in 60 seconds

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run from a repository:

```console
uvx flowharness scan .
```

`uvx` may use the network to obtain the released package from PyPI. The scan itself is read-only,
zero-model, account-free, and makes no network calls.

## Read the result

A result such as:

```text
flowharness-scan: drift index 30/100 (drifting) - QUARANTINE (policy scoring/2)
```

has two parts: a 0–100 Architectural Drift Index and a risk verdict.

- `CLEAR` / `PASS` (exit `0`) means the configured gate passed.
- `REVIEW` / `NEEDS_HUMAN` (exit `1`) requires human review and must not be auto-approved. A
  scanner error can also exit `1`, so inspect stderr and the workflow log.
- `QUARANTINE` / `FAIL` (exit `2`) is a hard failure. Command-line usage errors can also exit `2`,
  so confirm that the report was produced before treating the code as a verdict.

See [Findings and verdicts](docs/findings-and-verdicts.md) for interpretation and remediation.

## Add Scan to pull requests

Copy this least-privilege workflow to `.github/workflows/flowharness-scan.yml`:

```yaml
name: FlowHarness Scan
"on":
  pull_request:
permissions:
  contents: read
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: flowharness-ai/scan-action@v1
        with:
          directory: .
          fail-on: risk
```

The reusable copy is [examples/scan.yml](examples/scan.yml). The public
[Scan Action repository](https://github.com/flowharness-ai/scan-action) contains its browsable
Action source.

## Tools available today

- **FlowHarness Scan** statically inspects agent-context surfaces, emits local, GitHub, JSON,
  badge, or SARIF output, and supports committed baselines. Read the [Scan guide](docs/scan.md) or
  the [flowharness 0.3.0 PyPI page](https://pypi.org/project/flowharness/0.3.0/).
- **FlowHarness Vibe Check** replays committed evaluation cases for an agent-context change,
  publishes the result to the step summary, and creates or updates one sticky comment on
  same-repository pull requests. Read the [Vibe Check guide](docs/vibe-check.md), browse the
  [Vibe Check Action source](https://github.com/flowharness-ai/vibe-check-action), or inspect the
  [flowharness-ci-runner 0.3.0 PyPI page](https://pypi.org/project/flowharness-ci-runner/0.3.0/).
  The Action can also run [NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector) on your
  agent skills and gate its findings in the same comment; see
  [Gate SkillSpector findings](docs/vibe-check.md#gate-skillspector-findings).

Start with the [Getting started guide](docs/getting-started.md).

## Choose the right tool

| If you need to… | Choose | Why |
| --- | --- | --- |
| Review a repository's agent-context files before merging a pull request | [FlowHarness Scan](docs/scan.md) | It deterministically finds static drift and risk without running an evaluation. |
| Prove an agent-context change preserves expected behavior | [FlowHarness Vibe Check](docs/vibe-check.md) | It replays committed cases and reports the result on the pull request. |

Run Scan first when the question is “what static repository risk changed?” Add Vibe Check when the
question is “does this change still behave as our committed cases expect?” They are complementary
signals, not interchangeable gates.

## Version matrix

| Surface | Released version | Embedded Python artifact |
| --- | --- | --- |
| Local CLI | 0.3.0 | flowharness 0.3.0 |
| Scan Action | v1.1.0 | flowharness 0.3.0 |
| Vibe Check Action | v1.1.0 | flowharness-ci-runner 0.3.0 |

Stable major Action tags are used in copy-paste workflows. Organizations that require immutable
supply-chain inputs can replace the major tag with the release commit SHA shown in the relevant
public Action repository.

## Open-core and source boundary

FlowHarness is open-core. Its local tools and GitHub Actions are free and Apache-2.0. The organization-wide governance and evaluation control plane is a commercial product available as managed SaaS, on-premises, and air-gapped enterprise deployments.

This public documentation and examples hub is not a VCS source mirror. It is also not the
commercial-platform implementation. The two public Action repositories contain browsable Action
source. The released Python source is Apache-2.0 source contained in the six PyPI 0.3.0 sdists.
See [Source and provenance](docs/source-and-provenance.md) for direct artifacts and hashes.

## From one repository to organizational governance

The free tools remain useful without an account. Teams generally need the commercial platform
when they must apply shared policy across repositories, require human sign-off, distribute signed
agent context, measure fleet convergence, centralize evaluation evidence, or deploy under managed
SaaS, on-premises, or air-gapped constraints.

Read [Organization-wide governance](docs/organizational-platform.md) or visit
[flowharness.ai](https://flowharness.ai/) to discuss a design-partner deployment.

## Deeper runbooks

- [Getting started](docs/getting-started.md)
- [FlowHarness Scan](docs/scan.md)
- [FlowHarness Vibe Check](docs/vibe-check.md)
- [Findings and verdicts](docs/findings-and-verdicts.md)
- [Adoption and baselines](docs/adoption-and-baselines.md)
- [Privacy, permissions, and tokens](docs/privacy-permissions-and-tokens.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Organization-wide governance](docs/organizational-platform.md)

## External acceptance

The public onboarding runbook is preserved in the archived
[external acceptance repository](https://github.com/flowharness-ai/public-docs-acceptance-20260801).
The evidence includes [pull request 1](https://github.com/flowharness-ai/public-docs-acceptance-20260801/pull/1),
the restored-green [Scan run 30749326003](https://github.com/flowharness-ai/public-docs-acceptance-20260801/actions/runs/30749326003),
the restored-green [Vibe Check run 30749326004](https://github.com/flowharness-ai/public-docs-acceptance-20260801/actions/runs/30749326004),
the single updated [sticky comment 5158062641](https://github.com/flowharness-ai/public-docs-acceptance-20260801/pull/1#issuecomment-5158062641),
and annotated tag
[`public-docs-accepted-2026-08-01`](https://github.com/flowharness-ai/public-docs-acceptance-20260801/releases/tag/public-docs-accepted-2026-08-01).

## Release and project policies

The six released Python distributions are
[flowharness](https://pypi.org/project/flowharness/0.3.0/),
[flowharness-ci-runner](https://pypi.org/project/flowharness-ci-runner/0.3.0/),
[flowharness-core](https://pypi.org/project/flowharness-core/0.3.0/),
[flowharness-inspection](https://pypi.org/project/flowharness-inspection/0.3.0/),
[flowharness-evaluation](https://pypi.org/project/flowharness-evaluation/0.3.0/), and
[flowharness-portability](https://pypi.org/project/flowharness-portability/0.3.0/).

This hub's documentation and examples are licensed under [Apache-2.0](LICENSE). Report security
issues through the private process in [SECURITY.md](SECURITY.md); do not disclose secrets in a
public issue.
