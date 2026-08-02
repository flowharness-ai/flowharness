# Troubleshooting

Start by pinning the released distribution, confirming the working directory, and reading stderr.
A process exit alone is not enough to distinguish a verdict from a setup error.

## `uvx` resolves the wrong command or package

Use the distribution name after `--from` and the console-script name after it:

```console
uvx --no-config --no-sources --refresh --from flowharness==0.1.2 \
  flowharness --help
uvx --no-config --no-sources --refresh --from flowharness-ci-runner==0.1.2 \
  flowharness-ci --help
```

`flowharness-ci-runner` is the distribution; `flowharness-ci` is its executable. `--refresh`
forces a fresh resolution, while `--no-config --no-sources` ignores persistent uv configuration
and alternate sources. If acquisition fails, verify network access to PyPI and package hosts,
then retry the pinned form. Do not diagnose package-install traffic as scanner egress.

Version output can differ between the Action and local commands: Vibe Check Action v1.0.1 embeds
`flowharness-ci-runner` 0.1.1, while this hub's developer commands exercise the separately released
0.1.2 runner. The [version matrix](../README.md#version-matrix) records that boundary.

## Vibe Check cannot find a merge base

Replay compares the current change with `--base` (the Action defaults to `origin/main`). A shallow
checkout or absent base ref fails closed. In Actions, keep full history:

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0
```

Locally, fetch the intended base ref and confirm that `git merge-base <base> HEAD` succeeds. Then
pass that exact ref with `--base`. Also confirm that the command is running inside the intended Git
repository.

## The replay suite or gate policy is absent

When an AI or governance surface changed and replay is required, Vibe Check expects the committed
`.flowharness/suite.lock.json` and every case it references. An absent, unreadable, or malformed
suite then fails closed with an `error:` line and exit `2`. Run the developer seeder, inspect its
diff, and commit the real files:

```console
uvx --no-config --no-sources --from flowharness-ci-runner==0.1.2 \
  flowharness-ci seed
```

An absent `.flowharness/gate-policy.toml` is different: when replay is required, the runner uses
the safe default and returns `NEEDS_HUMAN` rather than silently passing an unconfigured evaluation.
A malformed or unreadable policy fails closed. Review the seeded starter policy, choose thresholds
explicitly, and commit it.

If no AI or governance surface changed and no external findings were supplied, the no-change fast
path prints `no AI-surface changes` and exits `0` before loading either file. Confirm the detected
change scope before interpreting a pass as evidence that the suite and policy were read.

## Exit `1` or `2` is ambiguous

For Scan, exit `1` can be either `REVIEW` / `NEEDS_HUMAN` or a scanner/output error. Exit `2` can
be either `QUARANTINE` / `FAIL` or invalid CLI usage. For Vibe Check, typed git, suite, policy,
case, or other input errors also return the fail-closed exit `2`.

Look for the expected banner, JSON, table, or GitHub report. If it is absent and stderr contains
`error:` or argparse usage, fix execution first. Never auto-approve exit `1`, and never report a
domain failure from an exit code without confirming the report.

## The sticky comment is missing

The local replay report and verdict remain authoritative. First check the job's step summary. On a
same-repository pull request, confirm that the workflow grants `pull-requests: write`, that GitHub
Actions can supply `${{ github.token }}`, and that repository policy allows the write. Comment
posting is deliberately non-fatal, so an API or permission failure leaves the report in the step
summary without changing the gate.

Fork pull requests intentionally do not receive a sticky comment: secrets and the needed write
token are unavailable. The Action emits a fixed fork notice, retains the full step-summary report,
and propagates the replay verdict. Do not use `pull_request_target` as a workaround.

## SARIF has fewer locations than the full report

SARIF includes a physical location only when a finding has a safe file anchor. Anchorless
findings, unsafe locations, and overflow can remain visible in other report formats without a
fabricated SARIF location. An empty finding set is still a valid SARIF 2.1.0 log.

Compare `--format json` with `--format sarif` before assuming a finding was lost. Uploading the
SARIF file is a separate network operation; apply the guidance in
[Privacy, permissions, and tokens](privacy-permissions-and-tokens.md).
