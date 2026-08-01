"""Mutation tests for the fail-closed public documentation validator."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CATEGORY = "The agent governance and evaluation control plane for organizations."
OPEN_CORE = (
    "FlowHarness is open-core. Its local tools and GitHub Actions are free and "
    "Apache-2.0. The organization-wide governance and evaluation control plane is a "
    "commercial product available as managed SaaS, on-premises, and air-gapped "
    "enterprise deployments."
)
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

SCAN_WORKFLOW = """name: FlowHarness Scan
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
          fail-on: high
"""

VIBE_WORKFLOW = """name: FlowHarness Vibe Check
"on":
  pull_request:
permissions:
  contents: read
  pull-requests: write
jobs:
  vibe-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: flowharness-ai/vibe-check-action@v1
        with:
          executor: replay
          upload: ${{ secrets.FLOWHARNESS_TOKEN != '' }}
        env:
          FLOWHARNESS_TOKEN: ${{ secrets.FLOWHARNESS_TOKEN }}
          FLOWHARNESS_API_URL: ${{ vars.FLOWHARNESS_API_URL }}
"""


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _populate_valid_public_hub(root: Path) -> None:
    readme = f"""# FlowHarness

{CATEGORY}

{OPEN_CORE}

Available today: FlowHarness Scan and FlowHarness Vibe Check.

See the [organizational platform](docs/organizational-platform.md).

This public documentation and examples hub is not a VCS source mirror. Public Action
repositories contain Action source; released Python source is in the Apache-2.0 sdists.

## Version matrix

