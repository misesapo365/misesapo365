#!/usr/bin/env python3
"""Edit LP slice PNGs: footer branding, price strip (remove 3rd item, zoom price)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    paths = (
        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
        "/System/Library/Fonts/Supplement/ヒラギノ角ゴシック W6.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc",
    )
    for path in paths:
        try:
            return ImageFont.truetype(path, size, index=0)
        except OSError:
            continue
    return ImageFont.load_default()


def edit_price(path: Path) -> None:
    im = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(im)
    # Remove third feature (契約期間はご相談)
    draw.rectangle((656, 12, 862, 158), fill=(252, 200, 28))

    # Zoom price headline inside white card
    box = (72, 22, 338, 112)
    inner = im.crop(box)
    scale = 1.16
    sw = max(1, int(inner.width * scale))
    sh = max(1, int(inner.height * scale))
    scaled = inner.resize((sw, sh), Image.Resampling.LANCZOS)
    dw, dh = box[2] - box[0], box[3] - box[1]
    cx, cy = sw // 2, sh // 2
    left = max(0, cx - dw // 2)
    top = max(0, cy - dh // 2)
    if left + dw > sw:
        left = sw - dw
    if top + dh > sh:
        top = sh - dh
    zoomed = scaled.crop((left, top, left + dw, top + dh))
    im.paste(zoomed, (box[0], box[1]))
    im.save(path, "PNG", optimize=True)


def edit_footer(path: Path) -> None:
    im = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(im)
    font = _load_font(21)
    label = "ミセサポ365"
    tw = int(draw.textlength(label, font=font))
    pad_x, pad_y = 4, 3
    x0, y0, x1, y1 = 96, 200, 98 + tw + pad_x * 2, 232
    draw.rectangle((x0, y0, x1, y1), fill=(255, 255, 255))
    draw.text((x0 + pad_x, y0 + pad_y), label, fill=(34, 34, 34), font=font)

    # Copyright strip — repaint band then centered text
    band_y0, band_y1 = 270, 296
    strip_fill = (253, 253, 251)
    draw.rectangle((0, band_y0, im.width - 1, band_y1), fill=strip_fill)
    small = _load_font(12)
    text = "© 2025 ミセサポ365 All Rights Reserved."
    tw = int(draw.textlength(text, font=small))
    tx = (im.width - tw) // 2
    ty = band_y0 + (band_y1 - band_y0 - 14) // 2
    draw.text((tx, ty), text, fill=(88, 88, 86), font=small)
    im.save(path, "PNG", optimize=True)


def main() -> None:
    assets = ROOT / "assets"
    edit_price(assets / "05_price_offer.png")
    edit_footer(assets / "07_final_cta_footer.png")
    print("Updated:", assets / "05_price_offer.png", assets / "07_final_cta_footer.png")


if __name__ == "__main__":
    main()
