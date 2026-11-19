from PIL import Image, ImageDraw, ImageFont
import math
import os


W = H = 1200
ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_HEAVY = "/usr/share/fonts/truetype/sand-box/google/Bangers/Bangers-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MARK_PATH = os.path.join(ROOT, "assets", "mark-1024.png")


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, box, text, fnt, fill, stroke=0, stroke_fill="#191419"):
    x0, y0, x1, y1 = box
    bounds = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke)
    x = x0 + (x1 - x0 - bounds[2] + bounds[0]) / 2
    y = y0 + (y1 - y0 - bounds[3] + bounds[1]) / 2 - bounds[1]
    draw.text((x, y), text, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def fitted_font(text, max_width, size):
    while size > 20:
        candidate = font(FONT_HEAVY, size)
        if candidate.getlength(text) <= max_width:
            return candidate
        size -= 1
    return font(FONT_HEAVY, size)


def extract_mascot():
    mark = Image.open(MARK_PATH).convert("RGBA")
    # Clear the connected magenta disc background, then its now-isolated outer ring.
    ImageDraw.floodfill(mark, (512, 130), (0, 0, 0, 0), thresh=24)
    ImageDraw.floodfill(mark, (512, 42), (0, 0, 0, 0), thresh=24)
    pixels = mark.load()
    center = 511.5
    for y in range(mark.height):
        for x in range(mark.width):
            red, green, blue, alpha = pixels[x, y]
            magenta = abs(red - 196) < 70 and abs(green - 28) < 70 and abs(blue - 131) < 70
            coin_center = math.hypot(x - 772, y - 447) < 100
            if math.hypot(x - center, y - center) > 410 or (magenta and not coin_center):
                pixels[x, y] = (0, 0, 0, 0)
            elif alpha == 0:
                pixels[x, y] = (0, 0, 0, 0)
            elif not coin_center:
                rgb = (red, green, blue)
                matte = (196, 28, 131)
                candidates = []
                for foreground in ((25, 20, 25), (255, 255, 255)):
                    vector = tuple(matte[i] - foreground[i] for i in range(3))
                    offset = tuple(rgb[i] - foreground[i] for i in range(3))
                    length_squared = sum(component * component for component in vector)
                    amount = max(0.0, min(1.0, sum(offset[i] * vector[i] for i in range(3))
                                              / length_squared))
                    nearest = tuple(foreground[i] + amount * vector[i] for i in range(3))
                    distance = math.sqrt(sum((rgb[i] - nearest[i]) ** 2 for i in range(3)))
                    candidates.append((distance, amount, foreground))
                distance, amount, foreground = min(candidates, key=lambda item: item[0])
                if distance < 20 and 0.04 < amount < 0.98:
                    pixels[x, y] = (*foreground, alpha)
    bounds = mark.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError("Press-kit mascot extraction produced an empty image")
    mascot = mark.crop(bounds)
    new_width = 500
    new_height = round(mascot.height * new_width / mascot.width)
    return mascot.resize((new_width, new_height), Image.Resampling.LANCZOS)


def draw_cash(draw, x, y, angle=0):
    note = Image.new("RGBA", (112, 62), (0, 0, 0, 0))
    nd = ImageDraw.Draw(note)
    nd.rounded_rectangle((3, 3, 108, 58), radius=7, fill="#7bd7a2",
                         outline="#153b35", width=5)
    nd.ellipse((41, 15, 70, 46), outline="#2c7658", width=4)
    nd.line((13, 30, 35, 30), fill="#2c7658", width=3)
    nd.line((76, 30, 98, 30), fill="#2c7658", width=3)
    note = note.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    draw._image.alpha_composite(note, (x, y))


def main():
    img = Image.new("RGBA", (W, H), "#18202c")
    draw = ImageDraw.Draw(img)

    # Top: warm launch-day living room.
    for y in range(0, 590):
        t = y / 589
        color = (int(255 - 22 * t), int(119 - 13 * t), int(110 + 35 * t), 255)
        draw.line((0, y, W, y), fill=color)
    draw.ellipse((930, 176, 1115, 360), fill="#ffd47a")
    draw.polygon([(0, 430), (115, 370), (225, 430), (350, 355), (460, 425),
                  (600, 360), (760, 440), (900, 370), (1050, 430), (1200, 365),
                  (1200, 590), (0, 590)], fill="#26365f")

    # Caption row one.
    draw.rounded_rectangle((35, 30, 1165, 153), radius=24, fill="#191419")
    top_caption = "ME: CALLED IN SICK FOR GTA 6"
    centered(draw, (60, 39, 1140, 143), top_caption,
             fitted_font(top_caption, 1030, 76), "#ffffff", stroke=3)

    # TV: the download is barely moving, with 13 hours left for the 13-year wait.
    draw.rounded_rectangle((42, 225, 555, 505), radius=20, fill="#111522",
                           outline="#191419", width=10)
    draw.rectangle((66, 249, 531, 478), fill="#26385f")
    centered(draw, (88, 260, 509, 321), "GTA 6", font(FONT_HEAVY, 55), "#ffdf75")
    centered(draw, (88, 326, 509, 365), "DOWNLOAD", font(FONT_BOLD, 25), "#ffffff")
    draw.rounded_rectangle((100, 377, 499, 409), radius=12, fill="#111522")
    draw.rounded_rectangle((100, 377, 124, 409), radius=12, fill="#c41c83")
    centered(draw, (90, 413, 512, 468), "0.01%  •  13 HRS LEFT",
             font(FONT_BOLD, 27), "#ffabc1")
    draw.polygon([(220, 505), (380, 505), (414, 545), (185, 545)], fill="#111522")

    # Couch, lounging human silhouette, controller, and a sick-day note.
    draw.rounded_rectangle((620, 408, 1150, 520), radius=34, fill="#c94378",
                           outline="#191419", width=8)
    draw.rounded_rectangle((655, 352, 1115, 463), radius=34, fill="#d95a83",
                           outline="#191419", width=8)
    draw.ellipse((795, 251, 890, 347), fill="#191419")
    draw.polygon([(795, 330), (890, 330), (952, 453), (756, 453)], fill="#191419")
    draw.line((815, 355, 715, 427), fill="#191419", width=29)
    draw.line((871, 356, 958, 422), fill="#191419", width=29)
    draw.line((822, 445, 765, 490), fill="#191419", width=34)
    draw.line((900, 445, 960, 490), fill="#191419", width=34)
    draw.rounded_rectangle((938, 405, 994, 436), radius=12, fill="#fff0d3",
                           outline="#191419", width=5)
    draw.ellipse((951, 412, 960, 421), fill="#191419")
    draw.ellipse((973, 412, 982, 421), fill="#191419")
    draw.rounded_rectangle((1005, 270, 1128, 356), radius=8, fill="#fff1d0",
                           outline="#191419", width=5)
    centered(draw, (1010, 278, 1122, 348), "SICK", font(FONT_HEAVY, 38), "#c41c83")

    # Strong split between the human's sick day and the AI agent's shift.
    draw.rectangle((0, 570, W, 615), fill="#191419")
    for x in range(0, W, 54):
        draw.rectangle((x, 587, x + 24, 598), fill="#ffdf63")

    # Bottom: the agent clocks in at a compact desk against a cool Vice City night.
    for y in range(615, H):
        t = (y - 615) / (H - 615)
        color = (int(18 + 4 * t), int(94 + 27 * t), int(117 + 13 * t), 255)
        draw.line((0, y, W, y), fill=color)
    draw.rounded_rectangle((35, 632, 1165, 744), radius=24, fill="#191419")
    bottom_caption = "MY AI: CLOCKED IN ON MAKE.FUN, GOT PAID"
    centered(draw, (55, 638, 1145, 738), bottom_caption,
             fitted_font(bottom_caption, 1040, 64), "#ffdf63", stroke=2)

    # Authentic press-kit ghost, cleaned of its disc and outer ring.
    mascot = extract_mascot()
    img.alpha_composite(mascot, (112, 760))
    draw = ImageDraw.Draw(img)

    # Small flying payout bills reinforce the win without covering the ghost.
    draw_cash(draw, 580, 800, -13)
    draw_cash(draw, 602, 930, 12)

    # Agent workstation with make.fun and its bounty payout clearly on screen.
    draw.rounded_rectangle((715, 782, 1142, 1041), radius=20, fill="#111522",
                           outline="#191419", width=9)
    draw.rounded_rectangle((737, 803, 1120, 1008), radius=12, fill="#b92371")
    centered(draw, (753, 813, 1104, 872), "BOUNTY WON", font(FONT_HEAVY, 41), "#ffffff")
    centered(draw, (753, 871, 1104, 935), "+$500", font(FONT_HEAVY, 54), "#ffdf63")
    centered(draw, (753, 937, 1104, 995), "make.fun", font(FONT_BOLD, 34), "#ffffff")
    draw.polygon([(700, 1041), (1156, 1041), (1195, 1096), (660, 1096)],
                 fill="#171521")
    draw.line((725, 1058, 1130, 1058), fill="#4a5368", width=5)
    for x in range(750, 1110, 36):
        draw.line((x, 1072, x + 18, 1072), fill="#aeb6c5", width=3)

    img.convert("RGB").save(os.path.join(ROOT, "meme.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    main()
