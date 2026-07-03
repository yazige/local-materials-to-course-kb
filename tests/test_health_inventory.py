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
HEALTH_INVENTORY = SKILL_ROOT / "scripts" / "kb_health_inventory.py"


def run_json(*args: str) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(HEALTH_INVENTORY), *args, "--format", "json"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if not completed.stdout:
        raise AssertionError(completed.stderr)
    return completed.returncode, json.loads(completed.stdout)


class HealthInventoryTest(unittest.TestCase):
    def init_vault(self, root: Path) -> None:
        subprocess.run(
            [sys.executable, str(INIT_PERSONAL), "--vault-root", str(root)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_report_finds_candidates_without_leaking_page_body(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            vault = Path(tmp_dir) / "vault"
            self.init_vault(vault)
            topic_root = (
                vault
                / "知识库"
                / "课程知识库"
                / "A-岗前通用&基础认知"
                / "01_知识主题"
            )
            sentinel = "PRIVATE_BODY_SENTINEL"
            (topic_root / "已链接主题.md").write_text(
                f"# 已链接主题\n\n正文 {sentinel}\n", encoding="utf-8"
            )
            (topic_root / "孤岛主题.md").write_text(
                f"# 孤岛主题\n\n待确认 {sentinel}\n", encoding="utf-8"
            )
            (topic_root / "重复一.md").write_text(
                f"# 重复\n\n可能过时 {sentinel}\n", encoding="utf-8"
            )
            (topic_root / "重复二.md").write_text(
                f"# 重复\n\n可能过时 {sentinel}\n", encoding="utf-8"
            )
            raw_root = vault / "raw"
            raw_root.mkdir()
            (raw_root / "原始转写稿.md").write_text(
                f"# 原始转写\n\n待确认 {sentinel}\n", encoding="utf-8"
            )
            (
                vault
                / "知识库"
                / "课程知识库"
                / "A-岗前通用&基础认知"
                / "01_知识主文档.md"
            ).write_text(
                "# 入口\n\n[[01_知识主题/已链接主题]]\n"
                "[坏链接](01_知识主题/不存在.md)\n",
                encoding="utf-8",
            )

            code, report = run_json("--vault-root", str(vault), "--limit", "20")
            serialized = json.dumps(report, ensure_ascii=False)

            self.assertEqual(code, 0)
            self.assertNotIn(sentinel, serialized)
            self.assertGreaterEqual(report["summary"]["broken_links"], 1)
            self.assertGreaterEqual(report["summary"]["exact_duplicate_groups"], 1)
            self.assertGreaterEqual(report["summary"]["orphan_candidates"], 1)
            self.assertGreaterEqual(report["summary"]["pending_confirmation"], 1)
            self.assertGreaterEqual(report["summary"]["stale_candidates"], 1)
            self.assertGreaterEqual(report["summary"]["source_markdown_skipped"], 1)
            self.assertFalse(
                any(
                    item.startswith("raw/")
                    for item in report["candidates"]["pending_confirmation"]["items"]
                )
            )
            self.assertTrue(
                any(
                    item.endswith("孤岛主题.md")
                    for item in report["candidates"]["orphan_candidates"]["items"]
                )
            )

    def test_large_vault_report_is_bounded_and_marks_truncation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            vault = Path(tmp_dir) / "vault"
            self.init_vault(vault)
            topic_root = (
                vault
                / "知识库"
                / "课程知识库"
                / "A-岗前通用&基础认知"
                / "01_知识主题"
            )
            for index in range(200):
                (topic_root / f"未索引主题_{index:03d}.md").write_text(
                    f"# 未索引主题 {index}\n\n不应出现在报告中的正文 {index}\n",
                    encoding="utf-8",
                )

            code, report = run_json("--vault-root", str(vault), "--limit", "10")
            orphan_report = report["candidates"]["orphan_candidates"]

            self.assertEqual(code, 0)
            self.assertEqual(len(orphan_report["items"]), 10)
            self.assertTrue(orphan_report["truncated"])
            self.assertEqual(orphan_report["total"], 200)
            self.assertNotIn(
                "不应出现在报告中的正文",
                json.dumps(report, ensure_ascii=False),
            )

    def test_raw_directory_is_counted_but_never_scanned_for_markers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            vault = Path(tmp_dir) / "vault"
            (vault / "raw").mkdir(parents=True)
            (vault / "wiki").mkdir()
            (vault / "raw" / "source.md").write_text(
                "# 原始转写\n\n待确认 RAW_SENTINEL\n",
                encoding="utf-8",
            )
            (vault / "wiki" / "正式知识.md").write_text(
                "# 正式知识\n",
                encoding="utf-8",
            )

            code, report = run_json("--vault-root", str(vault), "--limit", "20")

            self.assertEqual(code, 0)
            self.assertEqual(report["summary"]["source_markdown_skipped"], 1)
            self.assertEqual(report["summary"]["markdown_scanned"], 1)
            self.assertEqual(report["summary"]["pending_confirmation"], 0)


if __name__ == "__main__":
    unittest.main()
