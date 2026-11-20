#!/usr/bin/env python3
"""GTA 6 launch-night trophy stack. Writes meme-trophies.png."""

import math
import os
from PIL import Image, ImageChops, ImageDraw, ImageFont

W = H = 1200
ROOT = os.path.dirname(os.path.abspath(__file__))
MARK = os.path.join(ROOT, "assets", "mark-1024.png")
OUT = os.path.join(ROOT, "meme-trophies.png")
FB = "/usr/share/fonts/truetype/sand-box/google"
F_DISP = f"{FB}/Archivo Black/ArchivoBlack-Regular.ttf"
F_BOLD = f"{FB}/Poppins/Poppins-Bold.ttf"
F_SEMI = f"{FB}/Poppins/Poppins-SemiBold.ttf"
F_MED = f"{FB}/Poppins/Poppins-Medium.ttf"

METAL = {
    "PLATINUM": dict(fill=(176, 230, 242), light=(255, 255, 255), dark=(90, 148, 166),
                     edge=(10, 44, 58), pill=(190, 238, 248), ink=(8, 40, 54)),
    "GOLD": dict(fill=(240, 186, 60), light=(255, 236, 170), dark=(150, 100, 16),
                 edge=(48, 32, 6), pill=(255, 210, 96), ink=(48, 32, 4)),
    "SILVER": dict(fill=(208, 212, 220), light=(255, 255, 255), dark=(122, 128, 140),
                   edge=(30, 34, 42), pill=(230, 232, 238), ink=(28, 32, 40)),
    "BRONZE": dict(fill=(198, 124, 66), light=(238, 190, 136), dark=(124, 70, 30),
                   edge=(42, 22, 8), pill=(216, 148, 92), ink=(42, 24, 8)),
}

