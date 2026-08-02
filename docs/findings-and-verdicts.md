# Findings and verdicts

FlowHarness Scan 0.1.2 produces two related answers: an Architectural Drift Index from 0 to 100
and a gate verdict. A higher index means more architectural drift; it is not a probability of
failure. The verdict answers whether the selected gate passed. Read both, then inspect the
findings that produced them.

For a detailed, machine-readable report, run:

```console
uvx --from flowharness==0.1.2 flowharness scan . --format json
```

Each finding identifies a check, severity, affected subject, evidence, and a suggested action when
one is available. Evidence is deliberately concise: use the subject and safe file location to
inspect the repository rather than treating the report as a replacement for review.

## Check families

The default 0.1.2 scan groups checks into two families:

- **Architectural drift** finds duplication, contradiction, divergence between equivalent agent
  surfaces, and orphaned context. These dimensions contribute to the index.
- **Risk and hygiene** checks attestation and integrity, unsafe or missing bounds, prompt-injection
  patterns, and possible leakage. These findings drive the default risk verdict and also
  contribute to the index.

Reader findings can also explain malformed, unreadable, or unsafe-path inputs. Do not dismiss one
as ordinary drift until the scanner has successfully read the intended surface.

Findings have `info`, `warn`, `error`, or `critical` severity. Severity expresses the scanner's
policy significance, while the index expresses accumulated drift. One important risk finding can
therefore produce a hard verdict even when the overall index is modest.

## Verdicts and process exits

| Scanner banner | Shared verdict | Exit | Required response |
| --- | --- | --- | --- |
| `CLEAR` | `PASS` | `0` | The configured gate passed. Keep the report as evidence and continue. |
| `REVIEW` | `NEEDS_HUMAN` | `1` | A person must inspect the finding and explicitly decide; never auto-approve it. |
| `QUARANTINE` | `FAIL` | `2` | Stop the change and remediate or make an explicit policy decision. |

These meanings apply when a report was actually produced. A scanner or local-output error can
also exit `1`, while invalid command-line usage can also exit `2`. FlowHarness Vibe Check also uses
`PASS=0`, `NEEDS_HUMAN=1`, and `FAIL=2`, and typed setup or input errors fail closed at exit `2`.
Never classify a bare process code: read stderr, confirm the expected report or banner exists, and
separate a domain verdict from an execution error.

The gate matters too. `--fail-on risk` uses the three-way risk verdict above. `--fail-on
"index>N"` compares the displayed index to a chosen threshold, and `--fail-on baseline` checks for
findings absent from a supplied committed baseline. Changing the output format does not change the
gate.

## Remediation workflow

1. Confirm the scan completed and record the exact command, version, gate, and report.
2. Start with `critical` and `error` findings, then review warnings. Locate the referenced agent
   rule, prompt, skill, tool definition, memory, or harness configuration.
3. Compare the evidence with repository intent. Remove contradictory or duplicated instructions,
   restore bounds and provenance, eliminate unsafe imports or leakage patterns, or deliberately
   consolidate the authoritative rule.
4. Rerun the same pinned command. Confirm the finding is gone and that the index and verdict moved
   for the expected reason.
5. If a finding represents reviewed existing debt, record that decision in a committed baseline;
   do not regenerate the baseline merely to make a new finding disappear.
6. For `NEEDS_HUMAN`, leave a durable review decision. For `FAIL`, keep the gate closed until the
   unsafe change is removed or an accountable owner changes policy through review.

Use [Adoption and baselines](adoption-and-baselines.md) to introduce enforcement without forcing a
repository-wide cleanup in its first pull request. See the [Scan guide](scan.md) for formats and
gate syntax.
