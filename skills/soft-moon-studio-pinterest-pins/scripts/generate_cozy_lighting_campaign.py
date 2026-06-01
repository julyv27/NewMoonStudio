#!/usr/bin/env python3
from __future__ import annotations

import csv
import base64
import html
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN = ROOT / "campaigns" / "pinterest" / "cozy-lighting-ideas"
SVG_DIR = CAMPAIGN / "source-svg"
PNG_DIR = CAMPAIGN / "pins"
STATIC = ROOT / "static" / "img" / "blog" / "cozy-lighting"

PINS = [
    {
        "id": "pin-01",
        "style": "cream-card",
        "image": "cover-cozy-bedroom.jpg",
        "kicker": "COZY HOME GUIDE",
        "headline": ["9 Cozy Lighting Ideas", "for Softer Evenings"],
        "subline": "simple ways to make your home feel warmer at night",
    },
    {
        "id": "pin-02",
        "style": "dark-overlay",
        "image": "floor-lamp.jpg",
        "kicker": "SOFT MOON STUDIO",
        "headline": ["Skip the", "Overhead Light"],
        "subline": "9 softer lighting ideas for a calmer home",
    },
    {
        "id": "pin-03",
        "style": "split",
        "image": "cover-cozy-bedroom.jpg",
        "image2": "fairy-lights-cozy-interior.jpg",
        "kicker": "BEDROOM LIGHTING IDEAS",
        "headline": ["Make Your Bedroom", "Feel Softer at Night"],
        "subline": "warm, cozy lighting inspiration",
    },
    {
        "id": "pin-04",
        "style": "cream-card",
        "image": "wall-sconce.jpg",
        "kicker": "RENTER-FRIENDLY HOME IDEAS",
        "headline": ["Cozy Lighting Ideas", "for Renters"],
        "subline": "soft lighting without a full room makeover",
    },
    {
        "id": "pin-05",
        "style": "dark-overlay",
        "image": "flameless-candles.jpg",
        "kicker": "EASY EVENING UPDATE",
        "headline": ["Small Lights,", "Softer Evenings"],
        "subline": "9 cozy ways to layer warm light at home",
    },
    {
        "id": "pin-06",
        "style": "split",
        "image": "floor-lamp.jpg",
        "image2": "paper-lantern.jpg",
        "kicker": "COZY HOME DECOR",
        "headline": ["9 Warm Lighting Ideas", "for a Cozy Home"],
        "subline": "from reading corners to gentle statement lights",
    },
    {
        "id": "pin-07",
        "style": "cream-card",
        "image": "fairy-lights-cozy-interior.jpg",
        "kicker": "SMALL-SPACE LIGHTING",
        "headline": ["Cozy Lighting Ideas", "for Small Spaces"],
        "subline": "warmth without adding clutter",
    },
    {
        "id": "pin-08",
        "style": "dark-overlay",
        "image": "paper-lantern.jpg",
        "kicker": "SOFT HOME AESTHETIC",
        "headline": ["How to Layer", "Warm Light at Night"],
        "subline": "simple ideas for a calmer evening atmosphere",
    },
    {
        "id": "pin-09",
        "style": "split",
        "image": "cover-cozy-bedroom.jpg",
        "image2": "wall-sconce.jpg",
        "kicker": "COZY BEDROOM DETAILS",
        "headline": ["Soft Lighting Ideas", "for a Cozy Bedside"],
        "subline": "small changes that make evenings feel gentler",
    },
    {
        "id": "pin-10",
        "style": "cream-card",
        "image": "floor-lamp.jpg",
        "kicker": "READING CORNER INSPIRATION",
        "headline": ["Create a Softer", "Reading Corner"],
        "subline": "warm lighting ideas for quiet evenings",
    },
    {
        "id": "pin-11",
        "style": "dark-overlay",
        "image": "cover-cozy-bedroom.jpg",
        "kicker": "COZY HOME CHECKLIST",
        "headline": ["Your Home Feels Harsh", "After Dark?"],
        "headline_size": 76,
        "subline": "try these 9 softer lighting ideas",
    },
    {
        "id": "pin-12",
        "style": "split",
        "image": "flameless-candles.jpg",
        "image2": "fairy-lights-cozy-interior.jpg",
        "kicker": "SOFT EVENING RITUALS",
        "headline": ["9 Gentle Ways", "to Light Your Evenings"],
        "subline": "cozy ideas for shelves, bedrooms and reading corners",
    },
]


def esc(text: str) -> str:
    return html.escape(text)