CARDS = [
    dict(grade="PLATINUM", name="Patience",
         desc="13 years of delays. Still on the install bar.",
         rarity="100% of players"),
    dict(grade="BRONZE", name="Storage Wars",
         desc="Paid $80, then deleted every other game.",
         rarity="71.2% of players"),
    dict(grade="SILVER", name="Out Sick",
         desc="Three sick days. The preload isn't finished.",
         rarity="94.7% of players"),
    dict(grade="GOLD", name="Florida Energy",
         desc="Jason and Lucia hit five stars in Leonida.",
         rarity="18.4% of players"),
    dict(grade="GOLD", name="Passive Income",
         desc="Won a bounty. You hadn't moved in 72 hours.",
         rarity="0.6% of players", ghost=True, chip="$ earned"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky_color(t):
    stops = [
        (0.00, (16, 10, 52)),
        (0.16, (72, 22, 92)),
        (0.34, (188, 52, 108)),
        (0.48, (240, 96, 74)),
        (0.60, (255, 170, 82)),
        (0.72, (28, 136, 138)),
        (0.86, (10, 64, 78)),
        (1.00, (4, 20, 30)),
    ]
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if t <= t1:
            u = 0 if t1 == t0 else (t - t0) / (t1 - t0)
            return lerp(c0, c1, u)
    return stops[-1][1]


def blit(base, layer, xy=(0, 0)):
    base.alpha_composite(layer, xy)


def draw_sky(img):
    draw = ImageDraw.Draw(img)
    for y in range(H):
        draw.line([(0, y), (W, y)], fill=sky_color(y / (H - 1)))


def glow_circle(base, cx, cy, radius, color, alpha):
    layer = Image.new("RGBA", (radius * 2, radius * 2), (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse((0, 0, radius * 2 - 1, radius * 2 - 1), fill=(*color, alpha))
    blit(base, layer, (int(cx - radius), int(cy - radius)))


def draw_sun(base):
    cx, cy = 1048, 148
    for rad, col, alpha in (
        (230, (255, 150, 80), 26),
        (150, (255, 186, 110), 48),
        (92, (255, 214, 150), 100),
        (52, (255, 244, 220), 245),
    ):
        glow_circle(base, cx, cy, rad, col, alpha)


def frond(draw, x, y, ang, length, width, color):
    rad = math.radians(ang)
    dx, dy = math.cos(rad), -math.sin(rad)
    px, py = -dy, dx
    ex, ey = x + dx * length, y + dy * length
    mx, my = x + dx * length * 0.52, y + dy * length * 0.62 - 8
    draw.polygon(
        [(x, y), (mx + px * width, my + py * width), (ex, ey), (mx - px * width, my - py * width)],
        fill=color,
    )


def draw_palm(layer, bx, by, lean, height, color, angles):
    draw = ImageDraw.Draw(layer)
    cx, cy = bx + lean, by - height
    draw.polygon([(bx - 16, by), (bx + 14, by), (cx + 8, cy + 4), (cx - 8, cy + 4)], fill=color)
    for i, ang in enumerate(angles):
        frond(draw, cx, cy, ang, height * (0.42 + (i % 3) * 0.05), 8, color)


def palm_layer():
    """Edge silhouettes only. The stack knocks the middle out so fronds never cross type."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ink = (7, 14, 20, 235)
    draw_palm(layer, -30, 1280, 16, 520, ink, range(25, 155, 14))
    draw_palm(layer, 1228, 1300, -20, 560, ink, range(20, 160, 13))
    draw_palm(layer, 20, 360, 8, 240, ink, range(15, 130, 16))
    draw_palm(layer, 1160, 250, -8, 175, ink, range(18, 96, 13))
    draw_palm(layer, 280, 1260, 0, 150, ink, range(30, 155, 20))
    draw_palm(layer, 900, 1270, 0, 160, ink, range(25, 160, 18))
    return layer


def trophy_icon(size, metal):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = size
    fill, hi, dark, edge = metal["fill"], metal["light"], metal["dark"], metal["edge"]
    lw = max(4, s // 14)
    d.arc((s * 0.02, s * 0.16, s * 0.42, s * 0.64), 90, 280, fill=fill, width=lw)
    d.arc((s * 0.58, s * 0.16, s * 0.98, s * 0.64), 260, 90, fill=fill, width=lw)
    d.ellipse((s * 0.20, s * 0.12, s * 0.80, s * 0.36), fill=hi, outline=edge, width=max(2, s // 28))
    d.polygon(
        [(s * 0.26, s * 0.26), (s * 0.74, s * 0.26), (s * 0.64, s * 0.58), (s * 0.36, s * 0.58)],
        fill=fill,
    )
    d.polygon(
        [(s * 0.36, s * 0.32), (s * 0.46, s * 0.32), (s * 0.42, s * 0.52), (s * 0.34, s * 0.52)],
        fill=hi,
    )
    d.rectangle((s * 0.44, s * 0.56, s * 0.56, s * 0.72), fill=dark)
    d.rounded_rectangle((s * 0.30, s * 0.70, s * 0.70, s * 0.80), radius=max(3, s // 16), fill=fill, outline=edge, width=2)
    d.rounded_rectangle((s * 0.18, s * 0.78, s * 0.82, s * 0.91), radius=max(3, s // 18), fill=dark, outline=edge, width=2)
    return im


def load_mark(target):
    mark = Image.open(MARK).convert("RGBA")
    side = mark.size[0]
    mask = Image.new("L", (side, side), 0)
    ImageDraw.Draw(mask).ellipse((2, 2, side - 3, side - 3), fill=255)
    mark.putalpha(ImageChops.multiply(mark.split()[-1], mask))
    return mark.resize((target, target), Image.Resampling.LANCZOS)


def ghost_body_height(mark):
    white = mark.split()[0].point(lambda p: 255 if p > 230 else 0)
    box = white.getbbox()
    return 0 if box is None else box[3] - box[1]


def lh(fnt):
    ascent, descent = fnt.getmetrics()
    return ascent + descent


def tracked(draw, text, fnt, y, fill, gap):
    width = sum(draw.textlength(ch, font=fnt) + gap for ch in text) - gap
    x = (W - width) / 2
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + gap


def rounded(base, box, radius, fill, outline=None, width=2):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    blit(base, layer)


def pill(draw, x, y, text, fnt, bg, fg):
    tw = draw.textlength(text, font=fnt)
    h = lh(fnt)
    box = (x, y, x + tw + 26, y + h + 8)
    draw.rounded_rectangle(box, radius=(h + 8) / 2, fill=bg)
    draw.text((x + 13, y + 3), text, font=fnt, fill=fg)
    return box


def draw_header(base):
    draw = ImageDraw.Draw(base)
    kicker = font(F_BOLD, 22)
    title_f = font(F_DISP, 66)
    sub_f = font(F_BOLD, 36)
    tracked(draw, "TROPHY UNLOCKED", kicker, 14, (255, 214, 120), 4)
    title = "GTA 6, NIGHT ONE"
    sub = "MY TROPHY LIST SO FAR"
    tw = draw.textlength(title, font=title_f)
    sw = draw.textlength(sub, font=sub_f)
    if tw > 1080 or sw > 1080:
        raise SystemExit("header overflow")
    draw.text(((W - tw) / 2, 46), title, font=title_f, fill=(255, 255, 255),
              stroke_width=3, stroke_fill=(28, 8, 32))
    draw.text(((W - sw) / 2, 128), sub, font=sub_f, fill=(255, 246, 232),
              stroke_width=2, stroke_fill=(32, 10, 28))


def draw_card(base, box, spec, fonts):
    x0, y0, x1, y1 = box
    ghost = spec.get("ghost")
    metal = METAL[spec["grade"]]
    if ghost:
        rounded(base, (x0 + 6, y0 + 10, x1 + 6, y1 + 12), 30, (0, 0, 0, 80))
        rounded(base, (x0 - 14, y0 - 12, x1 + 14, y1 + 14), 36, (255, 176, 48, 55))
        rounded(base, box, 30, (32, 20, 12, 242), (255, 206, 96, 255), 5)
    else:
        rounded(base, (x0 + 5, y0 + 8, x1 + 5, y1 + 10), 26, (0, 0, 0, 70))
        rounded(base, box, 26, (12, 10, 20, 232), (255, 255, 255, 55), 2)

    draw = ImageDraw.Draw(base)
    icon_s = 268 if ghost else 100
    ix = x0 + 16
    iy = y0 + (y1 - y0 - icon_s) / 2
    if ghost:
        mark = load_mark(icon_s)
        body = ghost_body_height(mark)
        if body < 110:
            raise SystemExit(f"ghost body {body}px is under 110")
        print(f"ghost body {body}px inside {icon_s}px mark")
        draw.ellipse((ix - 8, iy - 8, ix + icon_s + 8, iy + icon_s + 8), outline=metal["pill"], width=5)
        base.alpha_composite(mark, (int(ix), int(iy)))
    else:
        draw.ellipse((ix, iy, ix + icon_s, iy + icon_s), fill=(10, 10, 16, 255), outline=metal["fill"], width=4)
        cup = trophy_icon(icon_s - 16, metal)
        base.alpha_composite(cup, (int(ix + 8), int(iy + 8)))

    name_f, desc_f, meta_f, grade_f, brand_f = fonts
    text_x = ix + icon_s + 20
    text_r = x1 - 22
    lines = [(spec["name"], name_f, (255, 255, 255))]
    if ghost:
        lines.append(("make.fun", brand_f, (255, 78, 166)))
    lines.append((spec["desc"], desc_f, (255, 255, 255)))
    lines.append((f"RARITY   {spec['rarity']}", meta_f, (236, 226, 214)))
    gap = 5
    block = sum(lh(fnt) for _, fnt, _ in lines) + gap * (len(lines) - 1)
    if block > (y1 - y0 - 16):
        raise SystemExit(f"card too short for {spec['name']}: {block} > {y1 - y0 - 16}")
    grade_w = draw.textlength(spec["grade"], font=grade_f) + 26
    name_w = draw.textlength(spec["name"], font=name_f)
    if text_x + name_w + 16 + grade_w > text_r:
        raise SystemExit(f"name overflow: {spec['name']}")
    for text, fnt, _ in lines[1:]:
        if not text.startswith("RARITY") and text_x + draw.textlength(text, font=fnt) > text_r:
            raise SystemExit(f"line overflow: {text}")
    ty = y0 + (y1 - y0 - block) / 2
    for text, fnt, col in lines:
        draw.text((text_x, ty), text, font=fnt, fill=col)
        if text == spec["name"]:
            pill(draw, text_r - grade_w, ty + 2, spec["grade"], grade_f, metal["pill"], metal["ink"])
        if text.startswith("RARITY") and spec.get("chip"):
            chip_f = grade_f
            cw = draw.textlength(spec["chip"], font=chip_f) + 26
            chip = pill(draw, text_r - cw, ty - 1, spec["chip"], chip_f, (176, 246, 196), (8, 52, 30))
            if text_x + draw.textlength(text, font=fnt) + 12 > chip[0]:
                raise SystemExit("chip overlaps rarity")
        ty += lh(fnt) + gap


def main():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw_sky(img)
    draw_sun(img)
    regular = (
        font(F_DISP, 40),
        font(F_SEMI, 30),
        font(F_MED, 22),
        font(F_BOLD, 16),
        font(F_BOLD, 30),
    )
    punch = (
        font(F_DISP, 44),
        font(F_SEMI, 30),
        font(F_MED, 22),
        font(F_BOLD, 18),
        font(F_BOLD, 40),
    )
    palms = palm_layer()
    # Fronds frame the stack. They do not run under the type.
    hole = Image.new("L", (W, H), 255)
    ImageDraw.Draw(hole).rounded_rectangle((28, 172, W - 28, 1116), radius=32, fill=0)
    red, green, blue, alpha = palms.split()
    palms.putalpha(ImageChops.multiply(alpha, hole))
    blit(img, palms)
    draw_header(img)
    y = 186
    for spec in CARDS:
        ghost = spec.get("ghost")
        height = 318 if ghost else 146
        inset = 28 if ghost else 50
        draw_card(img, (inset, y, W - inset, y + height), spec, punch if ghost else regular)
        y += height + 7
    if y > H - 24:
        raise SystemExit(f"stack runs off the canvas at {y}")
    flat = Image.new("RGB", (W, H), (0, 0, 0))
    flat.paste(img, mask=img.split()[-1])
    flat.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT} {size} bytes end={y - 8}")
    if size >= 900 * 1024:
        raise SystemExit("png is 900KB or larger")


if __name__ == "__main__":
    main()
