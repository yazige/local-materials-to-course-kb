from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = PROJECT_ROOT / "skills" / "local-materials-to-course-kb"
INIT_PERSONAL = SKILL_ROOT / "scripts" / "init_personal_kb.py"
INIT_COURSE = SKILL_ROOT / "scripts" / "init_course_kb.py"
QUEUE_SCRIPT = SKILL_ROOT / "scripts" / "queue_inventory.py"
VERIFY_SCRIPT = SKILL_ROOT / "scripts" / "verify_course_kb.py"
AUTOMATION_PRESETS = SKILL_ROOT / "references" / "automation-presets.md"


def run_json(script: Path, *args: str) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(script), *args, "--format", "json"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if not completed.stdout:
        raise AssertionError(completed.stderr)
    return completed.returncode, json.loads(completed.stdout)


class VaultWorkflowTest(unittest.TestCase):
    def test_personal_initializer_creates_vault_queue_and_course_topics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            vault = Path(tmp_dir) / "vault"
            subprocess.run(
                [sys.executable, str(INIT_PERSONAL), "--vault-root", str(vault)],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertTrue((vault / "README.md").is_file())
            self.assertTrue((vault / "AGENTS.md").is_file())
            self.assertTrue((vault / "index.md").is_file())
            self.assertTrue((vault / "log.md").is_file())
            self.assertTrue((vault / "素材" / "待整理" / "TBD").is_dir())
            self.assertTrue((vault / "素材" / "待整理" / "Done").is_dir())
            self.assertTrue((vault / "素材" / "待整理" / "待复核" / "课程资料").is_dir())
            self.assertTrue((vault / "素材" / "待整理" / "待复核" / "创作复盘").is_dir())
            self.assertTrue(
                (
                    vault
                    / "知识库"
                    / "课程知识库"
                    / "A-岗前通用&基础认知"
                    / "01_知识主题"
                ).is_dir()
            )
            self.assertFalse((vault / "知识库" / "课程知识库" / "media").exists())

    def test_inventory_and_verifier_accept_vault_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            vault = Path(tmp_dir) / "vault"
            subprocess.run(
                [sys.executable, str(INIT_PERSONAL), "--vault-root", str(vault)],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            (vault / "素材" / "待整理" / "TBD" / "新资料.pdf").write_text("x")

            inventory_code, inventory = run_json(
                QUEUE_SCRIPT, "--vault-root", str(vault)
            )
            verify_code, verification = run_json(
                VERIFY_SCRIPT, "--vault-root", str(vault)
            )

            self.assertEqual(inventory_code, 0)
            self.assertEqual(inventory["queue"]["tbd_count"], 1)
            self.assertEqual(verify_code, 0)
            self.assertEqual(verification["errors"], [])

    def test_root_index_declares_navigation_only_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            vault = Path(tmp_dir) / "vault"
            subprocess.run(
                [sys.executable, str(INIT_PERSONAL), "--vault-root", str(vault)],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            root_index = (
                vault / "知识库" / "课程知识库" / "00_总索引.md"
            ).read_text(encoding="utf-8")

            self.assertIn(
                "只保留导航、累计数量、最近更新和一句摘要",
                root_index,
            )
            self.assertNotIn("## 知识正文", root_index)

    def test_skill_contains_four_paused_automation_presets(self) -> None:
        text = AUTOMATION_PRESETS.read_text(encoding="utf-8")

        self.assertIn("资料沉淀队列", text)
        self.assertIn("课程资料对话式复核", text)
        self.assertIn("本地知识库每周体检", text)
        self.assertIn("每周创作复盘", text)
        self.assertEqual(text.count("默认状态：`PAUSED`"), 4)
        self.assertIn("不要自动运行", text)


if __name__ == "__main__":
    unittest.main()
