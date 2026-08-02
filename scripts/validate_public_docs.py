"""Fail-closed validation for the FlowHarness public documentation hub."""

from __future__ import annotations

import html
import re
import sys
from collections.abc import Mapping
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlsplit

import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "docs/getting-started.md",
    "docs/scan.md",
    "docs/vibe-check.md",
    "docs/findings-and-verdicts.md",
    "docs/adoption-and-baselines.md",
    "docs/privacy-permissions-and-tokens.md",
    "docs/troubleshooting.md",
    "docs/organizational-platform.md",
    "docs/source-and-provenance.md",
    "examples/scan.yml",
    "examples/vibe-check.yml",
    "scripts/validate_public_docs.py",
    "scripts/test_validate_public_docs.py",
)

CATEGORY = "The agent governance and evaluation control plane for organizations."
OPEN_CORE = (
    "FlowHarness is open-core. Its local tools and GitHub Actions are free and "
    "Apache-2.0. The organization-wide governance and evaluation control plane is a "
    "commercial product available as managed SaaS, on-premises, and air-gapped "
    "enterprise deployments."
)
VERSION_MATRIX_HEADER = (
    "Surface",
    "Released version",
    "Embedded Python artifact",
)
VERSION_MATRIX_SEPARATOR = ("---", "---", "---")
VERSION_MATRIX_ROWS = (
    ("Local CLI", "0.1.2", "flowharness 0.1.2"),
    ("Scan Action", "v1.0.1", "flowharness 0.1.2"),
    ("Vibe Check Action", "v1.0.1", "flowharness-ci-runner 0.1.1"),
)

SCAN_TOOL_SELECTION_MARKERS = (
    "Who: repository maintainers and reviewers.",
    "When: before merging a pull request that changes agent-context files.",
    "Why: detect deterministic static drift and risk before the change ships.",
)
SCAN_WALKTHROUGH_HEADING = "## Walkthrough: remediate a risky agent instruction"
SCAN_WALKTHROUGH_MARKERS = (
    "https://example.invalid/flowharness-scan-fixture",
    "injection_heuristics_check",
    "override, exfil, remote_exec",
    "QUARANTINE",
    "--format json",
)
VIBE_TOOL_SELECTION_MARKERS = (
    "Who: teams that own an agent's expected behavior.",
    "When: after changing prompts, rules, skills, tools, or other agent context.",
    "Why: replay committed cases to prove the intended behavior still holds.",
)
VIBE_WALKTHROUGH_HEADING = "## Walkthrough: correct a committed cassette failure"
VIBE_WALKTHROUGH_MARKERS = (
    "support-agent billing-dispute",
    "human escalation",
    "recorded candidate output",
    "offline replay",
)
VIBE_CASSETTE_SCHEMA_MARKERS = (
    '"schema": "flowharness/ci-case/v1"',
    '"recorded_output":',
    '"expected": {"contains":',
)
VIBE_CASSETTE_CORRECTION = (
    "The corrected committed cassette must record candidate output that includes the "
    "required human escalation before offline replay can pass."
)
VIBE_OFFLINE_BOUNDARY = (
    "The released Vibe Check replay evaluation is offline and uses no live model."
)

WORKFLOW_CONTRACTS = {
    "examples/scan.yml": {
        "action": "flowharness-ai/scan-action@v1",
        "inputs": frozenset({"directory", "fail-on"}),
        "permissions": {"contents": "read"},
        "env": frozenset(),
    },
    "examples/vibe-check.yml": {
        "action": "flowharness-ai/vibe-check-action@v1",
        "inputs": frozenset({"executor", "upload"}),
        "permissions": {"contents": "read", "pull-requests": "write"},
        "env": frozenset({"FLOWHARNESS_TOKEN", "FLOWHARNESS_API_URL"}),
    },
}

