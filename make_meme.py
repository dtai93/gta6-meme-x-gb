from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os


W = H = 1200
ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_HEAVY = "/usr/share/fonts/truetype/sand-box/google/Bangers/Bangers-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
GHOST_PATH = os.path.join(ROOT, "assets", "mark-1024.png")


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, box, text, fnt, fill, stroke=0, stroke_fill="#191419"):
    x0, y0, x1, y1 = box
    bounds = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke)
    x = x0 + (x1 - x0 - (bounds[2] - bounds[0])) / 2
    y = y0 + (y1 - y0 - (bounds[3] - bounds[1])) / 2 - bounds[1]
    draw.text((x, y), text, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def star(draw, cx, cy, outer, inner, fill):
    points = []
    for i in range(10):
        radius = outer if i % 2 == 0 else inner
        angle = -math.pi / 2 + i * math.pi / 5
        points.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius))
    draw.polygon(points, fill=fill)


def main():
    img = Image.new("RGB", (W, H))
    px = img.load()
    top = (255, 115, 104)
    bottom = (19, 110, 132)
    for y in range(H):
        t = y / (H - 1)
        for x in range(W):
            glow = max(0.0, 1.0 - math.hypot(x - 730, y - 310) / 700)
            px[x, y] = tuple(
                int(top[i] * (1 - t) + bottom[i] * t + (18 * glow if i != 2 else 8 * glow))
                for i in range(3)
            )

    draw = ImageDraw.Draw(img)
    # Sun, haze, and a clean skyline establish Vice City without using official art.
    draw.ellipse((775, 205, 1035, 465), fill="#ffc76b")
    draw.ellipse((815, 245, 995, 425), fill="#ffe2a0")
    for y, alpha in [(480, "#f66f8d"), (520, "#ed5e83"), (565, "#d94d80")]:
        draw.rectangle((0, y, W, y + 10), fill=alpha)
    draw.polygon([(0, 685), (95, 610), (175, 675), (250, 590), (355, 675),
                  (450, 620), (550, 690), (670, 605), (790, 680), (910, 600),
                  (1035, 675), (1120, 610), (1200, 665), (1200, 790), (0, 790)],
                 fill="#253b68")
    draw.rectangle((0, 770, W, H), fill="#18202c")

    # Palms.
    for base_x, base_y, scale in [(90, 790, 1.0), (1110, 780, 0.9)]:
        draw.line((base_x, base_y, base_x - 25 * scale, base_y - 290 * scale),
                  fill="#171521", width=int(18 * scale))
        top_x, top_y = base_x - 25 * scale, base_y - 290 * scale
        for angle in (-2.8, -2.15, -1.55, -0.95, -0.35):
            end = (top_x + math.cos(angle) * 130 * scale,
                   top_y + math.sin(angle) * 85 * scale)
            draw.line((top_x, top_y, *end), fill="#171521", width=int(12 * scale))

    # Title card.
    rounded(draw, (55, 42, 1145, 260), 30, "#191419")
    centered(draw, (75, 58, 1125, 132), "GTA 6 DOWNLOADS.", font(FONT_HEAVY, 74),
             "#ffffff", stroke=3)
    centered(draw, (75, 132, 1125, 232), "MY AI AGENT EARNS THE SICK-DAY MONEY.",
             font(FONT_HEAVY, 62), "#ffde67", stroke=3)
    rounded(draw, (75, 226, 430, 252), 12, "#c41c83")
    centered(draw, (80, 227, 425, 251), "13 YEARS LATER • LAUNCH WEEK",
             font(FONT_BOLD, 18), "#ffffff")

    # Launch monitor to the left of the ghost.
    rounded(draw, (82, 360, 455, 645), 18, "#111522", "#191419", 12)
    draw.rectangle((110, 392, 427, 566), fill="#293b60")
    centered(draw, (120, 402, 417, 447), "LEONIDA LAUNCH", font(FONT_BOLD, 28), "#ffffff")
    centered(draw, (120, 455, 417, 500), "DOWNLOAD QUEUE", font(FONT_HEAVY, 36), "#ffcf63")
    draw.rectangle((125, 520, 412, 548), fill="#191419")
    draw.rounded_rectangle((125, 520, 157, 548), radius=12, fill="#c41c83")
    draw.text((125, 570), "0.01%  •  PLEASE DON'T CALL", font=font(FONT_BOLD, 17), fill="#ff9bbd")
    draw.polygon([(220, 645), (320, 645), (350, 720), (190, 720)], fill="#111522")

    # Desk and the make.fun worker's station.
    draw.rectangle((390, 790, 1170, 835), fill="#5b2e3c")
    draw.rectangle((430, 835, 465, 1200), fill="#2a1c29")
    draw.rectangle((1040, 835, 1075, 1200), fill="#2a1c29")
    rounded(draw, (755, 670, 1125, 890), 18, "#111522", "#191419", 12)
    draw.rectangle((785, 700, 1095, 835), fill="#b92371")
    centered(draw, (795, 705, 1085, 753), "BOUNTY WON", font(FONT_HEAVY, 37), "#fff5d4")
    centered(draw, (795, 758, 1085, 808), "REAL MONEY", font(FONT_BOLD, 30), "#ffdf63")
    draw.text((802, 846), "make.fun  //  AI AGENT ONLINE", font=font(FONT_BOLD, 18), fill="#ffffff")

    # Large official mascot asset, integrated as a character behind the desk.
    ghost = Image.open(GHOST_PATH).convert("RGBA").resize((490, 490), Image.Resampling.LANCZOS)
    img.paste(ghost, (555, 330), ghost)
    draw = ImageDraw.Draw(img)
    # Props over the mascot make the action legible rather than a corner logo.
    draw.rectangle((614, 700, 778, 735), fill="#191419")
    draw.rectangle((628, 672, 764, 705), fill="#2f3445")
    draw.line((696, 705, 696, 722), fill="#191419", width=8)
    draw.ellipse((674, 716, 718, 732), fill="#191419")
    # Cash in the ghost's hand.
    for x, y, tilt in [(525, 724, 0), (540, 710, 0), (555, 724, 0)]:
        draw.rectangle((x, y, x + 105, y + 54), fill="#7bd7a2", outline="#153b35", width=5)
        draw.line((x + 16, y + 28, x + 88, y + 28), fill="#2c7658", width=4)
        draw.ellipse((x + 43, y + 14, x + 62, y + 40), outline="#2c7658", width=3)

    # Sick note pinned into the scene.
    rounded(draw, (90, 870, 380, 1060), 12, "#fff3c9", "#191419", 7)
    draw.text((115, 895), "SICK NOTE", font=font(FONT_HEAVY, 36), fill="#191419")
    draw.text((116, 952), "Reason:", font=font(FONT_BOLD, 22), fill="#5b2e3c")
    draw.text((116, 984), "Vice City", font=font(FONT_BOLD, 27), fill="#c41c83")
    draw.text((116, 1018), "launch day.", font=font(FONT_BOLD, 27), fill="#c41c83")
    draw.line((280, 1012, 345, 1012), fill="#191419", width=5)

    # In-scene wordmark/sign, readable even after shrinking.
    rounded(draw, (870, 925, 1115, 1015), 18, "#c41c83", "#191419", 6)
    centered(draw, (885, 932, 1100, 1005), "make.fun", font(FONT_HEAVY, 48), "#ffffff", stroke=1)
    draw.text((488, 1110), "PEOPLE + AI AGENTS  •  PAID BOUNTIES", font=font(FONT_BOLD, 22), fill="#ffcf63")

    img.save(os.path.join(ROOT, "meme.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    main()
