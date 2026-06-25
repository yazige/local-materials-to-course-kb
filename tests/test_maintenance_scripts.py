from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = PROJECT_ROOT / "skills" / "local-materials-to-course-kb"
INIT_SCRIPT = SKILL_ROOT / "scripts" / "init_course_kb.py"
QUEUE_SCRIPT = SKILL_ROOT / "scripts" / "queue_inventory.py"
VERIFY_SCRIPT = SKILL_ROOT / "scripts" / "verify_course_kb.py"


def run_json(script: Path, *args: str) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(script), *args, "--format", "json"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert completed.stdout, completed.stderr
    return completed.returncode, json.loads(completed.stdout)


def init_kb(root: Path) -> None:
    subprocess.run(
        [sys.executable, str(INIT_SCRIPT), "--root", str(root)],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class MaintenanceScriptsTest(unittest.TestCase):
    def test_queue_inventory_counts_visible_top_level_items_and_work_statuses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir) / "kb"
            init_kb(root)

            (root / "media" / "TBD" / ".DS_Store").write_text("mac metadata")
            (root / "media" / "TBD" / "2025-广告课").mkdir()
            (root / "media" / "TBD" / "2025-账号风控.pdf").write_text(
                "pdf placeholder"
            )
            (root / "media" / "Done" / "2026-06-25_已完成批次").mkdir()

            work_area = root / "98_音视频处理工作区"
            (work_area / "2026-06-25_广告课_音视频转课程知识库_v1_待复核").mkdir(
                parents=True
            )
            (work_area / "2026-06-25_账号风控_音视频转课程知识库_v1_处理中").mkdir()

            code, report = run_json(QUEUE_SCRIPT, "--root", str(root))

            self.assertEqual(code, 0)
            self.assertEqual(report["media"]["tbd_count"], 2)
            self.assertEqual(report["media"]["done_count"], 1)
            self.assertEqual(report["media"]["hidden_ignored_count"], 1)
            self.assertEqual(report["work_area"]["total_dirs"], 2)
            self.assertEqual(report["work_area"]["status_counts"], {"待复核": 1, "处理中": 1})
            self.assertIn("先收口", report["next_recommended_action"])


    def test_verify_course_kb_reports_missing_required_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir) / "kb"
            init_kb(root)
            (root / "media" / "Done").rmdir()

            code, report = run_json(VERIFY_SCRIPT, "--root", str(root))

            self.assertEqual(code, 1)
            self.assertTrue(any("media/Done" in item for item in report["errors"]))


    def test_verify_course_kb_accepts_initialized_structure_with_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir) / "kb"
            init_kb(root)
            (root / "media" / ".DS_Store").write_text("mac metadata")
            (
                root
                / "98_音视频处理工作区"
                / "2026-06-25_广告课_音视频转课程知识库_v1_待复核"
            ).mkdir(parents=True)

            code, report = run_json(VERIFY_SCRIPT, "--root", str(root))

            self.assertEqual(code, 0)
            self.assertEqual(report["errors"], [])
            self.assertTrue(any(".DS_Store" in item for item in report["warnings"]))
            self.assertTrue(any("待复核" in item for item in report["warnings"]))


if __name__ == "__main__":
    unittest.main()
