# Organization-wide governance

The free tools answer repository-level questions: what agent context exists, where it has drifted,
and whether a committed replay suite still passes. An organization needs a control plane when the
same decisions must be consistent, reviewable, distributable, and provable across repositories,
teams, runtimes, and deployment environments.

## Commercial target lifecycle · design partners

For commercial design-partner deployments, the target organizational lifecycle is:

```text
propose → evaluate → approve → release → distribute → observe → evidence
```

The design-partner scope is to evaluate a proposed prompt, rule, skill, tool definition, memory,
MCP definition, or harness configuration against policy and committed cases. Required people
approve exceptions and sensitive changes. Approved context can then become a signed release,
reach enrolled repositories and agent runtimes through governed distribution, be observed for
drift and evaluation regression, and leave durable evidence for later review.

FlowHarness sits above agent runtimes; it does not replace them. The commercial design-partner
scope includes translation and distribution so the same governed intent can reach Claude Code,
Cursor, Continue, OpenCode, `AGENTS.md`, and other surfaces while retaining provenance and
accountability.

## Who uses and buys it

- **AI and platform engineering** need a shared catalog, reproducible evaluation gates, release
  management, repository enrollment, and fleet convergence.
- **Security and governance** need policy enforcement, human sign-off, controlled distribution,
  drift visibility, and tamper-evident history.
- **Compliance and oversight** need reviewable evaluation runs, trace and change evidence,
  retained decisions, and defensible audit exports.
- **Engineering leadership** needs an organization-level view of coverage, staleness, quality,
  safety, cost, and regression trends without replacing each team's runtime.

## Commercial platform · design partners

The commercial platform connects local findings and evaluations to:

- governed catalogs and shared policy for prompts, rules, skills, tools, MCP definitions, memory,
  and harness configuration;
- proposal, evaluation, policy gate, accountable human sign-off, signed release, and rollout;
- translation and controlled distribution across repositories and agent runtimes;
- enrollment plus fleet-wide drift, staleness, coverage, and convergence visibility;
- longitudinal evaluation-run and trace signals for quality, safety, cost, and regression; and
- tamper-evident history, organizational oversight, and audit/compliance evidence.

These are organization-wide commercial capabilities, not additional modes unlocked inside a free
scan. A useful threshold is ownership: if one repository can decide and document its own policy,
the free tools may be sufficient. If many repositories need shared policy, approvals, signed
distribution, fleet evidence, or managed operation, the organizational platform is the appropriate
conversation.

## Deployment and open-core boundary

FlowHarness is open-core. Its local tools and GitHub Actions are free and Apache-2.0. The organization-wide governance and evaluation control plane is a commercial product available as managed SaaS, on-premises, and air-gapped enterprise deployments.

The same governance lifecycle is intended across those deployment models. The deployment choice
sets the operational and data boundary; it does not turn the commercial platform into part of the
public documentation hub or released Python source.

The current public tools are available without an account and remain useful on their own. The
commercial path is a design-partner conversation, not a self-service checkout or a claim that
every described integration is generally available. Bring a representative scan, repository
portfolio, required approval model, deployment constraints, and evidence needs to make that
conversation concrete.

[Talk to FlowHarness about an agent-governance design partnership](https://flowharness.ai/), or
continue with the free [adoption runbook](adoption-and-baselines.md).
