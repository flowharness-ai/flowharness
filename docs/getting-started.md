# Getting started

FlowHarness Scan gives you a local read of the agent rules, prompts, skills, and related context in
a repository. You need [uv](https://docs.astral.sh/uv/getting-started/installation/) and a directory
to inspect; no FlowHarness account is required.

## Get a result in 60 seconds

From the repository root:

```console
uvx flowharness scan .
```

The first `uvx` invocation may connect to PyPI to obtain the package and its dependencies. Once
the tool starts, the default scan is deterministic, read-only, zero-model, and zero-network.

For an explicitly reproducible 0.1.2 invocation:

```console
uvx --from flowharness==0.1.2 flowharness scan .
```

A repository with material risk findings might print:

```text
flowharness-scan: drift index 30/100 (drifting) - QUARANTINE (policy scoring/1)
```

The index measures context drift. The word after the dash is the gate:

- `CLEAR` maps to `PASS` and exit `0`.
- `REVIEW` maps to `NEEDS_HUMAN` and exit `1`; a person must review the findings.
- `QUARANTINE` maps to `FAIL` and exit `2`; treat it as a hard gate.

Exit `1` can also indicate a scanner error, and exit `2` can also indicate invalid command usage.
Read stderr and confirm a report was emitted before interpreting either code as a verdict.

## Choose the right tool

| Need | Start with | What it answers |
| --- | --- | --- |
| A pull request changes agent rules, prompts, skills, or related files | [FlowHarness Scan](scan.md) | Whether deterministic static drift or risk needs remediation before merge. |
| A pull request changes how an agent should respond | [FlowHarness Vibe Check](vibe-check.md) | Whether committed replay cases still demonstrate the intended behavior. |

Use both when a behavior change also changes agent-context files: Scan is the static hygiene gate;
Vibe Check is the committed-behavior gate.

## Choose the next action

- Investigate or remediate a finding with [Findings and verdicts](findings-and-verdicts.md).
- Adopt existing debt without hiding new drift using a [committed baseline](scan.md#baseline-existing-debt).
- Add the least-privilege [Scan pull-request workflow](../examples/scan.yml).
- Seed replay evaluations and add [Vibe Check](vibe-check.md).
- Review [privacy, permissions, tokens, and network boundaries](privacy-permissions-and-tokens.md).
- If the need spans repositories, policies, approvals, or fleet evidence, read about the
  [organization-wide commercial platform](organizational-platform.md).
