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
        cls.classification = (
            SKILL_ROOT / "references" / "classification-and-audit.md"
        ).read_text(encoding="utf-8")
        cls.lifecycle = (
            SKILL_ROOT / "references" / "workspace-lifecycle.md"
        ).read_text(encoding="utf-8")

    def test_skill_names_four_first_class_capabilities(self) -> None:
        for heading in (
            "## 能力一：资料沉淀队列",
            "## 能力二：课程资料对话式复核",
            "## 能力三：定期体检本地知识库",
            "## 能力四：定期创作复盘",
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

    def test_skill_hardens_index_dedup_transcript_and_audit_boundaries(self) -> None:
        for phrase in (
            "`00_总索引.md` 只允许保存导航、累计数量、最近更新和一句摘要",
            "去重顺序不可跳过",
            "文件名、标题和关键词搜索",
            "盘点和体检禁止读取原始转写稿",
            "只有当前批次进入提取或审核阶段后",
            "先运行 `scripts/kb_health_inventory.py`",
            "禁止把全库正文或脚本读取到的正文批量送入模型",
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

    def test_dialogue_review_has_ab_state_machine_and_sync_contract(self) -> None:
        combined = self.skill + self.lifecycle
        for phrase in (
            "AI 先总结材料",
            "只把需要用户业务判断的结论提交确认",
            "A、B 是待确认槽位，不是必须补满的配额",
            "用户回答 A 时，只处理 A",
            "原样保留仍属独立判断的 B",
            "只有当前项仍有阻塞写入的独立核心结论时",
            "用户回答 B 时反向执行",
            "暂停新问题",
            "接力摘要",
            "资料摘要",
            "可沉淀知识",
            "复核清单",
            "`index.md`",
            "`log.md`",
        ):
            self.assertIn(phrase, combined)

    def test_dialogue_review_caps_each_decision_chain_at_two_levels(self) -> None:
        combined = self.skill + self.lifecycle
        for phrase in (
            "同一判断链最多两层",
            "第 2 层确认后必须收口",
            "按实际情况判断",
            "不得为了维持 A/B 数量继续生成同链追问",
            "两层内形成结论后",
            "标记该项“已写入”",
        ):
            self.assertIn(phrase, combined)

    def test_scene_material_is_not_forced_into_one_primary_category(self) -> None:
        combined = self.skill + self.classification
        for phrase in (
            "知识主题型",
            "问题场景型",
            "只选择一个主分类",
            "不强行归入单一分类",
            "保留完整场景",
            "双向链接",
            "可复用知识",
            "对应模块",
            "资料类型：问题场景型",
            "场景入口",
            "涉及模块",
            "场景索引",
            "没有权威归属",
            "不要为了收口强行选择分类",
        ):
            self.assertIn(phrase, combined)

    def test_dialogue_review_automation_is_paused_and_waits_for_user(self) -> None:
        for phrase in (
            "课程资料对话式复核",
            "默认状态：`PAUSED`",
            "已有未决 A/B 时，只展示现有 A/B",
            "不要先修改知识库",
            "不处理 TBD 新资料",
            "不运行知识库体检或创作复盘",
        ):
            self.assertIn(phrase, self.presets)


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
            "四项自动化",
        )
        first_path = self.readme.split("## 你会得到什么", 1)[0]
        for phrase in required:
            self.assertIn(phrase, first_path)

    def test_readme_keeps_the_original_reader_story_and_course_use_cases(self) -> None:
        for phrase in (
            "资料越攒越多",
            "适合谁",
            "培训负责人",
            "做 SOP",
            "视频转写",
            "可复用的课程资产",
            "通义听悟",
            "项目结构",
        ):
            self.assertIn(phrase, self.readme)

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

    def test_guide_is_self_contained_for_building_the_vault(self) -> None:
        for phrase in (
            "无需离开本页",
            "下载 Obsidian",
            "Codex 官方文档",
            "复制下面这段提示词",
            "先确认两个问题",
            "一次只问一个问题",
            "每次回答后",
            "生活.md",
            "工作.md",
            "学习.md",
            "目标_",
            "README.md",
            "AGENTS.md",
            "index.md",
            "log.md",
            "素材/待整理/TBD",
            "转载并改编自",
        ):
            self.assertIn(phrase, self.guide)


if __name__ == "__main__":
    unittest.main()
