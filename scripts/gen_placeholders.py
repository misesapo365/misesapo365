#!/usr/bin/env python3
"""Generate LP slice placeholders (repo lacked binary assets)."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SPECS = [
    ("01_first_view.png", (1726, 1000), "ファーストビュー", "#fff8e7"),
    ("03_problem_recommend.png", (1726, 440), "お悩み・推奨", "#fff0dc"),
    ("04_benefits_services.png", (1726, 496), "できること", "#e8f4ff"),
    ("05_price_offer.png", (1726, 328), "料金", "#f5ffe8"),
    ("06_flow.png", (1726, 392), "ご利用の流れ", "#fce8ff"),
    ("07_final_cta_footer.png", (1726, 630), "CTA・フッター", "#ffe8e8"),
]


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for name, (w, h), label, bg in SPECS:
        im = Image.new("RGB", (w, h), bg)
        draw = ImageDraw.Draw(im)
        try:
            font_large = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 72)
            font_small = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc", 36)
        except OSError:
            font_large = ImageFont.load_default()
            font_small = font_large
        draw.rectangle([0, 0, w, 12], fill="#f7b500")
        tw, th = draw.textbbox((0, 0), label, font=font_large)[2:]
        draw.text(((w - tw) // 2, (h - th) // 2 - 40), label, fill="#222", font=font_large)
        sub = "プレースホルダー（本番画像に差し替え可）"
        tw2, th2 = draw.textbbox((0, 0), sub, font=font_small)[2:]
        draw.text(((w - tw2) // 2, (h - th) // 2 + 50), sub, fill="#555", font=font_small)
        out = ASSETS / name
        im.save(out, "PNG", optimize=True)
        print(out, out.stat().st_size)


if __name__ == "__main__":
    main()
