from pathlib import Path
import unittest


WORKFLOW = Path(__file__).parents[1] / ".github/workflows/security-baseline.yml"


class SecurityBaselineWorkflowTests(unittest.TestCase):
    def test_caller_uses_pinned_ghas_free_scanners(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("pull_request:", text)
        self.assertIn("push:\n    branches: [main]", text)
        self.assertIn("workflow_dispatch:", text)
        self.assertIn("Staros-Labs/infra/.github/workflows/reusable-security-gitleaks.yml@409ae040cd95594781278724fe6a8ba2027913c0", text)
        self.assertIn("Staros-Labs/infra/.github/workflows/reusable-security-osv.yml@409ae040cd95594781278724fe6a8ba2027913c0", text)
        self.assertEqual(text.count("report_only: true"), 2)
        self.assertNotIn("github/codeql-action", text)
        self.assertNotIn("security-events", text)
        self.assertNotIn("upload-sarif", text)
        self.assertNotIn("paths:", text)
        self.assertNotIn("paths-ignore:", text)


if __name__ == "__main__":
    unittest.main()
