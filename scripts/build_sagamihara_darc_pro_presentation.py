#!/usr/bin/env python3
"""相模原ダルク紹介用のプロ仕様PowerPointを自動生成するスクリプト。

このスクリプトは次の2部構成で資料を生成する:
1) 公式サイト・公的情報を反映した新規セクション
2) ユーザー提供の参考PDFを全ページ画像化して付録として完全コピー
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import Iterable

import fitz  # PyMuPDF
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


# 16:9 (wide) default
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a complete pro-level Sagamihara DARC presentation."
    )
    parser.add_argument(
        "--reference-pdf",
        default=(
            "/workspace/reference_materials/"
            "sagamihara_darc_presentation_2026_20260421013752.pdf"
        ),
        help="Path to the reference PDF to copy as appendix slides.",
    )
    parser.add_argument(
        "--output",
        default="/workspace/outputs/sagamihara_darc_presentation_complete_pro_2026.pptx",
        help="Output .pptx path.",
    )
    parser.add_argument(
        "--workdir",
        default="/workspace/outputs/tmp_reference_pages",
        help="Directory used for rendered reference page images.",
    )
    return parser.parse_args()


def add_rect(slide, left, top, width, height, color: RGBColor, line: bool = False):
    shape = slide.shapes.add_shape(1, left, top, width, height)  # MSO_AUTO_SHAPE_TYPE.RECTANGLE
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    if line:
        shape.line.color.rgb = RGBColor(80, 90, 110)
    else:
        shape.line.fill.background()
    return shape


def add_textbox(
    slide,
    left,
    top,
    width,
    height,
    text: str,
    font_size: int = 18,
    bold: bool = False,
    color: RGBColor = RGBColor(240, 244, 252),
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
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    return box


def add_bullets(
    slide,
    left,
    top,
    width,
    height,
    title: str,
    bullets: Iterable[str],
    title_size: int = 20,
    body_size: int = 16,
):
    card = add_rect(slide, left, top, width, height, RGBColor(19, 30, 51))
    add_textbox(
        slide,
        left + Inches(0.24),
        top + Inches(0.12),
        width - Inches(0.4),
        Inches(0.5),
        title,
        font_size=title_size,
        bold=True,
        color=RGBColor(118, 239, 220),
    )

    body = slide.shapes.add_textbox(
        left + Inches(0.24), top + Inches(0.62), width - Inches(0.4), height - Inches(0.7)
    )
    tf = body.text_frame
    tf.clear()
    first = True
    for item in bullets:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.text = f"• {item}"
        p.level = 0
        p.alignment = PP_ALIGN.LEFT
        if p.runs:
            run = p.runs[0]
            run.font.name = "Meiryo"
            run.font.size = Pt(body_size)
            run.font.color.rgb = RGBColor(238, 242, 250)

    return card


def add_master_header(slide, title: str, subtitle: str):
    add_rect(slide, Inches(0), Inches(0), SLIDE_W, SLIDE_H, RGBColor(10, 18, 34))
    add_rect(slide, Inches(0), Inches(0), SLIDE_W, Inches(0.18), RGBColor(0, 181, 173))
    add_rect(slide, Inches(0), Inches(0.18), SLIDE_W, Inches(0.75), RGBColor(13, 25, 45))

    add_textbox(
        slide,
        Inches(0.5),
        Inches(0.27),
        Inches(8.2),
        Inches(0.35),
        title,
        font_size=20,
        bold=True,
    )
    add_textbox(
        slide,
        Inches(0.5),
        Inches(0.57),
        Inches(10.0),
        Inches(0.28),
        subtitle,
        font_size=12,
        color=RGBColor(177, 195, 225),
    )


def add_footer(slide, page_label: str):
    add_rect(slide, Inches(0), SLIDE_H - Inches(0.34), SLIDE_W, Inches(0.34), RGBColor(8, 14, 26))
    add_textbox(
        slide,
        Inches(0.38),
        SLIDE_H - Inches(0.28),
        Inches(6.8),
        Inches(0.2),
        "SAGAMIHARA DARC | CORPORATE PRESENTATION 2026",
        font_size=10,
        color=RGBColor(150, 166, 196),
    )
    add_textbox(
        slide,
        SLIDE_W - Inches(1.4),
        SLIDE_H - Inches(0.28),
        Inches(1.0),
        Inches(0.2),
        page_label,
        font_size=10,
        color=RGBColor(150, 166, 196),
        align=PP_ALIGN.RIGHT,
    )


def add_cover_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_rect(slide, Inches(0), Inches(0), SLIDE_W, SLIDE_H, RGBColor(8, 16, 33))
    add_rect(slide, Inches(0), Inches(0), SLIDE_W, Inches(0.2), RGBColor(0, 181, 173))
    add_rect(slide, Inches(0), Inches(0.2), Inches(6.2), Inches(7.3), RGBColor(10, 22, 43))
    add_rect(slide, Inches(6.1), Inches(0.2), Inches(7.233), Inches(7.3), RGBColor(16, 34, 62))

    add_textbox(
        slide,
        Inches(0.65),
        Inches(1.25),
        Inches(5.5),
        Inches(2.4),
        "一般社団法人\n相模原ダルク\n紹介資料 完全版",
        font_size=38,
        bold=True,
    )
    add_textbox(
        slide,
        Inches(0.65),
        Inches(4.0),
        Inches(5.2),
        Inches(1.2),
        "CHANGE YOUR LIFE!\n依存症からの回復支援を、予防から社会復帰まで一気通貫で実装",
        font_size=15,
        color=RGBColor(194, 210, 236),
    )

    add_bullets(
        slide,
        Inches(6.55),
        Inches(1.2),
        Inches(6.35),
        Inches(4.8),
        "本資料の構成",
        [
            "Part A: 公式サイト・公的情報を反映した新規プロ仕様セクション",
            "Part B: 提供資料の完全コピー（18ページ）",
            "目的: 既存情報の維持 + 最新情報・経営視点を追加",
            "用途: 説明会、連携機関向け提案、家族会・支援機関共有",
        ],
        title_size=24,
        body_size=16,
    )
    add_textbox(
        slide,
        Inches(0.65),
        Inches(6.75),
        Inches(5.4),
        Inches(0.5),
        f"作成日: {date.today().isoformat()}",
        font_size=11,
        color=RGBColor(148, 167, 200),
    )


def add_executive_summary(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_master_header(
        slide,
        "Executive Summary",
        "相模原ダルクの提供価値を、実績・支援設計・社会連携の3軸で整理",
    )
    add_bullets(
        slide,
        Inches(0.6),
        Inches(1.15),
        Inches(4.0),
        Inches(5.7),
        "組織価値",
        [
            "理念: 人としての尊厳を大切に、生き直す力を支える",
            "依存症回復を、生活・就労・家族支援まで含めて設計",
            "当事者スタッフ中心の伴走型支援",
        ],
    )
    add_bullets(
        slide,
        Inches(4.75),
        Inches(1.15),
        Inches(4.0),
        Inches(5.7),
        "実績・体制",
        [
            "創設以来の延べ支援実績 400名以上",
            "5つの大型寮 + 個室寮9室、定員約70名規模",
            "24時間見守りと5段階ステージ制による自立支援",
        ],
    )
    add_bullets(
        slide,
        Inches(8.9),
        Inches(1.15),
        Inches(3.8),
        Inches(5.7),
        "対外連携",
        [
            "医療・行政・司法・地域団体とのネットワーク",
            "予防啓発、家族会、就労支援を統合",
            "地域の依存症課題に対する社会資源として機能",
        ],
    )
    add_footer(slide, "2")


def add_agenda(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_master_header(slide, "Agenda", "新規セクションと完全コピー付録の全体像")

    left_items = [
        "1. 外部環境（依存症情勢・政策動向）",
        "2. 相模原ダルクの理念・提供価値",
        "3. サービスポートフォリオと支援プロセス",
        "4. 差別化要因（8つの強み）",
        "5. 連携ネットワーク・家族支援",
    ]
    right_items = [
        "6. KPIダッシュボード設計",
        "7. 実行ロードマップ（提案）",
        "8. お問い合わせ導線",
        "9. 出典一覧",
        "10. 付録: 提供資料の完全コピー（18ページ）",
    ]
    add_bullets(slide, Inches(0.9), Inches(1.3), Inches(5.8), Inches(5.2), "Part A (新規)", left_items)
    add_bullets(slide, Inches(6.65), Inches(1.3), Inches(5.8), Inches(5.2), "Part B (付録)", right_items)
    add_footer(slide, "3")


def add_environment_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_master_header(
        slide,
        "外部環境: 日本の薬物情勢（2024-2025）",
        "警察庁 令和7年警察白書・厚生労働省依存症対策ページを基に要約",
    )

    add_bullets(
        slide,
        Inches(0.7),
        Inches(1.2),
        Inches(6.1),
        Inches(5.9),
        "公的統計ハイライト",
        [
            "2024年の薬物事犯検挙人員は13,462人（高水準を維持）",
            "全薬物事犯に占める比率: 覚醒剤 45.5%、大麻 45.1%",
            "20歳代以下の若年層で大麻事犯が継続して高水準",
            "2024年12月: 大麻施用罪を含む法改正が施行",
        ],
    )
    add_bullets(
        slide,
        Inches(7.05),
        Inches(1.2),
        Inches(5.55),
        Inches(5.9),
        "示唆",
        [
            "早期介入・相談導線の拡充が一層重要",
            "家族・学校・地域連携による一次予防の継続が必要",
            "治療後の再発予防と社会復帰支援の統合設計が鍵",
            "公的機関・民間回復施設の役割分担と接続強化が必要",
        ],
    )
    add_footer(slide, "4")


def add_value_proposition_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_master_header(slide, "理念・ミッション・提供価値", "公式サイト施設情報を基に再構成")
    add_bullets(
        slide,
        Inches(0.75),
        Inches(1.2),
        Inches(5.7),
        Inches(5.9),
        "理念・使命",
        [
            "理念: 人としての尊厳を大切に、生き直す力を支える",
            "使命: 生き直す力で依存症からの回復を",
            "安心して自分を表現できる共同の場づくりを重視",
        ],
    )
    add_bullets(
        slide,
        Inches(6.7),
        Inches(1.2),
        Inches(5.9),
        Inches(5.9),
        "提供価値",
        [
            "相談・入寮・通所・就労支援を段階的に提供",
            "本人だけでなく家族・周囲の方の相談にも対応",
            "依存症回復を社会参加までつなぐ伴走型支援",
            "地域の多機関連携ネットワークのハブ機能",
        ],
    )
    add_footer(slide, "5")


def add_service_portfolio_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_master_header(slide, "サービスポートフォリオ", "公式ページ記載の事業内容を俯瞰")
    add_bullets(
        slide,
        Inches(0.7),
        Inches(1.15),
        Inches(3.95),
        Inches(2.6),
        "障害福祉サービス",
        ["自立訓練（生活訓練）", "就労継続支援B型", "段階的な社会参加を支援"],
        title_size=18,
        body_size=14,
    )
    add_bullets(
        slide,
        Inches(4.85),
        Inches(1.15),
        Inches(3.95),
        Inches(2.6),
        "入寮事業",
        ["大型寮5か所 + 個室寮9室", "24時間体制の見守り", "依存症治療に特化した住環境"],
        title_size=18,
        body_size=14,
    )
    add_bullets(
        slide,
        Inches(9.0),
        Inches(1.15),
        Inches(3.95),
        Inches(2.6),
        "相談事業",
        ["本人・家族・周囲の方が相談可能", "初回無料（公式案内）", "秘密保持のもとで対応"],
        title_size=18,
        body_size=14,
    )
    add_bullets(
        slide,
        Inches(0.7),
        Inches(3.95),
        Inches(6.25),
        Inches(2.9),
        "連携・協力事業",
        [
            "医療機関・行政機関・地域団体との連携",
            "依存症回復プログラムの監修・助言・運営協力",
            "地域全体の回復支援ネットワークを形成",
        ],
        title_size=18,
        body_size=14,
    )
    add_bullets(
        slide,
        Inches(7.15),
        Inches(3.95),
        Inches(5.8),
        Inches(2.9),
        "予防・啓発事業",
        [
            "教育機関・行政・団体向け講演活動",
            "地域イベント参加（エイサー演舞など）",
            "予防啓発を通じた再発防止・早期相談促進",
        ],
        title_size=18,
        body_size=14,
    )
    add_footer(slide, "6")


def add_recovery_process_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_master_header(slide, "回復支援プロセス", "相談から社会復帰・継続支援までの標準導線")
    stages = [
        "01 初回相談\n（本人・家族・関係者）",
        "02 アセスメント\n（課題/状態/希望の整理）",
        "03 導入期支援\n（入寮/通所・生活再建）",
        "04 回復プログラム\n（5ステージ制・個別支援）",
        "05 社会復帰準備\n（就労支援・地域連携）",
        "06 アフターケア\n（家族会・継続フォロー）",
    ]

    box_w = Inches(2.0)
    gap = Inches(0.15)
    left = Inches(0.45)
    top = Inches(2.0)
    for idx, stage in enumerate(stages):
        x = left + idx * (box_w + gap)
        color = RGBColor(0, 181, 173) if idx in (0, 5) else RGBColor(30, 58, 96)
        add_rect(slide, x, top, box_w, Inches(2.2), color)
        add_textbox(
            slide,
            x + Inches(0.15),
            top + Inches(0.18),
            box_w - Inches(0.25),
            Inches(1.9),
            stage,
            font_size=13,
            bold=True,
            align=PP_ALIGN.CENTER,
        )
    add_textbox(
        slide,
        Inches(0.8),
        Inches(5.1),
        Inches(12.0),
        Inches(1.0),
        "ポイント: 依存症を単発の治療で捉えず、再発予防・家族支援・就労支援まで連続的に設計する。",
        font_size=17,
        color=RGBColor(198, 216, 243),
    )
    add_footer(slide, "7")


def add_strength_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_master_header(slide, "差別化要因: 8つの強み", "公式「相模原ダルクの強み」ページを要約")
    strengths = [
        "1) 10年超で延べ400名以上の回復支援実績",
        "2) 最新プログラム + 24時間見守り + 5段階ステージ制",
        "3) 定員約70名、関東圏最大規模クラスの設備",
        "4) 当事者経験を持つスタッフによる伴走支援",
        "5) 理事陣の専門性と安定運営",
        "6) 他機関プログラムへの監修・協力実績",
        "7) 地域活動・啓発・行政連携の継続",
        "8) 開設当初からの家族支援（家族会・相談）",
    ]
    add_bullets(
        slide,
        Inches(0.75),
        Inches(1.2),
        Inches(12.0),
        Inches(5.8),
        "8 ADVANTAGES",
        strengths,
        title_size=22,
        body_size=16,
    )
    add_footer(slide, "8")


def add_network_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_master_header(slide, "連携ネットワーク設計", "医療・行政・司法・地域・家族をつなぐ支援基盤")
    add_bullets(
        slide,
        Inches(0.75),
        Inches(1.25),
        Inches(3.8),
        Inches(5.5),
        "医療",
        ["依存症専門医療機関", "精神科・心療内科", "治療継続と再発予防連携"],
    )
    add_bullets(
        slide,
        Inches(4.75),
        Inches(1.25),
        Inches(3.8),
        Inches(5.5),
        "行政・司法",
        ["保健所・精神保健福祉センター", "保護観察所・矯正関連", "地域支援事業との接続"],
    )
    add_bullets(
        slide,
        Inches(8.75),
        Inches(1.25),
        Inches(3.8),
        Inches(5.5),
        "地域・家族",
        ["家族会・自助グループ", "地域啓発イベント", "卒業後フォローと居場所づくり"],
    )
    add_footer(slide, "9")


def add_kpi_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_master_header(slide, "KPIダッシュボード（提案）", "既存実績と運営指標を同時に可視化")
    add_bullets(
        slide,
        Inches(0.7),
        Inches(1.2),
        Inches(6.1),
        Inches(5.8),
        "アウトカム指標",
        [
            "支援人数（累計/年度）",
            "在寮中再使用率",
            "卒業後継続率（6か月/12か月）",
            "就労移行・定着率",
            "家族会継続参加率",
        ],
    )
    add_bullets(
        slide,
        Inches(7.05),
        Inches(1.2),
        Inches(5.55),
        Inches(5.8),
        "運営指標",
        [
            "初回相談件数と相談経路",
            "待機期間・入寮稼働率",
            "多機関連携件数（医療・行政・司法）",
            "再相談率と緊急介入件数",
            "支援満足度（本人/家族）",
        ],
    )
    add_footer(slide, "10")


def add_roadmap_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_master_header(
        slide,
        "実行ロードマップ（提案）",
        "支援品質向上・連携拡張・発信強化を同時推進",
    )
    add_bullets(
        slide,
        Inches(0.7),
        Inches(1.2),
        Inches(3.9),
        Inches(5.8),
        "Phase 1",
        ["相談導線の標準化", "初回面談テンプレート統一", "KPI定義と記録整備"],
    )
    add_bullets(
        slide,
        Inches(4.8),
        Inches(1.2),
        Inches(3.9),
        Inches(5.8),
        "Phase 2",
        ["家族支援コンテンツ強化", "連携機関との定例共有", "卒業者フォローの拡張"],
    )
    add_bullets(
        slide,
        Inches(8.9),
        Inches(1.2),
        Inches(3.9),
        Inches(5.8),
        "Phase 3",
        ["地域向け啓発の定期化", "成果レポート公開", "外部連携モデルの横展開"],
    )
    add_footer(slide, "11")


def add_contact_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_master_header(slide, "お問い合わせ", "初回相談無料・秘密厳守（公式案内）")
    add_bullets(
        slide,
        Inches(0.9),
        Inches(1.5),
        Inches(12.0),
        Inches(4.8),
        "連絡先",
        [
            "一般社団法人 相模原ダルク",
            "〒252-0237 神奈川県相模原市中央区千代田3-3-20",
            "TEL: 042-707-0391 / FAX: 042-707-0392",
            "営業時間: 平日 9:00-17:00 / 土・祝 9:00-14:00（日曜休）",
            "公式サイト: https://s-darc.com/",
        ],
        title_size=24,
        body_size=18,
    )
    add_textbox(
        slide,
        Inches(0.9),
        Inches(6.5),
        Inches(12.0),
        Inches(0.5),
        "CHANGE YOUR LIFE! 変われる。変われた仲間がいる。",
        font_size=18,
        bold=True,
        color=RGBColor(118, 239, 220),
    )
    add_footer(slide, "12")


def add_sources_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_master_header(slide, "出典", "公式サイト・公的機関公開情報（2026年4月参照）")
    sources = [
        "1. 相模原ダルク公式サイト: https://s-darc.com/",
        "2. 施設情報: https://s-darc.com/facility/",
        "3. 強み: https://s-darc.com/advantage/",
        "4. 問い合わせ: https://s-darc.com/contact/",
        "5. 警察庁 令和7年警察白書 第4節薬物銃器対策:",
        "   https://www.npa.go.jp/hakusyo/r07/honbun/html/bb4441000.html",
        "6. 厚生労働省 依存症対策:",
        "   https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000070789.html",
        "7. 参考資料(提供ファイル):",
        "   sagamihara_darc_presentation_2026_20260421013752.pdf",
        "   sagamihara_darc_presentation_2026_corporate_IR_redesign.pptx",
    ]
    add_bullets(
        slide,
        Inches(0.75),
        Inches(1.2),
        Inches(12.0),
        Inches(5.9),
        "References",
        sources,
        title_size=22,
        body_size=14,
    )
    add_footer(slide, "13")


def add_appendix_title(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_master_header(
        slide,
        "付録A: 提供資料の完全コピー",
        "以下18ページは提供PDFを画像化して順番通りにそのまま収録",
    )
    add_bullets(
        slide,
        Inches(0.9),
        Inches(1.7),
        Inches(11.9),
        Inches(4.6),
        "Appendix Notes",
        [
            "元資料の記載内容・構成を保持するため、各ページを全面画像として収録",
            "元資料: sagamihara_darc_presentation_2026_20260421013752.pdf (18ページ)",
            "この付録は『削除・改変なしで内容を残す』要件に対応",
        ],
        title_size=24,
        body_size=17,
    )
    add_footer(slide, "14")


def render_pdf_pages(pdf_path: Path, workdir: Path) -> list[Path]:
    workdir.mkdir(parents=True, exist_ok=True)
    pages: list[Path] = []
    with fitz.open(str(pdf_path)) as doc:
        for idx, page in enumerate(doc, start=1):
            # 解像度を上げることで投影時の視認性を確保
            pix = page.get_pixmap(matrix=fitz.Matrix(1.8, 1.8), alpha=False)
            out = workdir / f"ref_page_{idx:02d}.png"
            pix.save(str(out))
            pages.append(out)
    return pages


def add_copied_reference_slides(prs: Presentation, page_images: list[Path], start_page_num: int):
    page_no = start_page_num
    for image_path in page_images:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        slide.shapes.add_picture(str(image_path), Inches(0), Inches(0), width=SLIDE_W, height=SLIDE_H)
        page_no += 1


def build_presentation(reference_pdf: Path, output_path: Path, workdir: Path):
    if not reference_pdf.exists():
        raise FileNotFoundError(f"Reference PDF not found: {reference_pdf}")

    page_images = render_pdf_pages(reference_pdf, workdir)
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    # Part A: New enterprise-style storyline
    add_cover_slide(prs)
    add_executive_summary(prs)
    add_agenda(prs)
    add_environment_slide(prs)
    add_value_proposition_slide(prs)
    add_service_portfolio_slide(prs)
    add_recovery_process_slide(prs)
    add_strength_slide(prs)
    add_network_slide(prs)
    add_kpi_slide(prs)
    add_roadmap_slide(prs)
    add_contact_slide(prs)
    add_sources_slide(prs)

    # Part B: Full copied appendix from provided material
    add_appendix_title(prs)
    add_copied_reference_slides(prs, page_images, start_page_num=14)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output_path))


def main():
    args = parse_args()
    reference_pdf = Path(args.reference_pdf).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    workdir = Path(args.workdir).expanduser().resolve()
    build_presentation(reference_pdf, output_path, workdir)
    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
