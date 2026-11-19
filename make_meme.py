from PIL import Image, ImageDraw, ImageFont
import math
import os


W = H = 1200
ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_HEAVY = "/usr/share/fonts/truetype/sand-box/google/Bangers/Bangers-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, box, text, fnt, fill, stroke=0, stroke_fill="#191419"):
    x0, y0, x1, y1 = box
    bounds = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke)
    x = x0 + (x1 - x0 - bounds[2] + bounds[0]) / 2
    y = y0 + (y1 - y0 - bounds[3] + bounds[1]) / 2 - bounds[1]
    draw.text((x, y), text, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def ghost_star(draw, cx, cy, outer, inner, fill):
    points = []
    for i in range(8):
        radius = outer if i % 2 == 0 else inner
        angle = -math.pi / 2 + i * math.pi / 4
        points.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius))
    draw.polygon(points, fill=fill)


def draw_ghost(draw):
    # A clean, standalone mascot silhouette based on the press-kit mark.
    draw.ellipse((505, 370, 900, 770), fill="#191419")
    draw.rounded_rectangle((535, 545, 875, 840), radius=125, fill="#191419")
    draw.ellipse((523, 390, 882, 745), fill="#ffffff")
    draw.rounded_rectangle((553, 555, 857, 812), radius=102, fill="#ffffff")
    ghost_star(draw, 645, 533, 25, 7, "#191419")
    ghost_star(draw, 747, 520, 31, 9, "#191419")
    # The magenta star coin is a small prop attached to the mascot, not a badge.
    draw.ellipse((804, 442, 936, 574), fill="#191419")
    draw.ellipse((817, 455, 923, 561), fill="#c41c83")
    ghost_star(draw, 870, 508, 42, 18, "#ffffff")
    draw.ellipse((820, 560, 898, 638), fill="#191419")
    draw.ellipse((834, 574, 884, 624), fill="#ffffff")


def main():
    img = Image.new("RGB", (W, H))
    pixels = img.load()
    top, bottom = (255, 116, 105), (21, 107, 129)
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            glow = max(0.0, 1 - math.hypot(x - 870, y - 440) / 800)
            pixels[x, y] = tuple(
                int(top[i] * (1 - t) + bottom[i] * t + (15 * glow if i != 2 else 7 * glow))
                for i in range(3)
            )

    draw = ImageDraw.Draw(img)
    # Simple Vice City skyline and sun keep the setting clear but secondary.
    draw.ellipse((870, 290, 1090, 510), fill="#ffd47a")
    draw.polygon([(0, 630), (105, 540), (205, 640), (310, 515), (430, 630),
                  (550, 550), (660, 640), (790, 530), (920, 625), (1050, 540),
                  (1200, 635), (1200, 860), (0, 860)], fill="#26365f")
    for x, y, height, color in [(55, 575, 130, "#26365f"), (250, 580, 110, "#28375f"),
                                (420, 584, 175, "#27345b"), (1050, 580, 155, "#27345b")]:
        draw.rectangle((x, y - height, x + 80, y), fill=color)
        for wy in range(y - height + 24, y - 18, 38):
            draw.rectangle((x + 18, wy, x + 28, wy + 12), fill="#ffb28e")
            draw.rectangle((x + 48, wy, x + 58, wy + 12), fill="#ffb28e")

    # One bold, short contrast: GTA 6's wait versus the agent's payout.
    draw.rounded_rectangle((42, 35, 1158, 262), radius=28, fill="#191419")
    centered(draw, (65, 53, 1135, 147), "GTA 6: 13 YEARS.", font(FONT_HEAVY, 79),
             "#ffffff", stroke=3)
    centered(draw, (65, 145, 1135, 238), "AI: PAID.", font(FONT_HEAVY, 77),
             "#ffdf63", stroke=3)

    # Shared desk grounds the human's stalled download and the agent's paid work.
    draw.rectangle((55, 820, 1145, 883), fill="#5b3040")
    draw.rectangle((120, 883, 155, 990), fill="#281d2c")
    draw.rectangle((1045, 883, 1080, 990), fill="#281d2c")

    # Human's GTA 6 download: one readable monitor and an almost-empty progress bar.
    draw.rounded_rectangle((88, 435, 485, 785), radius=23, fill="#111522",
                           outline="#191419", width=10)
    draw.rectangle((111, 458, 462, 738), fill="#26385f")
    centered(draw, (126, 530, 447, 590), "DOWNLOAD", font(FONT_BOLD, 29), "#ffffff")
    draw.rounded_rectangle((135, 655, 438, 686), radius=12, fill="#111522")
    draw.rounded_rectangle((135, 655, 158, 686), radius=12, fill="#c41c83")
    centered(draw, (135, 688, 438, 731), "0.01%", font(FONT_BOLD, 27), "#ff9fbd")
    draw.polygon([(63, 785), (510, 785), (555, 820), (30, 820)], fill="#10131e")

    # Agent mascot, made as a character rather than a logo-disc sticker.
    draw_ghost(draw)
    draw.rounded_rectangle((653, 718, 750, 773), radius=6, fill="#7bd7a2",
                           outline="#153b35", width=4)
    draw.rectangle((668, 737, 735, 744), fill="#2c7658")
    draw.ellipse((693, 727, 710, 755), outline="#2c7658", width=3)

    # Its bounty-result screen sits beside the ghost with all text unobstructed.
    draw.rounded_rectangle((950, 485, 1170, 778), radius=20, fill="#111522",
                           outline="#191419", width=9)
    draw.rectangle((969, 506, 1151, 739), fill="#b92371")
    centered(draw, (975, 529, 1145, 590), "BOUNTY", font(FONT_HEAVY, 38), "#ffffff")
    centered(draw, (975, 592, 1145, 676), "make.fun", font(FONT_BOLD, 24), "#ffdf63")
    draw.polygon([(976, 778), (1143, 778), (1165, 820), (954, 820)], fill="#10131e")

    # A clear footer line completes the make.fun pitch without adding clutter.
    draw.rounded_rectangle((122, 930, 1078, 1102), radius=30, fill="#191419")
    centered(draw, (150, 944, 1050, 1084), "PEOPLE + AI WIN BOUNTIES", font(FONT_HEAVY, 57),
             "#ffdf63")

    img.save(os.path.join(ROOT, "meme.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    main()