| Surface | Released version | Embedded Python artifact |
| --- | --- | --- |
| Local CLI | 0.1.2 | flowharness 0.1.2 |
| Scan Action | v1.0.1 | flowharness 0.1.2 |
| Vibe Check Action | v1.0.1 | flowharness-ci-runner 0.1.1 |
"""
    _write(root / "README.md", readme)
    _write(
        root / "LICENSE", "Apache License 2.0 for this documentation and examples.\n"
    )
    _write(root / "SECURITY.md", "# Security\n\nReport vulnerabilities privately.\n")

    docs = {
        "getting-started.md": "# Getting started\n",
        "scan.md": "# FlowHarness Scan\n",
        "vibe-check.md": "# FlowHarness Vibe Check\n",
        "findings-and-verdicts.md": "# Findings and verdicts\n",
        "adoption-and-baselines.md": "# Adoption and baselines\n",
        "privacy-permissions-and-tokens.md": "# Privacy, permissions, and tokens\n",
        "troubleshooting.md": "# Troubleshooting\n",
        "organizational-platform.md": "# Organization-wide commercial platform\n",
    }
    for name, body in docs.items():
        _write(root / "docs" / name, body)

    rows = [
        "# Source and provenance",
        "",
        "Each released distribution is Apache-2.0 source from PyPI. SHA-256 values:",
        "",
        "| Distribution | sdist | Direct PyPI URL | SHA-256 |",
        "| --- | --- | --- | --- |",
    ]
    rows.extend(
        f"| {package} | {filename} | {url} | {digest} |"
        for package, filename, url, digest in PROVENANCE
    )
    _write(root / "docs" / "source-and-provenance.md", "\n".join(rows) + "\n")
    _write(root / "examples" / "scan.yml", SCAN_WORKFLOW)
    _write(root / "examples" / "vibe-check.yml", VIBE_WORKFLOW)


class PublicDocsValidatorTests(unittest.TestCase):
    """Each test changes one valid public-hub condition."""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name) / "flowharness"
        shutil.copytree(
            REPOSITORY_ROOT,
            self.root,
            ignore=shutil.ignore_patterns(".git", ".claude", "__pycache__"),
        )
        _populate_valid_public_hub(self.root)

    def run_validator(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.root / "scripts" / "validate_public_docs.py")],
            cwd=self.root,
            check=False,
            capture_output=True,
            text=True,
        )

    def assert_rejected(self, diagnostic: str) -> None:
        result = self.run_validator()
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn(diagnostic, output)

    def replace_once(self, relative_path: str, old: str, new: str) -> None:
        path = self.root / relative_path
        content = path.read_text(encoding="utf-8")
        self.assertEqual(
            content.count(old), 1, f"mutation source is not unique: {old!r}"
        )
        path.write_text(content.replace(old, new, 1), encoding="utf-8")

    def append(self, relative_path: str, text: str) -> None:
        path = self.root / relative_path
        path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")

    def test_accepts_complete_public_hub(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_unexpected_public_file(self) -> None:
        _write(self.root / "docs" / "unexpected.md", "# Unexpected public page\n")
        self.assert_rejected("unexpected public file: docs/unexpected.md")

    def test_scans_unexpected_public_file_for_private_content(self) -> None:
        _write(
            self.root / "docs" / "unexpected.md",
            "https://github.com/suleimanmahmoud/flowharness\n",
        )
        self.assert_rejected("docs/unexpected.md contains private monorepo URL")

    def test_scans_unexpected_public_file_for_banned_content(self) -> None:
        _write(self.root / "docs" / "unexpected.md", "SOC 2 Ready\n")
        self.assert_rejected(
            "docs/unexpected.md contains banned product claim: SOC 2 Ready"
        )

    def test_scans_unexpected_public_file_for_sensitive_url(self) -> None:
        _write(
            self.root / "docs" / "unexpected.md",
            "https://flowharness.ai/go/scan?secret=value\n",
        )
        self.assert_rejected(
            "docs/unexpected.md URL contains sensitive query parameter: secret"
        )

    def test_scans_unexpected_public_file_for_relative_sensitive_url(self) -> None:
        _write(self.root / "docs" / "unexpected.md", "[Leak](?secret=value)\n")
        self.assert_rejected(
            "docs/unexpected.md URL contains sensitive query parameter: secret"
        )

    def test_rejects_unexpected_file_beside_internal_napkin(self) -> None:
        _write(self.root / ".claude" / "public.md", "SOC 2 Ready\n")
        result = self.run_validator()
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn("unexpected public file: .claude/public.md", output)
        self.assertIn(
            ".claude/public.md contains banned product claim: SOC 2 Ready", output
        )

    def test_rejects_missing_trigger(self) -> None:
        self.replace_once("examples/scan.yml", "  pull_request:\n", "  push:\n")
        self.assert_rejected("examples/scan.yml must use pull_request")

    def test_rejects_boolean_on_key(self) -> None:
        self.replace_once("examples/scan.yml", '"on":\n', "on:\n")
        self.assert_rejected('examples/scan.yml must quote the literal string key "on"')

    def test_rejects_pull_request_target(self) -> None:
        self.replace_once(
            "examples/scan.yml", "  pull_request:\n", "  pull_request_target:\n"
        )
        self.assert_rejected("examples/scan.yml must not use pull_request_target")

    def test_rejects_excessive_permissions(self) -> None:
        self.replace_once(
            "examples/scan.yml",
            "  contents: read\n",
            "  contents: read\n  issues: write\n",
        )
        self.assert_rejected("examples/scan.yml permissions must be exactly")

    def test_rejects_pull_request_write_permission_in_scan(self) -> None:
        self.replace_once(
            "examples/scan.yml",
            "  contents: read\n",
            "  contents: read\n  pull-requests: write\n",
        )
        self.assert_rejected("examples/scan.yml permissions must be exactly")

    def test_rejects_missing_vibe_pull_request_write_permission(self) -> None:
        self.replace_once("examples/vibe-check.yml", "  pull-requests: write\n", "")
        self.assert_rejected("examples/vibe-check.yml permissions must be exactly")

    def test_rejects_missing_flowharness_api_url(self) -> None:
        self.replace_once(
            "examples/vibe-check.yml",
            "          FLOWHARNESS_API_URL: ${{ vars.FLOWHARNESS_API_URL }}\n",
            "",
        )
        self.assert_rejected(
            "examples/vibe-check.yml action env must include FLOWHARNESS_API_URL"
        )

    def test_rejects_wrong_action_input(self) -> None:
        self.replace_once(
            "examples/scan.yml", "          directory: .\n", "          path: .\n"
        )
        self.assert_rejected("examples/scan.yml Action inputs must be exactly")

    def test_rejects_wrong_vibe_action_input(self) -> None:
        self.replace_once(
            "examples/vibe-check.yml",
            "          executor: replay\n",
            "          mode: replay\n",
        )
        self.assert_rejected("examples/vibe-check.yml Action inputs must be exactly")

    def test_rejects_wrong_action_version(self) -> None:
        self.replace_once(
            "examples/scan.yml",
            "flowharness-ai/scan-action@v1",
            "flowharness-ai/scan-action@v2",
        )
        self.assert_rejected("examples/scan.yml must use flowharness-ai/scan-action@v1")

    def test_rejects_private_monorepo_url(self) -> None:
        self.append(
            "README.md",
            "\n[Private source](https://github.com/suleimanmahmoud/flowharness)\n",
        )
        self.assert_rejected("private monorepo URL")

    def test_rejects_banned_product_claim(self) -> None:
        self.append("README.md", "\nSOC 2 Ready\n")
        self.assert_rejected("banned product claim: SOC 2 Ready")

    def test_rejects_at_flowharness_core_claim(self) -> None:
        self.append("README.md", "\nInstall @flowharness/core.\n")
        self.assert_rejected("banned product claim: @flowharness/core")

    def test_rejects_low_latency_claim(self) -> None:
        self.append("README.md", "\nRequests complete in <15ms.\n")
        self.assert_rejected("banned product claim: <15ms")

    def test_rejects_runtime_proxy_claim(self) -> None:
        self.append("README.md", "\nFlowHarness is a low-latency LLM proxy.\n")
        self.assert_rejected("banned product claim: runtime or LLM proxy")

    def test_rejects_live_interception_claim(self) -> None:
        self.append("README.md", "\nAvailable today with live interception.\n")
        self.assert_rejected("banned product claim: live interception")

    def test_rejects_stale_b7_unproven_copy(self) -> None:
        self.append("README.md", "\nB7 has not proved sticky comments.\n")
        self.assert_rejected("stale B7-unproven copy")

    def test_rejects_placeholder_marker(self) -> None:
        self.append("README.md", "\nTBD: add the final guide.\n")
        self.assert_rejected("placeholder marker")

    def test_rejects_source_mirror_claim(self) -> None:
        self.replace_once(
            "README.md",
            "This public documentation and examples hub is not a VCS source mirror.",
            "This public documentation and examples hub is a source mirror.",
        )
        self.assert_rejected("must not call the public hub a source mirror")

    def test_rejects_semantic_source_mirror_claim(self) -> None:
        self.append(
            "README.md",
            "\nThis documentation hub serves as the complete source mirror.\n",
        )
        self.assert_rejected("must not call the public hub a source mirror")

    def test_rejects_another_affirmative_source_mirror_wording(self) -> None:
        self.append(
            "README.md",
            "\nThis documentation hub functions as a complete source mirror.\n",
        )
        self.assert_rejected("must not call the public hub a source mirror")

    def test_rejects_broken_relative_link(self) -> None:
        self.append("README.md", "\n[Missing guide](docs/does-not-exist.md)\n")
        self.assert_rejected("broken relative Markdown link")

    def test_rejects_relative_link_outside_repository(self) -> None:
        self.append("README.md", "\n[Outside](../outside.md)\n")
        self.assert_rejected("relative Markdown link escapes repository")

    def test_rejects_absent_sdist_hash(self) -> None:
        digest = PROVENANCE[0][3]
        self.replace_once("docs/source-and-provenance.md", digest, "")
        self.assert_rejected("missing SHA-256 for flowharness")

    def test_rejects_absent_sdist_filename(self) -> None:
        package, filename, _, _ = PROVENANCE[1]
        self.replace_once(
            "docs/source-and-provenance.md",
            f"| {package} | {filename} |",
            f"| {package} | missing.tar.gz |",
        )
        self.assert_rejected("missing sdist filename for flowharness-ci-runner")

    def test_rejects_absent_sdist_url(self) -> None:
        url = PROVENANCE[2][2]
        self.replace_once(
            "docs/source-and-provenance.md",
            url,
            "https://pypi.org/project/flowharness-core/",
        )
        self.assert_rejected("missing direct PyPI URL for flowharness-core")

    def test_rejects_sensitive_repository_query_parameter(self) -> None:
        self.append(
            "README.md",
            "\n[Leak](https://flowharness.ai/go/scan?repository=private/repo)\n",
        )
        self.assert_rejected("sensitive query parameter: repository")

    def test_rejects_sensitive_finding_query_parameter(self) -> None:
        self.append(
            "README.md", "\n[Leak](https://flowharness.ai/go/scan?finding=secret)\n"
        )
        self.assert_rejected("sensitive query parameter: finding")

    def test_rejects_sensitive_secret_query_parameter(self) -> None:
        self.append(
            "README.md", "\n[Leak](https://flowharness.ai/go/scan?secret=value)\n"
        )
        self.assert_rejected("sensitive query parameter: secret")

    def test_rejects_sensitive_query_only_markdown_url(self) -> None:
        self.append("README.md", "\n[Leak](?secret=value)\n")
        self.assert_rejected("sensitive query parameter: secret")

    def test_rejects_sensitive_relative_markdown_url(self) -> None:
        self.append(
            "README.md",
            "\n[Leak](docs/getting-started.md?repository=private/repo)\n",
        )
        self.assert_rejected("sensitive query parameter: repository")

    def test_rejects_sensitive_protocol_relative_markdown_url(self) -> None:
        self.append("README.md", "\n[Leak](//flowharness.ai/go/scan?finding=secret)\n")
        self.assert_rejected("sensitive query parameter: finding")

    def test_rejects_missing_category(self) -> None:
        self.replace_once("README.md", CATEGORY, "A governance tool for organizations.")
        self.assert_rejected("missing exact product category")

    def test_rejects_missing_open_core_boundary(self) -> None:
        self.replace_once(
            "README.md", OPEN_CORE, "FlowHarness has free and commercial products."
        )
        self.assert_rejected("missing exact open-core boundary")

    def test_rejects_missing_scan_tool(self) -> None:
        self.replace_once("README.md", "FlowHarness Scan", "Repository scanner")
        self.assert_rejected("missing released tool: FlowHarness Scan")

    def test_rejects_missing_vibe_check_tool(self) -> None:
        self.replace_once("README.md", "FlowHarness Vibe Check", "PR evaluation")
        self.assert_rejected("missing released tool: FlowHarness Vibe Check")

    def test_rejects_missing_organizational_bridge(self) -> None:
        self.replace_once(
            "README.md", "docs/organizational-platform.md", "docs/getting-started.md"
        )
        self.assert_rejected("missing organizational-platform bridge")

    def test_rejects_wrong_local_cli_version_matrix_entry(self) -> None:
        self.replace_once("README.md", "| Local CLI | 0.1.2 |", "| Local CLI | 0.1.1 |")
        self.assert_rejected("version matrix must identify local CLI 0.1.2")

    def test_rejects_wrong_version_matrix_header(self) -> None:
        self.replace_once(
            "README.md",
            "| Surface | Released version | Embedded Python artifact |",
            "| Surface | Version | Embedded Python artifact |",
        )
        self.assert_rejected("version matrix header must be exactly")

    def test_rejects_duplicate_version_matrix(self) -> None:
        matrix = """## Version matrix

