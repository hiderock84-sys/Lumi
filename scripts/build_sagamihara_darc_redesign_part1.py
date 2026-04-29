#!/usr/bin/env python3
"""参考スクリーンショット（第1回分）を完全再設計したPPTを生成する。

対象:
- 本日のご説明内容（10テーマ）
- 日本の依存症情勢 2024-2025
- 3段階予防と相模原ダルクの役割
- 組織概要・理念
- 実績ハイライト
- 相模原ダルクの強み (1/3), (2/3), (3/3)

要件:
- 内容は省略しない（主要項目を全て掲載）
- 既存デザインを流用せず、企業提案書風に全面リデザイン
"""

from __future__ import annotations

import argparse
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build redesigned part1 PPT from screenshot reference."
    )
    parser.add_argument(
        "--output",
        default="/workspace/outputs/sagamihara_darc_redesign_part1_from_screenshots.pptx",
        help="Output pptx path.",
    )
    return parser.parse_args()


class Theme:
    bg = RGBColor(245, 247, 252)
    panel = RGBColor(232, 238, 248)
    card = RGBColor(255, 255, 255)
    navy = RGBColor(16, 36, 74)
    accent = RGBColor(0, 174, 188)
    accent2 = RGBColor(75, 111, 255)
    text = RGBColor(21, 31, 49)
    sub = RGBColor(87, 101, 127)
    white = RGBColor(255, 255, 255)


def add_rect(slide, left, top, width, height, color: RGBColor, line: RGBColor | None = None):
    shp = slide.shapes.add_shape(1, left, top, width, height)
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(1.2)
    return shp


def add_text(
    slide,
    left,
    top,
    width,
    height,
    text: str,
    size: int = 16,
    bold: bool = False,
    color: RGBColor = Theme.text,
    align: PP_ALIGN = PP_ALIGN.LEFT,
):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    run = p.runs[0]
    run.font.name = "Meiryo"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return box


def add_bullets(
    slide,
    left,
    top,
    width,
    height,
    items: list[str],
    size: int = 14,
    color: RGBColor = Theme.text,
):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.clear()
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {item}"
        p.level = 0
        p.alignment = PP_ALIGN.LEFT
        if p.runs:
            run = p.runs[0]
            run.font.name = "Meiryo"
            run.font.size = Pt(size)
            run.font.color.rgb = color
    return box


def brand_header(slide, title: str, subtitle: str, page: str):
    add_rect(slide, Inches(0), Inches(0), SLIDE_W, SLIDE_H, Theme.bg)
    add_rect(slide, Inches(0), Inches(0), SLIDE_W, Inches(0.22), Theme.accent)
    add_rect(slide, Inches(0), Inches(0.22), SLIDE_W, Inches(0.9), Theme.navy)
    add_text(
        slide,
        Inches(0.45),
        Inches(0.40),
        Inches(8.8),
        Inches(0.35),
        title,
        size=20,
        bold=True,
        color=Theme.white,
    )
    add_text(
        slide,
        Inches(0.45),
        Inches(0.75),
        Inches(10.8),
        Inches(0.25),
        subtitle,
        size=11,
        color=RGBColor(201, 214, 238),
    )
    add_text(
        slide,
        Inches(12.1),
        Inches(0.42),
        Inches(1.0),
        Inches(0.25),
        page,
        size=11,
        color=Theme.white,
        align=PP_ALIGN.RIGHT,
    )
    add_rect(slide, Inches(0), Inches(7.2), SLIDE_W, Inches(0.3), Theme.panel)
    add_text(
        slide,
        Inches(0.35),
        Inches(7.26),
        Inches(7.5),
        Inches(0.2),
        "SAGAMIHARA DARC | STRATEGIC REDESIGN (PART 1)",
        size=9,
        color=Theme.sub,
    )


