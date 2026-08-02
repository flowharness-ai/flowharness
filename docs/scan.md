# FlowHarness Scan

FlowHarness Scan 0.1.2 deterministically inspects a repository's agent-context surfaces. The
scanner is read-only, uses no model, makes no network calls, and requires no account. `uvx` may
still connect to PyPI before the scan to obtain the released package.

Use the pinned form below when you need to reproduce 0.1.2 behavior:

```console
uvx --from flowharness==0.1.2 flowharness scan .
```

## Choose Scan for static repository hygiene

Who: repository maintainers and reviewers.
When: before merging a pull request that changes agent-context files.
Why: detect deterministic static drift and risk before the change ships.

Use Scan for the repository-level question: “what static context or policy risk did this change
introduce?” Use [Vibe Check](vibe-check.md) instead when the question is whether a committed set of
agent interactions still produces the intended behavior.

## Walkthrough: remediate a risky agent instruction

A pull request changes `AGENTS.md` with an instruction telling an agent to copy values from `.env`
into a public issue. Before merge, a reviewer runs the pinned Scan command and receives a risk
finding with a hard gate. Treat the finding as a review prompt, inspect the cited file, and replace
the instruction with the safe rule: never copy credentials or environment values into an issue;
ask a maintainer for a redacted reproduction instead.

Rerun the same pinned command after the correction. Confirm that the finding is gone and that the
new report and verdict match the reviewed change; do not create a baseline merely to hide the new
finding. In the pull request, the [Scan workflow](../examples/scan.yml) needs only `contents: read`:
it reports annotations and a step summary without writing to the pull request. The reviewer can
then approve the least-privilege workflow outcome with the corrected instruction and fresh report.

## Output formats

`--format` accepts five values:

| Format | Purpose |
| --- | --- |
| `banner` | One-line index and verdict; the default. |
| `json` | The content-addressed `inspection/v1` report. |
| `badge` | An SVG badge suitable for a README. |
| `github` | GitHub annotations and, when available, a step-summary block. |
| `sarif` | A canonical SARIF 2.1.0 log. |

`--json` and `--badge` are aliases for their corresponding formats. Add `--output PATH` to write
the selected bytes atomically to a file instead of stdout.

```console
uvx --from flowharness==0.1.2 flowharness scan . --format json --output flowharness-report.json
uvx --from flowharness==0.1.2 flowharness scan . --format badge --output flowharness-badge.svg
```

The selected format does not change the exit gate.

## Exit codes and fail-on modes

With the default `--fail-on risk`, the domain verdict determines the exit code:

| Exit | Verdict | Meaning |
| --- | --- | --- |
| `0` | `CLEAR` / `PASS` | The configured gate passed. |
| `1` | `REVIEW` / `NEEDS_HUMAN` | Human review is required; never auto-approve it. |
| `2` | `QUARANTINE` / `FAIL` | Hard failure. |

There are two adapter caveats: a scanner or local-output error can also exit `1`, and argparse
usage errors also exit `2`. Check stderr and the report rather than classifying a bare process code
as a verdict.

Choose a gate with `--fail-on`:

```console
uvx --from flowharness==0.1.2 flowharness scan . --fail-on risk
uvx --from flowharness==0.1.2 flowharness scan . --fail-on "index>40"
uvx --from flowharness==0.1.2 flowharness scan . \
  --baseline .flowharness-baseline.json --fail-on baseline
```

- `risk` preserves the three risk verdict exits above and is the default.
- `index>N` exits `2` only when the displayed index is strictly greater than `N`; otherwise it
  exits `0`.
- `baseline` exits `2` only when the scan introduces findings absent from the supplied baseline;
  otherwise it exits `0`. It requires `--baseline FILE`.

## Baseline existing debt

Create a baseline from a reviewed repository state, inspect the generated JSON, and commit it:

```console
uvx --from flowharness==0.1.2 flowharness scan . --set-baseline > .flowharness-baseline.json
git add .flowharness-baseline.json
git commit -m "chore: record FlowHarness baseline"
```

Then gate only newly introduced findings:

```console
uvx --from flowharness==0.1.2 flowharness scan . \
  --baseline .flowharness-baseline.json --fail-on baseline
```

`--set-baseline` prints the record to stdout; the scanner does not write into the project tree.
Regenerate and review the baseline deliberately when accepted debt changes.

## Scan pull requests

The [copy-paste workflow](../examples/scan.yml) uses
[`flowharness-ai/scan-action@v1`](https://github.com/flowharness-ai/scan-action) with only
`contents: read`. Its supported inputs are `directory` and `fail-on`. The current `v1` release is
Scan Action 1.0.1 and embeds `flowharness` 0.1.2.

The Action emits GitHub annotations, appends a verdict to the step summary, and propagates the
captured exit code. The same scanner-error and usage-error caveats apply to codes `1` and `2`.

## Export SARIF

Create a SARIF artifact without changing the gate:

```console
uvx --from flowharness==0.1.2 flowharness scan . \
  --format sarif --output flowharness.sarif --fail-on risk
```

SARIF contains file locations only when a finding has a safe physical location. An empty finding
set remains a valid SARIF log. Uploading that file to another service is a separate network and
data-handling decision; review [privacy and tokens](privacy-permissions-and-tokens.md) first.