| Surface | Released version | Embedded Python artifact |
| --- | --- | --- |
| Local CLI | 0.1.2 | flowharness 0.1.2 |
| Scan Action | v1.0.1 | flowharness 0.1.2 |
| Vibe Check Action | v1.0.1 | flowharness-ci-runner 0.1.1 |
"""
        self.append("README.md", f"\n{matrix}")
        self.assert_rejected("README.md must contain exactly one version matrix")

    def test_rejects_additional_version_matrix_row(self) -> None:
        self.replace_once(
            "README.md",
            "| Vibe Check Action | v1.0.1 | flowharness-ci-runner 0.1.1 |\n",
            "| Vibe Check Action | v1.0.1 | flowharness-ci-runner 0.1.1 |\n"
            "| Future Action | v2.0.0 | future-runner 2.0.0 |\n",
        )
        self.assert_rejected("version matrix rows must be exactly")

    def test_rejects_incomplete_version_matrix_cell(self) -> None:
        self.replace_once(
            "README.md",
            "| Scan Action | v1.0.1 | flowharness 0.1.2 |",
            "| Scan Action | v1.0.1 | |",
        )
        self.assert_rejected("version matrix rows must be exactly")

    def test_rejects_missing_version_matrix_row(self) -> None:
        self.replace_once(
            "README.md", "| Local CLI | 0.1.2 | flowharness 0.1.2 |\n", ""
        )
        self.assert_rejected("version matrix rows must be exactly")

    def test_rejects_wrong_scan_action_matrix_entry(self) -> None:
        self.replace_once(
            "README.md", "| Scan Action | v1.0.1 |", "| Scan Action | v1.0.0 |"
        )
        self.assert_rejected(
            "version matrix must identify Scan Action v1.0.1 with embedded 0.1.2"
        )

    def test_rejects_wrong_vibe_action_matrix_entry(self) -> None:
        self.replace_once(
            "README.md",
            "| Vibe Check Action | v1.0.1 |",
            "| Vibe Check Action | v1.0.0 |",
        )
        self.assert_rejected(
            "version matrix must identify Vibe Action v1.0.1 with embedded runner 0.1.1"
        )


if __name__ == "__main__":
    unittest.main()