def cover(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_rect(slide, Inches(0), Inches(0), SLIDE_W, SLIDE_H, RGBColor(13, 28, 58))
    add_rect(slide, Inches(0), Inches(0), Inches(5.8), SLIDE_H, RGBColor(10, 22, 46))
    add_rect(slide, Inches(5.8), Inches(0), Inches(7.533), SLIDE_H, RGBColor(24, 56, 104))
    add_rect(slide, Inches(0), Inches(0), SLIDE_W, Inches(0.18), Theme.accent)
    add_text(
        slide,
        Inches(0.62),
        Inches(1.05),
        Inches(4.8),
        Inches(2.8),
        "相模原ダルク\n企業提案品質\nリデザイン資料",
        size=36,
        bold=True,
        color=Theme.white,
    )
    add_text(
        slide,
        Inches(0.62),
        Inches(4.35),
        Inches(4.9),
        Inches(1.4),
        "参考スクリーンショット（第1回分）の内容を\n省略せず再構築",
        size=14,
        color=RGBColor(184, 204, 235),
    )
    add_rect(slide, Inches(6.2), Inches(1.0), Inches(6.6), Inches(5.5), RGBColor(248, 250, 255))
    add_text(
        slide,
        Inches(6.55),
        Inches(1.35),
        Inches(6.0),
        Inches(0.45),
        "収録セクション（PAGE 2-9相当）",
        size=20,
        bold=True,
        color=Theme.navy,
    )
    add_bullets(
        slide,
        Inches(6.55),
        Inches(1.95),
        Inches(6.0),
        Inches(4.9),
        [
            "本日のご説明内容（10テーマ）",
            "日本の依存症情勢 2024-2025",
            "3段階予防と相模原ダルクの役割",
            "組織概要・理念（PHILOSOPHY / MISSION）",
            "実績ハイライト（400+ / 5%以下 / 90%以上 / 70名程度）",
            "強み 1/3（実績・プログラム・24h・5ステージ）",
            "強み 2/3（設備・当事者スタッフ・理事・就労B型）",
            "強み 3/3（連携・地域参加・家族支援・相談窓口）",
        ],
        size=14,
        color=Theme.text,
    )


def agenda_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    brand_header(slide, "本日のご説明内容｜本日のテーマ", "10テーマを企業説明向けに再整理", "02")
    add_rect(slide, Inches(0.55), Inches(1.45), Inches(12.2), Inches(0.85), Theme.card, Theme.panel)
    add_text(
        slide,
        Inches(0.8),
        Inches(1.66),
        Inches(9.2),
        Inches(0.4),
        "予定時間: 約60分 / テーマ数: 10 / 拠点数: 5",
        size=15,
        bold=True,
        color=Theme.navy,
    )
    add_text(
        slide,
        Inches(0.8),
        Inches(2.5),
        Inches(12.0),
        Inches(0.35),
        "01〜10 の全項目（原文趣旨）を維持し、理解導線を強化したレイアウトへ再設計",
        size=12,
        color=Theme.sub,
    )

    items = [
        ("01", "日本の依存症情勢（2024-2025）", "最新の薬物事犯統計と若年層の情勢分析"),
        ("02", "予防の3段階と当施設の役割", "第一次〜第三次予防のフレームワークと実装"),
        ("03", "組織概要・理念と実績", "2014年設立、400名以上の支援実績"),
        ("04", "相模原ダルクの8つの強み", "回復支援の核となる競争優位性"),
        ("05", "5ステージ制 回復プログラム", "段階的目標設定と役割付与による自立支援"),
        ("06", "施設・サービスの全体像", "5つの拠点と支援機能のネットワーク"),
        ("07", "回復プログラム詳細", "デイ・ナイト・個別の包括的アプローチ"),
        ("08", "依存症の理解（7つの特徴）", "科学的理解に基づく回復支援の前提条件"),
        ("09", "家族支援・連携ネットワーク", "CRAFTプログラムと地域連携体制"),
        ("10", "お問い合わせ", "初回相談無料・秘密厳守"),
    ]

    x1, x2 = Inches(0.7), Inches(6.9)
    y = Inches(3.0)
    w, h = Inches(5.7), Inches(0.68)
    for idx, (num, title, desc) in enumerate(items):
        col_x = x1 if idx < 5 else x2
        row = idx if idx < 5 else idx - 5
        yy = y + Inches(0.78) * row
        add_rect(slide, col_x, yy, w, h, Theme.card, Theme.panel)
        add_rect(slide, col_x + Inches(0.08), yy + Inches(0.10), Inches(0.55), Inches(0.46), Theme.accent2)
        add_text(
            slide,
            col_x + Inches(0.205),
            yy + Inches(0.18),
            Inches(0.3),
            Inches(0.2),
            num,
            size=10,
            bold=True,
            color=Theme.white,
            align=PP_ALIGN.CENTER,
        )
        add_text(
            slide,
            col_x + Inches(0.72),
            yy + Inches(0.10),
            Inches(4.8),
            Inches(0.22),
            title,
            size=12,
            bold=True,
            color=Theme.navy,
        )
        add_text(
            slide,
            col_x + Inches(0.72),
            yy + Inches(0.33),
            Inches(4.8),
            Inches(0.22),
            desc,
            size=10,
            color=Theme.sub,
        )


def trend_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    brand_header(slide, "日本の依存症情勢 2024-2025 最新", "警察庁白書情報を軸に、示唆まで明確化", "03")

    add_rect(slide, Inches(0.7), Inches(1.55), Inches(5.9), Inches(2.45), Theme.card, Theme.panel)
    add_text(slide, Inches(1.0), Inches(1.8), Inches(5.2), Inches(0.3), "2024年 薬物事犯検挙人員", size=13, color=Theme.sub)
    add_text(slide, Inches(1.0), Inches(2.15), Inches(3.8), Inches(0.8), "13,462", size=54, bold=True, color=Theme.navy)
    add_text(slide, Inches(4.35), Inches(2.42), Inches(2.0), Inches(0.3), "人", size=18, bold=True, color=Theme.navy)
    add_text(
        slide,
        Inches(1.0),
        Inches(3.05),
        Inches(5.3),
        Inches(0.8),
        "覚醒剤事犯 45.5% / 大麻事犯 45.1%\n引き続き高水準を維持",
        size=12,
        color=Theme.text,
    )

    add_rect(slide, Inches(6.95), Inches(1.55), Inches(5.7), Inches(2.45), Theme.card, Theme.panel)
    add_text(slide, Inches(7.2), Inches(1.8), Inches(5.2), Inches(0.3), "注目トピック (2024-2025)", size=13, bold=True, color=Theme.navy)
    add_bullets(
        slide,
        Inches(7.2),
        Inches(2.15),
        Inches(5.1),
        Inches(1.8),
        [
            "大麻取締法改正（2024年12月施行）",
            "SNS売買の急増（特に若年層）",
            "暴力団関与（覚醒剤密売の約50%）",
        ],
        size=12,
        color=Theme.text,
    )

    add_rect(slide, Inches(0.7), Inches(4.25), Inches(11.95), Inches(2.6), Theme.card, Theme.panel)
    add_text(slide, Inches(1.0), Inches(4.55), Inches(11.3), Inches(0.3), "重要なポイント", size=15, bold=True, color=Theme.navy)
    add_bullets(
        slide,
        Inches(1.0),
        Inches(4.95),
        Inches(11.3),
        Inches(1.6),
        [
            "2024年12月の法改正後、早期相談・再発予防・家族支援を横断した地域導線の再設計が必要",
            "若年層へのSNS経由の接触を前提に、啓発だけでなく相談導線の見える化が重要",
            "公的機関・医療・民間回復施設の連携を前提にした継続支援モデルが求められる",
            "※ 2024年データは警察庁公式統計、2025年は速報値を含む",
        ],
        size=12,
        color=Theme.text,
    )


def prevention_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    brand_header(slide, "3段階予防と相模原ダルクの役割", "第一次（啓発）/ 第二次（早期介入）/ 第三次（回復）", "04")

    add_rect(slide, Inches(0.7), Inches(1.45), Inches(12.0), Inches(0.72), Theme.card, Theme.panel)
    add_text(
        slide,
        Inches(1.0),
        Inches(1.66),
        Inches(10.8),
        Inches(0.25),
        "相模原ダルクは、予防から社会復帰まで切れ目ない支援を提供（支援実績 400+）",
        size=13,
        bold=True,
        color=Theme.navy,
    )

    cards = [
        (
            "第一次予防（啓発）",
            [
                "講演・研修による乱用防止啓発",
                "学校・地域での薬物乱用防止教育",
                "エイサー演舞等の文化活動による啓発",
                "ニュースレター発行",
            ],
        ),
        (
            "第二次予防（介入）",
            [
                "医療・行政・司法と連携した早期発見",
                "KIPP / FLOW / TAMARPP 協力",
                "個別相談・初期カウンセリング",
                "家族支援プログラム / 再乱用防止指導",
            ],
        ),
        (
            "第三次予防（回復）",
            [
                "入寮・通所による集中回復",
                "5段階ステージ制・就労継続支援B型",
                "24時間見守り / 医療・行政・司法連携",
                "アフターケア / 家族支援 / 社会復帰支援",
            ],
        ),
    ]
    x_positions = [Inches(0.7), Inches(4.8), Inches(8.9)]
    for (title, bullets), x in zip(cards, x_positions):
        add_rect(slide, x, Inches(2.45), Inches(3.75), Inches(4.15), Theme.card, Theme.panel)
        add_rect(slide, x, Inches(2.45), Inches(3.75), Inches(0.46), Theme.accent)
        add_text(slide, x + Inches(0.2), Inches(2.66), Inches(3.3), Inches(0.25), title, size=13, bold=True, color=Theme.navy)
        add_bullets(slide, x + Inches(0.2), Inches(3.05), Inches(3.3), Inches(3.3), bullets, size=11, color=Theme.text)


def org_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    brand_header(slide, "組織概要・理念｜PHILOSOPHY & MISSION", "人としての尊厳を大切に、生き直す力を支える", "05")

    add_rect(slide, Inches(0.7), Inches(1.55), Inches(3.7), Inches(5.9), Theme.card, Theme.panel)
    add_text(slide, Inches(1.0), Inches(1.85), Inches(3.1), Inches(0.25), "組織情報", size=14, bold=True, color=Theme.navy)
    add_bullets(
        slide,
        Inches(1.0),
        Inches(2.2),
        Inches(3.1),
        Inches(4.9),
        [
            "法人名: 一般社団法人 相模原ダルク",
            "設立日: 2014年3月3日",
            "代表理事: 田中 秀泰",
            "所在地: 神奈川県相模原市",
            "支援実績: 延べ400名以上",
        ],
        size=12,
    )

    add_rect(slide, Inches(4.65), Inches(1.55), Inches(8.05), Inches(2.75), Theme.card, Theme.panel)
    add_text(slide, Inches(4.95), Inches(1.85), Inches(7.5), Inches(0.25), "PHILOSOPHY｜理念", size=14, bold=True, color=Theme.navy)
    add_text(
        slide,
        Inches(4.95),
        Inches(2.2),
        Inches(7.5),
        Inches(1.8),
        "「人としての尊厳を大切に、生き直す力を支える」\n"
        "一人ひとりを尊重し、安心して自分を表現できる共同の場をつくる。\n"
        "誠実な関わりと対話を通じ、本来持つ力を呼び起こし育てる。",
        size=12,
        color=Theme.text,
    )

    add_rect(slide, Inches(4.65), Inches(4.7), Inches(8.05), Inches(2.75), Theme.card, Theme.panel)
    add_text(slide, Inches(4.95), Inches(5.0), Inches(7.5), Inches(0.25), "MISSION｜使命", size=14, bold=True, color=Theme.navy)
    add_text(
        slide,
        Inches(4.95),
        Inches(5.35),
        Inches(7.5),
        Inches(1.8),
        "「生き直す力で依存症からの回復を」\n"
        "回復は恐れや圧力では育たない。安心できる環境と誠実な関わりの中で育つ。\n"
        "施設・地域・社会の中に回復の共同体を作り続ける。",
        size=12,
        color=Theme.text,
    )


def performance_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    brand_header(slide, "実績ハイライト｜データで見る相模原ダルク", "数値は2026年時点（自施設集計）", "06")
    add_rect(slide, Inches(0.7), Inches(1.55), Inches(12.0), Inches(1.05), Theme.card, Theme.panel)
    add_text(
        slide,
        Inches(1.0),
        Inches(1.9),
        Inches(11.2),
        Inches(0.3),
        "400名以上の支援実績 / 5%以下の再使用率 / 90%以上の卒業後継続率",
        size=16,
        bold=True,
        color=Theme.navy,
    )

    metrics = [
        ("400+", "回復支援実績", "創設以来の延べ支援人数"),
        ("5%以下", "入所中の再使用率", "24時間見守り・プログラム実装"),
        ("90%以上", "卒業後の継続率", "ピア支援・アフターケア"),
        ("70名程度", "受け入れ体制", "大型寮5 + 個室寮9"),
    ]
    x = Inches(0.75)
    for val, label, sub in metrics:
        add_rect(slide, x, Inches(3.0), Inches(2.85), Inches(3.9), Theme.card, Theme.panel)
        add_text(slide, x + Inches(0.2), Inches(3.3), Inches(2.4), Inches(0.6), val, size=34, bold=True, color=Theme.navy)
        add_text(slide, x + Inches(0.2), Inches(4.0), Inches(2.5), Inches(0.25), label, size=12, bold=True, color=Theme.text)
        add_text(slide, x + Inches(0.2), Inches(4.35), Inches(2.5), Inches(0.8), sub, size=10, color=Theme.sub)
        x += Inches(3.0)

    add_text(
        slide,
        Inches(0.8),
        Inches(6.55),
        Inches(11.8),
        Inches(0.3),
        "※ 再使用率は入所中当事者を対象とした2026年1月時点調査（n=70）",
        size=10,
        color=Theme.sub,
    )


def strengths_slide_1(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    brand_header(slide, "相模原ダルクの強み（1/3）", "驚異的実績 / 最新プログラム / 24時間見守り / 5段階ステージ制", "07")
    cards = [
        ("驚異的な実績", ["延べ400名以上の支援実績", "在寮中再使用率5%以下", "卒業後継続率90%以上", "定員70名規模"]),
        ("最新プログラム", ["MATRIX/CBTベースの再発予防", "12ステップ", "個別カウンセリング統合", "毎年アップデート"]),
        ("24時間見守り", ["寮にスタッフ常駐", "随時相談可能", "初期再使用リスク低減", "生活リズム確立支援"]),
        ("5段階ステージ制", ["Stage1〜5で可視化", "目標・課題を明確化", "権利と責任の段階拡大", "段階的自立を促進"]),
    ]
    x_positions = [Inches(0.7), Inches(6.7)]
    y_positions = [Inches(1.6), Inches(4.35)]
    idx = 0
    for y in y_positions:
        for x in x_positions:
            title, bullets = cards[idx]
            idx += 1
            add_rect(slide, x, y, Inches(5.95), Inches(2.45), Theme.card, Theme.panel)
            add_rect(slide, x, y, Inches(5.95), Inches(0.35), Theme.accent2)
            add_text(slide, x + Inches(0.2), y + Inches(0.07), Inches(5.5), Inches(0.2), title, size=12, bold=True, color=Theme.white)
            add_bullets(slide, x + Inches(0.2), y + Inches(0.47), Inches(5.45), Inches(1.85), bullets, size=11, color=Theme.text)


def strengths_slide_2(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    brand_header(slide, "相模原ダルクの強み（2/3）", "設備規模 / 当事者スタッフ / 理事専門性 / 就労継続支援B型", "08")
    cards = [
        ("関東圏最大規模の設備", ["定員70名体制", "24時間体制", "大型寮5 + 個室寮9", "送迎支援あり"]),
        ("当事者スタッフ多数在籍", ["経験者だからできる寄り添い", "寮に24時間常駐", "躓きやすい時期への助言", "ピア支援の実装"]),
        ("経験豊富な理事陣", ["各分野のエキスパートが牽引", "医療・福祉・司法と連携", "開設10年以上の安定運営", "組織全体で回復へコミット"]),
        ("就労継続支援B型", ["無理のない就労訓練", "治療継続と両立可能", "一般就労へのステップ", "自立に向けた現実的支援"]),
    ]
    x_positions = [Inches(0.7), Inches(6.7)]
    y_positions = [Inches(1.6), Inches(4.35)]
    idx = 0
    for y in y_positions:
        for x in x_positions:
            title, bullets = cards[idx]
            idx += 1
            add_rect(slide, x, y, Inches(5.95), Inches(2.45), Theme.card, Theme.panel)
            add_rect(slide, x, y, Inches(5.95), Inches(0.35), Theme.accent)
            add_text(slide, x + Inches(0.2), y + Inches(0.07), Inches(5.5), Inches(0.2), title, size=12, bold=True, color=Theme.white)
            add_bullets(slide, x + Inches(0.2), y + Inches(0.47), Inches(5.45), Inches(1.85), bullets, size=11, color=Theme.text)


def strengths_slide_3(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    brand_header(slide, "相模原ダルクの強み（3/3）", "医療・行政・司法連携 / 地域参加 / 家族支援 / 相談窓口", "09")
    cards = [
        ("医療・行政・司法連携", ["KIPP/FLOW/TAMARPP 協力", "保護観察所の再乱用防止プログラム", "刑務所・少年院での離脱指導", "現場で実装できる協働体制"]),
        ("地域社会への参加", ["琉球太鼓エイサー演舞参加", "清掃ボランティア", "学校・地域での講演活動", "共生を育む継続活動"]),
        ("家族支援を継続", ["毎週の家族相談", "月1回の家族会（学習+MTG）", "CRAFT的関わりの実践", "家族も回復のパートナー"]),
        ("相談窓口を常設", ["初回相談無料・秘密厳守", "本人・家族・周囲どなたでも", "平日 9:00-17:00", "土祝 9:00-14:00"]),
    ]
    x_positions = [Inches(0.7), Inches(6.7)]
    y_positions = [Inches(1.6), Inches(4.35)]
    idx = 0
    for y in y_positions:
        for x in x_positions:
            title, bullets = cards[idx]
            idx += 1
            add_rect(slide, x, y, Inches(5.95), Inches(2.45), Theme.card, Theme.panel)
            add_rect(slide, x, y, Inches(5.95), Inches(0.35), Theme.navy)
            add_text(slide, x + Inches(0.2), y + Inches(0.07), Inches(5.5), Inches(0.2), title, size=12, bold=True, color=Theme.white)
            add_bullets(slide, x + Inches(0.2), y + Inches(0.47), Inches(5.45), Inches(1.85), bullets, size=11, color=Theme.text)


def build(output: Path):
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    cover(prs)
    agenda_slide(prs)
    trend_slide(prs)
    prevention_slide(prs)
    org_slide(prs)
    performance_slide(prs)
    strengths_slide_1(prs)
    strengths_slide_2(prs)
    strengths_slide_3(prs)

    output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output))


def verify(output: Path):
    prs = Presentation(str(output))
    if len(prs.slides) != 9:
        raise RuntimeError(f"Unexpected slide count: {len(prs.slides)} (expected 9)")
    required = [
        "本日のご説明内容",
        "日本の依存症情勢",
        "3段階予防",
        "組織概要",
        "実績ハイライト",
        "強み（1/3）",
        "強み（2/3）",
        "強み（3/3）",
    ]
    text = []
    for s in prs.slides:
        for sh in s.shapes:
            t = getattr(sh, "text", "")
            if t:
                text.append(t)
    joined = "\n".join(text)
    miss = [k for k in required if k not in joined]
    if miss:
        raise RuntimeError(f"Missing required sections: {miss}")


def main():
    args = parse_args()
    output = Path(args.output).expanduser().resolve()
    build(output)
    verify(output)
    print(f"Generated: {output}")


if __name__ == "__main__":
    main()