def image_uri(name: str) -> str:
    data = base64.b64encode((STATIC / name).read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{data}"


def text_lines(lines: list[str], y: int, size: int, color: str, family: str, weight: int = 400, gap: int = 86) -> str:
    out = []
    for i, line in enumerate(lines):
        out.append(
            f'<text x="500" y="{y + i * gap}" text-anchor="middle" '
            f'fill="{color}" font-family="{family}" font-size="{size}" font-weight="{weight}">{esc(line)}</text>'
        )
    return "\n".join(out)


def base_defs() -> str:
    return """
  <defs>
    <linearGradient id="shade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1d1712" stop-opacity="0.16"/>
      <stop offset="58%" stop-color="#1d1712" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#1d1712" stop-opacity="0.84"/>
    </linearGradient>
    <linearGradient id="bottomShade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2f241d" stop-opacity="0"/>
      <stop offset="100%" stop-color="#2f241d" stop-opacity="0.74"/>
    </linearGradient>
  </defs>
"""


def brand(color: str, y: int = 1430) -> str:
    return (
        f'<text x="500" y="{y}" text-anchor="middle" fill="{color}" '
        'font-family="Avenir Next, Arial, sans-serif" font-size="24" '
        'letter-spacing="10">SOFT MOON STUDIO</text>'
    )


def cream_card(pin: dict[str, object]) -> str:
    headline = text_lines(pin["headline"], 1055, pin.get("headline_size", 70), "#3b3029", "Georgia, serif", gap=82)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1500" viewBox="0 0 1000 1500">
{base_defs()}
  <image href="{image_uri(pin["image"])}" width="1000" height="1500" preserveAspectRatio="xMidYMid slice"/>
  <rect width="1000" height="1500" fill="url(#bottomShade)"/>
  <rect x="58" y="900" width="884" height="500" rx="26" fill="#f2eee7" fill-opacity="0.96"/>
  <text x="500" y="970" text-anchor="middle" fill="#8b6d5d" font-family="Avenir Next, Arial, sans-serif" font-size="24" font-weight="600" letter-spacing="5">{esc(pin["kicker"])}</text>
  {headline}
  <line x1="390" y1="1212" x2="610" y2="1212" stroke="#b89d8d" stroke-width="2"/>
  <text x="500" y="1272" text-anchor="middle" fill="#67564c" font-family="Avenir Next, Arial, sans-serif" font-size="29">{esc(pin["subline"])}</text>
  {brand("#67564c", 1350)}
</svg>
"""


def dark_overlay(pin: dict[str, object]) -> str:
    headline = text_lines(pin["headline"], 575, pin.get("headline_size", 94), "#fffaf2", "Georgia, serif", gap=108)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1500" viewBox="0 0 1000 1500">
{base_defs()}
  <image href="{image_uri(pin["image"])}" width="1000" height="1500" preserveAspectRatio="xMidYMid slice"/>
  <rect width="1000" height="1500" fill="url(#shade)"/>
  <text x="500" y="475" text-anchor="middle" fill="#f3dfcf" font-family="Avenir Next, Arial, sans-serif" font-size="25" font-weight="600" letter-spacing="6">{esc(pin["kicker"])}</text>
  {headline}
  <line x1="360" y1="825" x2="640" y2="825" stroke="#efdcca" stroke-width="2"/>
  <text x="500" y="895" text-anchor="middle" fill="#fffaf2" font-family="Avenir Next, Arial, sans-serif" font-size="30">{esc(pin["subline"])}</text>
  {brand("#fffaf2")}
</svg>
"""


def split(pin: dict[str, object]) -> str:
    headline = text_lines(pin["headline"], 255, pin.get("headline_size", 72), "#3b3029", "Georgia, serif", gap=84)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1500" viewBox="0 0 1000 1500">
{base_defs()}
  <rect width="1000" height="1500" fill="#f2eee7"/>
  <text x="500" y="150" text-anchor="middle" fill="#8b6d5d" font-family="Avenir Next, Arial, sans-serif" font-size="24" font-weight="600" letter-spacing="5">{esc(pin["kicker"])}</text>
  {headline}
  <text x="500" y="480" text-anchor="middle" fill="#67564c" font-family="Avenir Next, Arial, sans-serif" font-size="28">{esc(pin["subline"])}</text>
  <image href="{image_uri(pin["image"])}" x="50" y="570" width="430" height="760" preserveAspectRatio="xMidYMid slice"/>
  <image href="{image_uri(pin["image2"])}" x="520" y="570" width="430" height="760" preserveAspectRatio="xMidYMid slice"/>
  <rect x="50" y="570" width="430" height="760" fill="none" stroke="#d5c8bd" stroke-width="4"/>
  <rect x="520" y="570" width="430" height="760" fill="none" stroke="#d5c8bd" stroke-width="4"/>
  {brand("#67564c", 1425)}
</svg>
"""


def render_svg(svg_path: Path, png_path: Path) -> None:
    png_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "swift",
            str(Path(__file__).with_name("render_svg.swift")),
            str(svg_path),
            str(png_path),
        ],
        check=True,
    )


def main() -> None:
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    styles = {"cream-card": cream_card, "dark-overlay": dark_overlay, "split": split}
    for pin in PINS:
        svg_path = SVG_DIR / f'{pin["id"]}.svg'
        png_path = PNG_DIR / f'{pin["id"]}.png'
        svg_path.write_text(styles[pin["style"]](pin), encoding="utf-8")
        render_svg(svg_path, png_path)
        print(png_path.relative_to(ROOT))
if __name__ == "__main__":
    main()
