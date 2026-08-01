# Security policy

## Scope

This policy covers FlowHarness Scan, FlowHarness Vibe Check, the Scan and Vibe Check GitHub
Actions, and the released FlowHarness Python packages.

## Report a vulnerability privately

Submit a private report through
[GitHub Security Advisories](https://github.com/flowharness-ai/flowharness/security/advisories/new).
Include the affected package or Action version, impact, and the smallest safe reproduction you can
provide.

Do not open a public issue containing a vulnerability, credential, repository content, private
path, finding body, token, or secret. If a public issue already exists, do not add sensitive
details; move the report to the private advisory channel.

We will acknowledge the report, investigate affected released artifacts, and coordinate a fix and
disclosure when warranted. Please allow time for triage before publishing details.

## Operational precautions

- Treat `FLOWHARNESS_TOKEN` as a secret and scope it to the Vibe Check Action step.
- Prefer immutable commit-SHA pins for Actions when your supply-chain policy requires them.
- Use `pull_request`, not `pull_request_target`, for workflows that evaluate untrusted pull-request
  content.
- Remove secrets from agent-context files before sharing a report or reproduction.
