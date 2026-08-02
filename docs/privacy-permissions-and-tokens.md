# Privacy, permissions, and tokens

FlowHarness separates package acquisition, local judgment, GitHub presentation, and optional
platform upload. Review each boundary independently.

## Network boundaries

`uvx` can contact PyPI and package hosts to download a requested release and its dependencies.
GitHub Actions can also contact their declared Action and tool sources during job setup. That is
installation traffic, before the scanner starts.

The default FlowHarness Scan 0.1.2 execution is deterministic, read-only, zero-model,
account-free, and makes no network calls. FlowHarness Vibe Check's `replay` executor is also local
and offline once its released packages and committed cases are present. Neither statement means
that `uvx` package resolution is offline.

Explicit output options can write a report, shell redirection can create a baseline, and the
developer `init` and `seed` commands intentionally create setup files. Those are opt-in operations;
an ordinary scan does not modify the inspected tree. Uploading SARIF to another service or
enabling signed platform upload introduces a separate network and data-handling decision.

## Least-privilege GitHub workflows

The [Scan workflow](../examples/scan.yml) needs only:

```yaml
permissions:
  contents: read
```

The [Vibe Check workflow](../examples/vibe-check.yml) reads the checkout and writes a same-repository
pull-request comment, so its permissions are exactly:

```yaml
permissions:
  contents: read
  pull-requests: write
```

Both use the `pull_request` trigger. Do not switch to `pull_request_target` to obtain secrets or
write access while evaluating untrusted pull-request content.

## `github.token` is not `FLOWHARNESS_TOKEN`

GitHub supplies `${{ github.token }}` to the workflow run. Vibe Check scopes it to the sticky
comment step as `GH_TOKEN`; it authorizes only the GitHub API operation allowed by
`pull-requests: write`. It is not a FlowHarness account credential, is not used by the Python
evaluator, and is not sent to the FlowHarness platform.

`FLOWHARNESS_TOKEN` is an optional FlowHarness platform signing key. It is needed only when signed
upload is explicitly enabled. `FLOWHARNESS_API_URL` names the instance's HTTPS base URL; the client
appends `/v1/evaluation/runs`. Keep both values on the invoking Action step:

```yaml
with:
  executor: replay
  upload: ${{ secrets.FLOWHARNESS_TOKEN != '' }}
env:
  FLOWHARNESS_TOKEN: ${{ secrets.FLOWHARNESS_TOKEN }}
  FLOWHARNESS_API_URL: ${{ vars.FLOWHARNESS_API_URL }}
```

Do not place either value in `with`, workflow-wide `env`, or job-wide `env`. A composite Action's
child processes inherit the invoking step environment, so step scope reduces exposure but does not
remove the need to review the public Action source. Upload success, failure, or absence never
changes the local replay verdict.

## Fork pull requests degrade safely

GitHub normally withholds repository secrets and write permission from fork pull requests. Vibe
Check therefore skips the sticky comment, emits a fixed notice, keeps the full report in the step
summary, and propagates the local replay verdict. Optional platform upload remains disabled when
the secret is absent. The workflow does not elevate privileges to compensate.

## Reports and acquisition links

Reports, annotations, SARIF, and step summaries can contain finding text and safe repository
locations needed for remediation. Treat those artifacts according to repository sensitivity and
review their destination before uploading or sharing them.

Current released Action branding uses fixed legacy root routes with first-party UTM values:
`/?utm_source=github&utm_medium=step_summary&utm_campaign=scan` and
`/?utm_source=github&utm_medium=pr_comment&utm_campaign=vibe_check`. The website keeps those routes
useful. New emitters use the stable contextual routes `/go/scan` and `/go/vibe-check`.

Both route families must remain privacy-safe: they must not encode repository names, owners,
branches, paths, findings, report bodies or hashes, tokens, secrets, or checkout-controlled
campaign values. FlowHarness does not construct a paid dashboard URL from checkout metadata. A
result-specific dashboard link is safe to display only when an authenticated platform response
returns a trusted, tenant-scoped URL.

For vulnerability reports, follow the private channel in [SECURITY.md](../SECURITY.md) and remove
credentials or sensitive repository content from reproductions.
