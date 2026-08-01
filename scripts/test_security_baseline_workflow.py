from __future__ import annotations

import re
import unittest
from pathlib import Path

WORKFLOW = Path(__file__).parents[1] / ".github/workflows/security-baseline.yml"
IMMUTABLE_REF = re.compile(
    r"^\s+uses: Staros-Labs/infra/.+@[0-9a-f]{40}$", re.MULTILINE
)
APPROVED_SHA = "e3b2d2216d219115ffe796aa4cd000a5f41f8b0a"


class SecurityBaselineWorkflowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.source = WORKFLOW.read_text(encoding="utf-8")

    def test_uses_unfiltered_report_only_reusable_scanners(self) -> None:
        for event in ("pull_request:", "push:", "schedule:", "workflow_dispatch:"):
            self.assertIn(f"  {event}", self.source)
        self.assertNotIn("paths", self.source)
        self.assertNotIn("paths-ignore", self.source)

        self.assertEqual(len(IMMUTABLE_REF.findall(self.source)), 4)
        self.assertEqual(self.source.count(f"@{APPROVED_SHA}"), 4)
        self.assertEqual(self.source.count("report_only: true"), 4)
        self.assertEqual(self.source.count("contents: read"), 5)
        for workflow in (
            "reusable-security-gitleaks.yml",
            "reusable-security-osv.yml",
            "reusable-security-trivy.yml",
        ):
            self.assertIn(f"Staros-Labs/infra/.github/workflows/{workflow}@", self.source)

    def test_forbids_ghas_and_external_report_uploads(self) -> None:
        for forbidden in ("github/codeql-action", "security-events", "upload-sarif"):
            self.assertNotIn(forbidden, self.source)


if __name__ == "__main__":
    unittest.main()