PROVENANCE = (
    (
        "flowharness",
        "flowharness-0.1.2.tar.gz",
        "https://files.pythonhosted.org/packages/23/f3/769098b150a9cb74fb0e821a5f43fc31d0fd3ef044604545b98c2f2eeb86/flowharness-0.1.2.tar.gz",
        "22aa011394c3724596b3cefadd79209254454befddc8c774b863beb3284c1b9a",
    ),
    (
        "flowharness-ci-runner",
        "flowharness_ci_runner-0.1.2.tar.gz",
        "https://files.pythonhosted.org/packages/4a/91/be715d7b789d4137280e5925a0a0954d752bfbbe50228c677c6b9e5b7fcf/flowharness_ci_runner-0.1.2.tar.gz",
        "0dbe4cd4f9d033f3b90c558d104092755d16e485d01382dbc203c8ee10b9e862",
    ),
    (
        "flowharness-core",
        "flowharness_core-0.1.2.tar.gz",
        "https://files.pythonhosted.org/packages/f3/28/4ec191d523985d698ea2a31c0a19d0d6ec6b18839d7ba207aad7b0532660/flowharness_core-0.1.2.tar.gz",
        "f9ae6640ea254e6df6905230470f70b027ec58b6d689a03afa96077d4bae5f8a",
    ),
    (
        "flowharness-inspection",
        "flowharness_inspection-0.1.2.tar.gz",
        "https://files.pythonhosted.org/packages/76/72/da782bb1e4cb0af47a53a0701a0de0f20b3d5e7a73e447468798dbfcd99b/flowharness_inspection-0.1.2.tar.gz",
        "539bfafecda148a0b1f6db2a06d5d481e2b266333578abf4e64ece692ad29643",
    ),
    (
        "flowharness-evaluation",
        "flowharness_evaluation-0.1.2.tar.gz",
        "https://files.pythonhosted.org/packages/88/17/a02bb845fd543ab78443aba4c36cb5e61f9b8a50d505f8eeb5268d2fcfa4/flowharness_evaluation-0.1.2.tar.gz",
        "2c00ed71d360c25b5839ba048dc70e42bce2c2a6f40646980ea3c5884f914cf1",
    ),
    (
        "flowharness-portability",
        "flowharness_portability-0.1.2.tar.gz",
        "https://files.pythonhosted.org/packages/c7/b5/2c3c1734cc8322b488c5daa90ed0ee4e0a829fa8ab06d07fcf90145c6705/flowharness_portability-0.1.2.tar.gz",
        "9d83492d93730bb5cb37d2352d50a3d2a3b4d3ca818fe6fdff9af403d3877af2",
    ),
)

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(\s*(<[^>]+>|[^)\s]+)")
ABSOLUTE_URL = re.compile(r"https?://[^\s<>()\[\]{}\"'`]+", re.IGNORECASE)
SENSITIVE_QUERY_KEYS = frozenset(
    {
        "repo",
        "repository",
        "path",
        "finding",
        "report",
        "report_body",
        "token",
        "secret",
    }
)
PLACEHOLDER_MARKER = re.compile(
    r"\b(?:TODO|TBD|FIXME|CHANGEME|INSERT[-_ ]HERE)\b|<40-hex-sha>",
    re.IGNORECASE,
)
RUNTIME_PROXY_CLAIM = re.compile(
    r"\b(?:(?:low[- ]latency|real[- ]time)\s+)?(?:LLM|runtime|inference)[- ]proxy\b",
    re.IGNORECASE,
)
STALE_B7_COPY = re.compile(
    r"\bB7\s+(?:has\s+not|hasn't|hasn’t|did\s+not)\s+prov(?:e|ed)\s+sticky comments?\b",
    re.IGNORECASE,
)
SOURCE_MIRROR_MENTION = re.compile(r"\bsource mirror\b", re.IGNORECASE)
NEGATED_SOURCE_MIRROR_PREFIX = re.compile(
    r"\bnot\s+(?:(?:a|the)\s+)?(?:complete\s+)?(?:VCS\s+)?$",
    re.IGNORECASE,
)
INTERNAL_ROOTS = frozenset({".git", ".ruff_cache"})
INTERNAL_FILES = frozenset({".claude/napkin.md"})
INTERNAL_SDD_METADATA = re.compile(
    r"^\.superpowers/sdd/(?:\.gitignore|[^/]+/(?:task-\d+-(?:brief|report)\.md|review-[0-9a-f]+\.\.[0-9a-f]+\.diff))$"
)


def _discover_repository_files(root: Path) -> tuple[str, ...]:
    files: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative_path = path.relative_to(root)
        relative_path_string = relative_path.as_posix()
        if (
            relative_path.parts[0] in INTERNAL_ROOTS
            or relative_path_string in INTERNAL_FILES
            or INTERNAL_SDD_METADATA.fullmatch(relative_path_string)
            or "__pycache__" in relative_path.parts
            or path.suffix == ".pyc"
        ):
            continue
        files.append(relative_path_string)
    return tuple(sorted(files))


def _load_public_text(
    root: Path, repository_files: tuple[str, ...], errors: list[str]
) -> dict[str, str]:
    texts: dict[str, str] = {}
    for relative_path in repository_files:
        if relative_path.startswith("scripts/"):
            continue
        try:
            texts[relative_path] = (root / relative_path).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"cannot read {relative_path} as UTF-8: {exc}")
    return texts


