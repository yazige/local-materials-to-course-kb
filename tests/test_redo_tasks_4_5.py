from __future__ import annotations

import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = PROJECT_ROOT / "skills" / "local-materials-to-course-kb"


class SkillFirstClassCapabilitiesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.presets = (
            SKILL_ROOT / "references" / "automation-presets.md"
        ).read_text(encoding="utf-8")

    def test_skill_names_three_first_class_capabilities(self) -> None:
        for heading in (
            "## 能力一：资料沉淀队列",
            "## 能力二：定期体检本地知识库",
            "## 能力三：定期创作复盘",
        ):
            self.assertIn(heading, self.skill)

    def test_ingestion_guards_context_and_suggests_off_peak_automation(self) -> None:
        for phrase in (
            "状态优先",
            "索引定位",
            "主题拆页",
            "一次一个批次",
            "Done 只读",
            "低使用时段",
            "避开用户高频使用 Codex 的时间",
            "不得一轮清空 TBD",
        ):
            self.assertIn(phrase, self.skill)

    def test_audit_has_required_checks_and_output_contract(self) -> None:
        for phrase in (
            "断链",
            "重复",
            "孤岛",
            "未整理",
            "待确认",
            "过期",
            "索引覆盖",
            "健康分",
            "最优先的 3 件事",
            "默认只读",
        ):
            self.assertIn(phrase, self.skill)

    def test_creation_review_has_evidence_states_and_write_allowlist(self) -> None:
        for phrase in (
            "AI 初稿",
            "修改意见",
            "最终稿",
            "稳定规律",
            "待观察",
            "待确认",
            "来源可追溯",
            "允许写入仅限",
            "reviews/",
            "wiki/",
            "index.md",
            "log.md",
        ):
            self.assertIn(phrase, self.skill)

    def test_presets_include_off_peak_and_full_output_contracts(self) -> None:
        self.assertIn("低使用时段", self.presets)
        self.assertIn("不得一轮清空 TBD", self.presets)
        self.assertIn("健康分：0-100", self.presets)
        self.assertIn("最优先处理的 3 件事", self.presets)
        self.assertIn("允许写入仅限", self.presets)


class PublicOnboardingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        cls.guide = (
            PROJECT_ROOT / "docs" / "build-your-personal-kb.md"
        ).read_text(encoding="utf-8")

    def test_readme_leads_with_full_pre_skill_onboarding(self) -> None:
        required = (
            "安装 Obsidian",
            "安装 Codex",
            "选择 Vault",
            "先确认存放路径",
            "核心目标",
            "素材层",
            "笔记层",
            "规则层",
            "生活.md",
            "工作.md",
            "学习.md",
            "index.md",
            "log.md",
            "AGENTS.md",
            "目标页",
            "一次只问一个问题",
            "用 Obsidian 打开",
            "验证",
            "安装 Skill",
            "三项自动化",
        )
        first_path = self.readme.split("## 你会得到什么", 1)[0]
        for phrase in required:
            self.assertIn(phrase, first_path)

    def test_guide_explains_bounded_context_mechanism(self) -> None:
        for phrase in (
            "索引定位",
            "主题拆页",
            "状态文件",
            "单批次",
            "不会随着知识库增长",
            "Obsidian",
        ):
            self.assertIn(phrase, self.guide)

    def test_sources_credit_feishu_and_karpathy_without_copying_prompt(self) -> None:
        combined = self.readme + self.guide
        self.assertIn("飞书", combined)
        self.assertIn("Karpathy", combined)
        self.assertIn("gist.github.com", combined)


if __name__ == "__main__":
    unittest.main()
