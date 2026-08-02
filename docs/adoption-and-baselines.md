# Adoption and baselines

Adopt FlowHarness in stages. The goal is to expose risk immediately, stop new debt, and make
existing debt smaller through reviewed changes—not to turn the first scan into an unplanned
repository migration.

## 1. Observe before enforcing

Run the pinned scanner locally and share the report with the people who own agent behavior:

```console
uvx --from flowharness==0.1.2 flowharness scan . --format json \
  --output flowharness-report.json
```

Review which surfaces were discovered, confirm that critical and error findings are understood,
and assign owners. If you add the Scan Action during this phase, do not make its check required
until the team has reviewed the current result. A temporary `index>100` threshold is observe-only
because the index is bounded at 100; remove that threshold when enforcement starts. Scanner errors
still need investigation.

## 2. Commit a reviewed baseline

A baseline accepts the identity of current findings without declaring them harmless. Generate it
from a trusted, reviewed commit:

```console
uvx --from flowharness==0.1.2 flowharness scan . --set-baseline \
  > .flowharness-baseline.json
git add .flowharness-baseline.json
git commit -m "chore: record FlowHarness baseline"
```

Inspect the JSON before committing it. The shell redirection creates the file; the scanner remains
read-only. Baseline changes deserve the same review as policy changes because they redefine which
debt is accepted.

## 3. Gate only new debt

Use the committed record to reject findings not present in the baseline:

```console
uvx --from flowharness==0.1.2 flowharness scan . \
  --baseline .flowharness-baseline.json --fail-on baseline
```

This is the useful first required gate for a repository with existing findings: unchanged accepted
debt passes, while a newly introduced finding exits `2`. Run this pinned CLI form in CI when using
a baseline. Scan Action v1 currently exposes only `directory` and `fail-on`, not a baseline-path
input, so setting its `fail-on` input to `baseline` alone is incomplete.

Do not automatically regenerate the file on every branch or after a failed run. When remediation
removes accepted findings, regenerate from the cleaned trusted state, review the smaller baseline,
and commit that change deliberately.

## 4. Tighten the gate

Track the index and severity mix over time. A single `--fail-on` invocation selects one gate, so
an index or risk gate does not preserve the baseline gate's “no new findings” guarantee. As owners
remove debt:

1. keep the baseline command as a required new-debt check and shrink its committed record so
   resolved findings cannot return unnoticed;
2. optionally add a separate `--fail-on "index>N"` check with a reviewed, progressively lower
   ceiling;
3. add a separate `--fail-on risk` check when the standard three-way risk verdict should gate the
   repository; and
4. make each selected CI check required only after its error paths and ownership are understood.

Replacing the baseline check with either alternative permits some new findings that stay below
that alternative's threshold. Make that coverage tradeoff explicit if policy calls for replacement
rather than complementary checks.

Treat `NEEDS_HUMAN` as a real hold with an accountable reviewer. Do not translate exit `1` into an
automatic approval.

## 5. Add replay evaluation

Once static inspection is stable, add FlowHarness Vibe Check for behavior that needs committed
examples. Initialize configuration, seed the replay suite, and review every generated artifact:

```console
uvx --no-config --no-sources --from flowharness==0.1.2 \
  flowharness init --dir . --hook none --workflow none
uvx --no-config --no-sources --from flowharness-ci-runner==0.1.2 \
  flowharness-ci seed
```

Commit `.flowharness/cases/`, `.flowharness/suite.lock.json`,
`.flowharness/gate-policy.toml`, and the FlowHarness configuration before enabling the
[Vibe Check workflow](../examples/vibe-check.yml). The starter policy intentionally requires human
judgment until the team selects explicit thresholds. Keep Scan and Vibe Check as separate signals:
static context hygiene and replay behavior answer different questions.

Fleet-wide policy, baseline ownership, approvals, rollout, and longitudinal evidence are the
bridge to the [commercial organizational platform](organizational-platform.md); the local tools
remain useful without an account.
