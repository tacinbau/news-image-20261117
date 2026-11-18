"""Draw a compact, text-first broadsheet for the 17 November news brief."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1024
HEIGHT = 1024
PAPER = (250, 248, 241)
INK = (23, 22, 20)
MUTED = (94, 91, 85)
RULE = (135, 35, 39)
HAIRLINE = (193, 188, 177)
FONT_DIR = Path("/usr/share/fonts/truetype/noto")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size=size)


def wrap(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        test = f"{line} {word}".strip()
        if line and draw.textlength(test, font=face) > width:
            lines.append(line)
            line = word
        else:
            line = test
    if line:
        lines.append(line)
    return lines


def paragraph(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    face: ImageFont.FreeTypeFont,
    width: int,
    fill: tuple[int, int, int] = INK,
    leading: int = 27,
) -> int:
    x, y = xy
    for line in wrap(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=fill)
        y += leading
    return y


def section(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    width: int,
    kicker: str,
    headline: str,
    summary: str,
    body_size: int = 20,
) -> int:
    kicker_face = font("NotoSans-Bold.ttf", 18)
    headline_face = font("NotoSerif-Bold.ttf", 30)
    body_face = font("NotoSans-Regular.ttf", body_size)
    draw.text((x, y), kicker.upper(), font=kicker_face, fill=RULE)
    y += 25
    for line in wrap(draw, headline, headline_face, width):
        draw.text((x, y), line, font=headline_face, fill=INK)
        y += 36
    y += 3
    return paragraph(draw, summary, (x, y), body_face, width, leading=25)


def draw_bridge(draw: ImageDraw.ImageDraw) -> None:
    """Add a small original line illustration beneath the lead summary."""
    y = 436
    draw.line((100, y, 924, y), fill=(83, 80, 74), width=3)
    draw.line((132, y - 4, 132, y + 17), fill=(83, 80, 74), width=3)
    draw.line((892, y - 4, 892, y + 17), fill=(83, 80, 74), width=3)
    for left, right, peak in ((170, 470, 409), (554, 854, 409)):
        draw.line((left, y - 2, (left + right) // 2, peak), fill=(83, 80, 74), width=3)
        draw.line(((left + right) // 2, peak, right, y - 2), fill=(83, 80, 74), width=3)
        draw.line((left, y - 2, left, y + 17), fill=(83, 80, 74), width=2)
        draw.line((right, y - 2, right, y + 17), fill=(83, 80, 74), width=2)
    for x in range(202, 825, 42):
        draw.line((x, y - 2, x, y + 9), fill=(120, 116, 107), width=1)


def main() -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(image)

    margin = 56
    draw.text((margin, 30), "THE WORLD LEDGER", font=font("NotoSerif-Black.ttf", 50), fill=INK)
    draw.text((731, 55), "WORLD NEWS  /  NO. 17", font=font("NotoSans-Bold.ttf", 18), fill=MUTED)
    draw.rectangle((margin, 101, WIDTH - margin, 107), fill=RULE)
    draw.text((margin, 120), "TUESDAY, 17 NOVEMBER 2026", font=font("NotoSans-Bold.ttf", 36), fill=INK)
    draw.text((775, 132), "THE DAILY BRIEF", font=font("NotoSans-Regular.ttf", 18), fill=MUTED)
    draw.line((margin, 174, WIDTH - margin, 174), fill=HAIRLINE, width=2)

    draw.text((margin, 190), "THE LEAD  /  EASTERN EUROPE", font=font("NotoSans-Bold.ttf", 19), fill=RULE)
    headline_face = font("NotoSerif-Bold.ttf", 45)
    lead_lines = wrap(draw, "Ukraine strikes Kerch Bridge; Kyiv says link severely damaged", headline_face, 900)
    y = 218
    for line in lead_lines:
        draw.text((margin, y), line, font=headline_face, fill=INK)
        y += 53
    body_face = font("NotoSans-Regular.ttf", 22)
    y += 2
    y = paragraph(
        draw,
        "Traffic on the Crimea–Russia link was suspended. Russia struck bridges in Kyiv in return.",
        (margin, y),
        body_face,
        900,
        leading=29,
    )
    draw_bridge(draw)
    draw.line((margin, 468, WIDTH - margin, 468), fill=INK, width=2)

    col_gap = 36
    col_width = (WIDTH - 2 * margin - col_gap) // 2
    left = margin
    right = margin + col_width + col_gap
    draw.line((512, 480, 512, 868), fill=HAIRLINE, width=1)

    section(
        draw,
        left,
        480,
        col_width - 4,
        "Diplomacy",
        "Trump, Xi and Putin set for summit",
        "Trump heads to Asia for a rare trilateral summit with Xi Jinping and Vladimir Putin.",
    )
    section(
        draw,
        right,
        480,
        col_width - 4,
        "Middle East",
        "Allies press Israel; UK sanctions firms",
        "UK, Australia, Canada and Italy urge Israel to open Gaza crossings for aid; Britain sanctions eight Israeli settlement firms over West Bank settlements. Israel calls sanctions hostile.",
        body_size=18,
    )
    draw.line((margin, 690, WIDTH - margin, 690), fill=HAIRLINE, width=1)
    section(
        draw,
        left,
        707,
        col_width - 4,
        "Japan",
        "Japan scrambles jets over suspected breach",
        "Japan scrambles fighter jets after suspected Russian aircraft violate its airspace.",
    )
    section(
        draw,
        right,
        707,
        col_width - 4,
        "Markets",
        "AI leads losses; Bitcoin stalls",
        "AI stocks lead Wall Street losses ahead of Nvidia earnings; Bitcoin stalls below $65,000 after a selloff.",
    )
    draw.line((margin, 868, WIDTH - margin, 868), fill=HAIRLINE, width=1)
    section(
        draw,
        margin,
        885,
        WIDTH - 2 * margin,
        "Culture  /  France",
        "Depardieu drops appeal in Paris court",
        "French actor Gerard Depardieu admits a sexual assault charge in a Paris court.",
    )
    draw.line((margin, 986, WIDTH - margin, 986), fill=RULE, width=3)

    image.save(Path(__file__).with_name("entry.png"), format="PNG", optimize=False, compress_level=9)


if __name__ == "__main__":
    main()