def _workflow_steps(
    document: Mapping[object, object], relative_path: str, errors: list[str]
) -> list[Mapping[object, object]]:
    jobs = document.get("jobs")
    if not isinstance(jobs, Mapping):
        errors.append(f"{relative_path} must define a jobs mapping")
        return []

    steps: list[Mapping[object, object]] = []
    for job in jobs.values():
        if not isinstance(job, Mapping):
            continue
        job_steps = job.get("steps")
        if not isinstance(job_steps, list):
            continue
        steps.extend(step for step in job_steps if isinstance(step, Mapping))
    if not steps:
        errors.append(f"{relative_path} must define workflow steps")
    return steps


def _validate_workflow(root: Path, relative_path: str, errors: list[str]) -> None:
    contract = WORKFLOW_CONTRACTS[relative_path]
    try:
        document = yaml.safe_load((root / relative_path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        errors.append(f"{relative_path} must parse with yaml.safe_load: {exc}")
        return

    if not isinstance(document, Mapping):
        errors.append(f"{relative_path} must parse to a YAML mapping")
        return

    if True in document:
        errors.append(
            f'{relative_path} must quote the literal string key "on"; boolean True is forbidden'
        )

    trigger = document.get("on")
    if "on" not in document:
        errors.append(f'{relative_path} must quote the literal string key "on"')
        trigger = document.get(True)

    if isinstance(trigger, (Mapping, list)):
        trigger_names = set(trigger)
    elif isinstance(trigger, str):
        trigger_names = {trigger}
    else:
        trigger_names = set()

    if "pull_request_target" in trigger_names:
        errors.append(f"{relative_path} must not use pull_request_target")
    if "pull_request" not in trigger_names:
        errors.append(f"{relative_path} must use pull_request")

    permissions = document.get("permissions")
    if permissions != contract["permissions"]:
        errors.append(
            f"{relative_path} permissions must be exactly {contract['permissions']}"
        )

    steps = _workflow_steps(document, relative_path, errors)
    expected_action = str(contract["action"])
    action_repository = expected_action.rsplit("@", maxsplit=1)[0]
    action_step = next(
        (step for step in steps if step.get("uses") == expected_action),
        None,
    )
    if action_step is None:
        errors.append(f"{relative_path} must use {expected_action}")
        return

    other_public_action_steps = [
        step
        for step in steps
        if isinstance(step.get("uses"), str)
        and str(step["uses"]).startswith(f"{action_repository}@")
        and step.get("uses") != expected_action
    ]
    if other_public_action_steps:
        errors.append(
            f"{relative_path} must not include another {action_repository} version"
        )

    inputs = action_step.get("with", {})
    input_names = frozenset(inputs) if isinstance(inputs, Mapping) else frozenset()
    if input_names != contract["inputs"]:
        errors.append(
            f"{relative_path} Action inputs must be exactly {sorted(contract['inputs'])}"
        )

    expected_env = contract["env"]
    if expected_env:
        environment = action_step.get("env", {})
        environment_names = (
            frozenset(environment) if isinstance(environment, Mapping) else frozenset()
        )
        for variable in sorted(expected_env):
            if variable not in environment_names:
                errors.append(f"{relative_path} action env must include {variable}")

        if "env" in document:
            errors.append(
                f"{relative_path} must scope FlowHarness credentials to the Action step"
            )
        jobs = document.get("jobs", {})
        if isinstance(jobs, Mapping) and any(
            isinstance(job, Mapping) and "env" in job for job in jobs.values()
        ):
            errors.append(
                f"{relative_path} must not put FlowHarness credentials in job env"
            )


def _validate_sensitive_query(relative_path: str, url: str, errors: list[str]) -> None:
    normalized_url = html.unescape(url).rstrip(".,;:")
    for query_key, _ in parse_qsl(
        urlsplit(normalized_url).query, keep_blank_values=True
    ):
        normalized_key = query_key.lower()
        if normalized_key in SENSITIVE_QUERY_KEYS:
            errors.append(
                f"{relative_path} URL contains sensitive query parameter: {normalized_key}"
            )


def _validate_markdown_links(
    root: Path, texts: Mapping[str, str], errors: list[str]
) -> None:
    resolved_root = root.resolve()
    for relative_path, text in texts.items():
        if not relative_path.endswith(".md"):
            continue
        source = root / relative_path
        for match in MARKDOWN_LINK.finditer(text):
            destination = match.group(1).strip("<>")
            if destination.startswith("#"):
                continue
            parsed = urlsplit(destination)
            if parsed.scheme or parsed.netloc:
                continue
            decoded_path = unquote(parsed.path)
            if not decoded_path:
                continue
            candidate = (
                resolved_root / decoded_path.lstrip("/")
                if decoded_path.startswith("/")
                else source.parent / decoded_path
            ).resolve()
            try:
                candidate.relative_to(resolved_root)
            except ValueError:
                errors.append(
                    f"{relative_path} relative Markdown link escapes repository: {destination}"
                )
                continue
            if not candidate.exists():
                errors.append(
                    f"{relative_path} has broken relative Markdown link: {destination}"
                )


def _markdown_cells(line: str) -> tuple[str, ...]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return ()
    return tuple(cell.strip() for cell in stripped.strip("|").split("|"))


def _validate_version_matrix(readme: str, errors: list[str]) -> None:
    lines = readme.splitlines()
    headings = [
        index for index, line in enumerate(lines) if line.strip() == "## Version matrix"
    ]
    if len(headings) != 1:
        errors.append("README.md must contain exactly one version matrix")
        return

    cursor = headings[0] + 1
    while cursor < len(lines) and not lines[cursor].strip():
        cursor += 1

    header = _markdown_cells(lines[cursor]) if cursor < len(lines) else ()
    if header != VERSION_MATRIX_HEADER:
        errors.append(
            f"README.md version matrix header must be exactly {VERSION_MATRIX_HEADER}"
        )
    cursor += 1

    separator = _markdown_cells(lines[cursor]) if cursor < len(lines) else ()
    if separator != VERSION_MATRIX_SEPARATOR:
        errors.append(
            "README.md version matrix must use the exact three-column separator"
        )
    cursor += 1

    rows: list[tuple[str, ...]] = []
    while cursor < len(lines):
        row = _markdown_cells(lines[cursor])
        if not row:
            break
        rows.append(row)
        cursor += 1

    parsed_rows = tuple(rows)
    if parsed_rows != VERSION_MATRIX_ROWS:
        errors.append(
            "README.md version matrix rows must be exactly the three supported surfaces"
        )
    if VERSION_MATRIX_ROWS[0] not in parsed_rows:
        errors.append("README.md version matrix must identify local CLI 0.1.2")
    if VERSION_MATRIX_ROWS[1] not in parsed_rows:
        errors.append(
            "README.md version matrix must identify Scan Action v1.0.1 with embedded 0.1.2"
        )
    if VERSION_MATRIX_ROWS[2] not in parsed_rows:
        errors.append(
            "README.md version matrix must identify Vibe Action v1.0.1 with embedded runner 0.1.1"
        )


def _validate_product_contract(texts: Mapping[str, str], errors: list[str]) -> None:
    readme = texts.get("README.md", "")
    normalized_readme = re.sub(r"\s+", " ", readme).strip()
    normalized_open_core = re.sub(r"\s+", " ", OPEN_CORE).strip()

    if CATEGORY not in normalized_readme:
        errors.append("README.md missing exact product category")
    if normalized_open_core not in normalized_readme:
        errors.append("README.md missing exact open-core boundary")
    for tool_name in ("FlowHarness Scan", "FlowHarness Vibe Check"):
        if tool_name not in readme:
            errors.append(f"README.md missing released tool: {tool_name}")
    if "docs/organizational-platform.md" not in readme:
        errors.append("README.md missing organizational-platform bridge")
    _validate_version_matrix(readme, errors)


def _validate_onboarding_contracts(
    texts: Mapping[str, str], errors: list[str]
) -> None:
    scan = texts.get("docs/scan.md", "")
    vibe_check = texts.get("docs/vibe-check.md", "")

    if not all(marker in scan for marker in SCAN_TOOL_SELECTION_MARKERS):
        errors.append("docs/scan.md missing Scan who/when/why contract")
    if SCAN_WALKTHROUGH_HEADING not in scan:
        errors.append("docs/scan.md missing Scan walkthrough")
    if not all(marker in scan for marker in SCAN_WALKTHROUGH_MARKERS):
        errors.append("docs/scan.md missing required Scan walkthrough content")
    if not all(marker in vibe_check for marker in VIBE_TOOL_SELECTION_MARKERS):
        errors.append("docs/vibe-check.md missing Vibe Check who/when/why contract")
    if VIBE_WALKTHROUGH_HEADING not in vibe_check:
        errors.append("docs/vibe-check.md missing Vibe Check walkthrough")
    if not all(marker in vibe_check for marker in VIBE_WALKTHROUGH_MARKERS):
        errors.append("docs/vibe-check.md missing required Vibe Check walkthrough content")
    if not all(marker in vibe_check for marker in VIBE_CASSETTE_SCHEMA_MARKERS):
        errors.append(
            "docs/vibe-check.md missing required Vibe Check cassette schema content"
        )
    if VIBE_CASSETTE_CORRECTION not in vibe_check:
        errors.append("docs/vibe-check.md missing exact committed-cassette correction")
    if VIBE_OFFLINE_BOUNDARY not in vibe_check:
        errors.append("docs/vibe-check.md missing exact offline/no-live-model boundary")


def _validate_provenance(texts: Mapping[str, str], errors: list[str]) -> None:
    relative_path = "docs/source-and-provenance.md"
    provenance = texts.get(relative_path, "")
    if "SHA-256" not in provenance:
        errors.append(f"{relative_path} must label SHA-256 provenance")
    for package, filename, url, digest in PROVENANCE:
        package_row = next(
            (
                line
                for line in provenance.splitlines()
                if re.search(rf"\|\s*{re.escape(package)}\s*\|", line)
            ),
            None,
        )
        if package_row is None:
            errors.append(f"{relative_path} missing distribution {package}")
            continue
        cells = [cell.strip() for cell in package_row.strip().strip("|").split("|")]
        if len(cells) < 4 or cells[1] != filename:
            errors.append(f"{relative_path} missing sdist filename for {package}")
        if len(cells) < 4 or cells[2] != url:
            errors.append(f"{relative_path} missing direct PyPI URL for {package}")
        if len(cells) < 4 or cells[3] != digest:
            errors.append(f"{relative_path} missing SHA-256 for {package}")


def _has_affirmative_source_mirror_claim(text: str) -> bool:
    for mention in SOURCE_MIRROR_MENTION.finditer(text):
        prefix = text[max(0, mention.start() - 80) : mention.start()]
        if not NEGATED_SOURCE_MIRROR_PREFIX.search(prefix):
            return True
    return False


def _validate_banned_content(texts: Mapping[str, str], errors: list[str]) -> None:
    for relative_path, text in texts.items():
        lowered = text.lower()
        if "github.com/suleimanmahmoud/flowharness" in lowered:
            errors.append(f"{relative_path} contains private monorepo URL")
        if "@flowharness/core" in lowered:
            errors.append(
                f"{relative_path} contains banned product claim: @flowharness/core"
            )
        if "<15ms" in lowered:
            errors.append(f"{relative_path} contains banned product claim: <15ms")
        if "soc 2 ready" in lowered:
            errors.append(f"{relative_path} contains banned product claim: SOC 2 Ready")
        if RUNTIME_PROXY_CLAIM.search(text):
            errors.append(
                f"{relative_path} contains banned product claim: runtime or LLM proxy"
            )
        if re.search(r"\blive interception\b", text, re.IGNORECASE):
            errors.append(
                f"{relative_path} contains banned product claim: live interception"
            )
        if STALE_B7_COPY.search(text):
            errors.append(f"{relative_path} contains stale B7-unproven copy")
        if PLACEHOLDER_MARKER.search(text):
            errors.append(f"{relative_path} contains placeholder marker")
        if _has_affirmative_source_mirror_claim(text):
            errors.append(
                f"{relative_path} must not call the public hub a source mirror"
            )

        for markdown_link in MARKDOWN_LINK.finditer(text):
            destination = markdown_link.group(1).strip("<>")
            _validate_sensitive_query(relative_path, destination, errors)
        for url_match in ABSOLUTE_URL.finditer(text):
            _validate_sensitive_query(relative_path, url_match.group(0), errors)


def validate_repository(root: Path = REPOSITORY_ROOT) -> list[str]:
    """Return every contract violation found under *root*."""

    repository_files = _discover_repository_files(root)
    repository_file_set = set(repository_files)
    required_file_set = set(REQUIRED_FILES)
    missing = [
        relative_path
        for relative_path in REQUIRED_FILES
        if relative_path not in repository_file_set
    ]
    unexpected = sorted(repository_file_set - required_file_set)

    errors = [f"missing required file: {relative_path}" for relative_path in missing]
    errors.extend(
        f"unexpected public file: {relative_path}" for relative_path in unexpected
    )
    texts = _load_public_text(root, repository_files, errors)
    _validate_banned_content(texts, errors)
    if missing:
        return list(dict.fromkeys(errors))

    for relative_path in WORKFLOW_CONTRACTS:
        _validate_workflow(root, relative_path, errors)
    _validate_markdown_links(root, texts, errors)
    _validate_product_contract(texts, errors)
    _validate_onboarding_contracts(texts, errors)
    _validate_provenance(texts, errors)
    return list(dict.fromkeys(errors))


def main() -> int:
    errors = validate_repository()
    if errors:
        print("Public documentation validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Public documentation validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
