#!/usr/bin/env python3
from __future__ import annotations

import base64
import html
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN = ROOT / "campaigns" / "pinterest" / "emotional-safety-home"
SVG_DIR = CAMPAIGN / "source-svg"
PNG_DIR = CAMPAIGN / "pins"
IMAGE = ROOT / "static" / "img" / "blog" / "lamp-blog.jpg"


def esc(text: str) -> str:
    return html.escape(text)


def image_uri(path: Path) -> str:
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{data}"


def svg() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1500" viewBox="0 0 1000 1500">
  <defs>
    <linearGradient id="shade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#251712" stop-opacity="0.10"/>
      <stop offset="45%" stop-color="#251712" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#251712" stop-opacity="0.82"/>
    </linearGradient>
    <linearGradient id="topWarmth" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f0c8a2" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#f0c8a2" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <image href="{image_uri(IMAGE)}" width="1000" height="1500" preserveAspectRatio="xMidYMid slice"/>
  <rect width="1000" height="1500" fill="url(#shade)"/>
  <rect width="1000" height="1500" fill="url(#topWarmth)"/>

  <rect x="70" y="130" width="860" height="510" rx="28" fill="#f2eee7" fill-opacity="0.93"/>
  <text x="500" y="225" text-anchor="middle" fill="#8b6d5d" font-family="Avenir Next, Arial, sans-serif" font-size="25" font-weight="600" letter-spacing="6">{esc("CALM HOME AESTHETIC")}</text>
  <text x="500" y="330" text-anchor="middle" fill="#3b3029" font-family="Georgia, serif" font-size="77">{esc("How to Make")}</text>
  <text x="500" y="420" text-anchor="middle" fill="#3b3029" font-family="Georgia, serif" font-size="77">{esc("Your Home Feel")}</text>
  <text x="500" y="510" text-anchor="middle" fill="#3b3029" font-family="Georgia, serif" font-size="77">{esc("Emotionally Safer")}</text>
  <line x1="365" y1="562" x2="635" y2="562" stroke="#b89d8d" stroke-width="2"/>
  <text x="500" y="605" text-anchor="middle" fill="#67564c" font-family="Avenir Next, Arial, sans-serif" font-size="27">{esc("soft lighting, slower evenings and tiny rituals")}</text>

  <text x="500" y="1430" text-anchor="middle" fill="#fffaf2" font-family="Avenir Next, Arial, sans-serif" font-size="24" letter-spacing="10">{esc("SOFT MOON STUDIO")}</text>
</svg>
"""


def main() -> None:
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    svg_path = SVG_DIR / "context-pin-01.svg"
    png_path = PNG_DIR / "context-pin-01.png"
    svg_path.write_text(svg(), encoding="utf-8")
    subprocess.run(
        [
            "swift",
            str(Path(__file__).with_name("render_svg.swift")),
            str(svg_path),
            str(png_path),
        ],
        check=True,
    )
    print(png_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
