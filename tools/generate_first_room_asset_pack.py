from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "web-emulator" / "assets"

PAL = {
    "transparent": (0, 0, 0, 0),
    "ink": "#100814",
    "black_soft": "#1a0d20",
    "night": "#12142f",
    "bluewood": "#1b2446",
    "bluewood_hi": "#28345f",
    "deep_purple": "#241235",
    "purple": "#3b2058",
    "lavender": "#6a4a8a",
    "lavender_hi": "#9a72bf",
    "dusty_pink": "#d98ab6",
    "pink_hi": "#f1b5cf",
    "old_gold": "#c99b54",
    "gold_hi": "#f0cf79",
    "candle": "#ffd782",
    "skin": "#f3c1ad",
    "skin_shadow": "#d98a93",
    "hair": "#2a1423",
    "hair_hi": "#6b3049",
    "cream": "#f8e7c4",
    "shadow": "#0a0712",
    "rain": "#8a6ac2",
    "paper": "#ead6bd",
    "box": "#7a4a52",
    "box_hi": "#ad6b64",
    "wood0": "#4b263a",
    "wood1": "#8f5062",
    "green": "#708e63",
}


def c(value, alpha=255):
    if isinstance(value, tuple):
        return value
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def save(img, folder, name):
    target = OUT / folder / name
    target.parent.mkdir(parents=True, exist_ok=True)
    img.save(target)


def rect(d, xy, fill, outline=None, width=1):
    d.rectangle(xy, fill=c(fill), outline=c(outline) if outline else None, width=width)


def ellipse(d, xy, fill, outline=None, width=1):
    d.ellipse(xy, fill=c(fill), outline=c(outline) if outline else None, width=width)


def poly(d, pts, fill, outline=None):
    d.polygon(pts, fill=c(fill), outline=c(outline) if outline else None)


def line(d, pts, fill, width=1):
    d.line(pts, fill=c(fill), width=width)


def star(d, x, y, fill="old_gold", size=4):
    color = PAL[fill] if fill in PAL else fill
    rect(d, (x - 1, y - size, x + 1, y + size), color)
    rect(d, (x - size, y - 1, x + size, y + 1), color)
    rect(d, (x, y, x, y), PAL["cream"])


def character(direction="down", frame=0, pose="idle"):
    img = Image.new("RGBA", (96, 128), PAL["transparent"])
    d = ImageDraw.Draw(img)
    bob = -2 if pose == "interact" else 0
    blink = pose == "surprise"
    holding = pose == "package"
    step = -1 if frame == 1 else 1

    ellipse(d, (25, 112, 72, 121), PAL["shadow"])
    if direction == "up":
        draw_character_back(d, bob, frame)
    elif direction == "side":
        draw_character_side(d, bob, frame, holding)
    else:
        draw_character_front(d, bob, frame, blink, holding, pose)
    return img


def draw_body_front(d, bob):
    rect(d, (34, 56 + bob, 62, 85 + bob), PAL["dusty_pink"], PAL["ink"], 3)
    rect(d, (38, 62 + bob, 58, 68 + bob), PAL["lavender_hi"])
    poly(d, [(30, 82 + bob), (67, 82 + bob), (76, 101 + bob), (23, 101 + bob)], PAL["deep_purple"], PAL["ink"])
    rect(d, (31, 87 + bob, 68, 92 + bob), PAL["dusty_pink"])
    rect(d, (39, 101, 46, 110), PAL["lavender"], PAL["ink"])
    rect(d, (55, 101, 62, 110), PAL["lavender"], PAL["ink"])
    rect(d, (34, 110, 48, 118), PAL["black_soft"], PAL["ink"])
    rect(d, (53, 110, 68, 118), PAL["black_soft"], PAL["ink"])


def draw_hair_front(d, bob):
    ellipse(d, (21, 10 + bob, 75, 75 + bob), PAL["hair"], PAL["ink"], 3)
    ellipse(d, (13, 38 + bob, 35, 95 + bob), PAL["hair"], PAL["ink"], 3)
    ellipse(d, (62, 37 + bob, 84, 94 + bob), PAL["hair"], PAL["ink"], 3)
    line(d, [(19, 50 + bob), (16, 72 + bob), (25, 92 + bob)], PAL["hair_hi"], 3)
    line(d, [(74, 47 + bob), (81, 70 + bob), (72, 92 + bob)], PAL["hair_hi"], 3)
    poly(d, [(19, 22 + bob), (35, 11 + bob), (47, 26 + bob), (62, 14 + bob), (78, 27 + bob), (71, 42 + bob), (23, 42 + bob)], PAL["hair"], PAL["ink"])
    ellipse(d, (15, 35 + bob, 29, 49 + bob), "#c87642", PAL["ink"], 2)
    rect(d, (21, 31 + bob, 24, 36 + bob), PAL["green"])


def draw_face_front(d, bob, surprise=False):
    ellipse(d, (31, 24 + bob, 65, 61 + bob), PAL["skin"], PAL["ink"], 3)
    rect(d, (38, 41 + bob, 44, 50 + bob), PAL["ink"])
    rect(d, (55, 41 + bob, 61, 50 + bob), PAL["ink"])
    rect(d, (40, 42 + bob, 41, 44 + bob), PAL["cream"])
    rect(d, (57, 42 + bob, 58, 44 + bob), PAL["cream"])
    rect(d, (34, 52 + bob, 40, 55 + bob), PAL["skin_shadow"])
    rect(d, (59, 52 + bob, 65, 55 + bob), PAL["skin_shadow"])
    if surprise:
        rect(d, (48, 55 + bob, 52, 60 + bob), PAL["ink"])
    else:
        line(d, [(46, 56 + bob), (50, 59 + bob), (55, 56 + bob)], PAL["ink"], 2)


def draw_character_front(d, bob, frame, surprise, holding, pose):
    draw_hair_front(d, bob)
    draw_body_front(d, bob)
    if pose == "interact":
        line(d, [(35, 65 + bob), (22, 76 + bob)], PAL["skin"], 6)
        line(d, [(62, 65 + bob), (78, 56 + bob)], PAL["skin"], 6)
        star(d, 81, 52 + bob, "gold_hi", 4)
    else:
        line(d, [(35, 65 + bob), (24, 82 + bob + frame * 2)], PAL["skin"], 6)
        line(d, [(62, 65 + bob), (74, 82 + bob - frame * 2)], PAL["skin"], 6)
    draw_face_front(d, bob, surprise)
    if holding:
        rect(d, (54, 70 + bob, 84, 94 + bob), PAL["box"], PAL["ink"], 3)
        rect(d, (66, 70 + bob, 72, 94 + bob), PAL["old_gold"])
        star(d, 80, 68 + bob, "gold_hi", 3)


def draw_character_back(d, bob, frame):
    ellipse(d, (20, 13 + bob, 76, 86 + bob), PAL["hair"], PAL["ink"], 3)
    line(d, [(28, 42 + bob), (21, 82 + bob)], PAL["hair_hi"], 3)
    line(d, [(68, 43 + bob), (76, 84 + bob)], PAL["hair_hi"], 3)
    rect(d, (34, 59 + bob, 63, 88 + bob), PAL["dusty_pink"], PAL["ink"], 3)
    poly(d, [(30, 84 + bob), (68, 84 + bob), (75, 102 + bob), (23, 102 + bob)], PAL["deep_purple"], PAL["ink"])
    rect(d, (35, 110, 48, 118), PAL["black_soft"], PAL["ink"])
    rect(d, (53, 110, 67, 118), PAL["black_soft"], PAL["ink"])
    line(d, [(34, 68 + bob), (23, 83 + bob + frame * 2)], PAL["skin"], 6)
    line(d, [(63, 68 + bob), (75, 83 + bob - frame * 2)], PAL["skin"], 6)


def draw_character_side(d, bob, frame, holding):
    ellipse(d, (22, 14 + bob, 76, 82 + bob), PAL["hair"], PAL["ink"], 3)
    ellipse(d, (55, 37 + bob, 86, 94 + bob), PAL["hair"], PAL["ink"], 3)
    ellipse(d, (35, 24 + bob, 68, 60 + bob), PAL["skin"], PAL["ink"], 3)
    poly(d, [(28, 24 + bob), (48, 10 + bob), (71, 28 + bob), (67, 40 + bob), (33, 39 + bob)], PAL["hair"], PAL["ink"])
    rect(d, (56, 41 + bob, 62, 50 + bob), PAL["ink"])
    line(d, [(59, 56 + bob), (64, 58 + bob)], PAL["ink"], 2)
    rect(d, (36, 58 + bob, 65, 88 + bob), PAL["dusty_pink"], PAL["ink"], 3)
    poly(d, [(34, 84 + bob), (67, 84 + bob), (76, 102 + bob), (28, 102 + bob)], PAL["deep_purple"], PAL["ink"])
    rect(d, (37 + frame * 2, 110, 51 + frame * 2, 118), PAL["black_soft"], PAL["ink"])
    rect(d, (57 - frame * 2, 110, 72 - frame * 2, 118), PAL["black_soft"], PAL["ink"])
    line(d, [(39, 68 + bob), (28, 84 + bob + frame * 2)], PAL["skin"], 6)
    line(d, [(63, 68 + bob), (78, 82 + bob - frame * 2)], PAL["skin"], 6)
    if holding:
        rect(d, (63, 72 + bob, 92, 96 + bob), PAL["box"], PAL["ink"], 3)
        rect(d, (75, 72 + bob, 81, 96 + bob), PAL["old_gold"])
        star(d, 88, 70 + bob, "gold_hi", 3)


def portrait(expression="neutral"):
    img = Image.new("RGBA", (128, 128), PAL["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (20, 10, 108, 118), PAL["hair"], PAL["ink"], 4)
    ellipse(d, (34, 26, 92, 88), PAL["skin"], PAL["ink"], 4)
    poly(d, [(24, 30), (49, 10), (65, 35), (91, 18), (104, 38), (94, 52), (30, 52)], PAL["hair"], PAL["ink"])
    rect(d, (45, 56, 55, 72), PAL["ink"])
    rect(d, (74, 56, 84, 72), PAL["ink"])
    rect(d, (48, 58, 51, 61), PAL["cream"])
    rect(d, (77, 58, 80, 61), PAL["cream"])
    rect(d, (31, 76, 43, 82), PAL["skin_shadow"])
    rect(d, (86, 76, 98, 82), PAL["skin_shadow"])
    if expression == "surprise":
        rect(d, (62, 82, 68, 91), PAL["ink"])
        draw_exclaim(d, 101, 25)
    else:
        line(d, [(57, 84), (65, 90), (74, 84)], PAL["ink"], 3)
    ellipse(d, (18, 42, 38, 62), "#c87642", PAL["ink"], 2)
    rect(d, (27, 36, 31, 43), PAL["green"])
    return img


def draw_exclaim(d, x, y):
    rect(d, (x, y, x + 4, y + 18), PAL["gold_hi"], PAL["ink"])
    rect(d, (x, y + 24, x + 4, y + 28), PAL["gold_hi"], PAL["ink"])


def object_package():
    img = Image.new("RGBA", (128, 96), PAL["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (18, 69, 110, 86), PAL["shadow"])
    rect(d, (22, 30, 106, 78), PAL["box"], PAL["ink"], 4)
    rect(d, (55, 30, 72, 78), PAL["old_gold"], PAL["ink"], 2)
    rect(d, (22, 46, 106, 58), PAL["box_hi"], PAL["ink"], 2)
    rect(d, (75, 36, 98, 52), PAL["paper"], PAL["ink"], 2)
    line(d, [(79, 42), (94, 42)], PAL["lavender"], 2)
    line(d, [(79, 48), (89, 48)], PAL["lavender"], 2)
    for x, y in [(18, 24), (110, 22), (92, 16), (52, 20)]:
        star(d, x, y, "gold_hi", 5)
    return img


def object_window():
    img = Image.new("RGBA", (160, 180), PAL["transparent"])
    d = ImageDraw.Draw(img)
    rect(d, (18, 12, 142, 164), PAL["black_soft"], PAL["dusty_pink"], 5)
    rect(d, (32, 28, 128, 150), PAL["night"], PAL["ink"], 3)
    rect(d, (76, 28, 84, 150), PAL["dusty_pink"])
    rect(d, (32, 88, 128, 96), PAL["dusty_pink"])
    for x in [46, 70, 104, 124]:
        line(d, [(x, 32), (x - 18, 145)], PAL["rain"], 3)
    ellipse(d, (102, 38, 126, 62), PAL["old_gold"])
    rect(d, (8, 76, 31, 170), PAL["deep_purple"], PAL["ink"])
    rect(d, (130, 76, 152, 170), PAL["deep_purple"], PAL["ink"])
    return img


def object_door():
    img = Image.new("RGBA", (96, 172), PAL["transparent"])
    d = ImageDraw.Draw(img)
    rect(d, (18, 10, 78, 164), PAL["black_soft"], PAL["dusty_pink"], 5)
    rect(d, (30, 30, 66, 86), PAL["deep_purple"], PAL["ink"], 3)
    rect(d, (30, 98, 66, 148), PAL["deep_purple"], PAL["ink"], 3)
    rect(d, (64, 86, 70, 92), PAL["old_gold"], PAL["ink"])
    return img


def object_bed():
    img = Image.new("RGBA", (280, 142), PAL["transparent"])
    d = ImageDraw.Draw(img)
    rect(d, (20, 26, 238, 100), PAL["black_soft"], PAL["ink"], 5)
    rect(d, (6, 58, 270, 126), PAL["lavender"], PAL["dusty_pink"], 5)
    rect(d, (20, 70, 252, 108), PAL["deep_purple"], PAL["ink"], 3)
    rect(d, (196, 68, 264, 124), PAL["pink_hi"], PAL["ink"], 3)
    rect(d, (20, 116, 252, 126), PAL["dusty_pink"])
    return img


def object_table():
    img = Image.new("RGBA", (132, 92), PAL["transparent"])
    d = ImageDraw.Draw(img)
    rect(d, (12, 20, 120, 55), PAL["wood0"], PAL["ink"], 4)
    rect(d, (22, 10, 110, 26), PAL["wood1"], PAL["ink"], 3)
    rect(d, (26, 52, 36, 82), PAL["wood0"], PAL["ink"])
    rect(d, (96, 52, 106, 82), PAL["wood0"], PAL["ink"])
    rect(d, (68, 18, 76, 55), PAL["old_gold"])
    star(d, 104, 8, "gold_hi", 4)
    return img


def object_rug():
    img = Image.new("RGBA", (420, 156), PAL["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (10, 20, 410, 136), PAL["deep_purple"], PAL["ink"], 4)
    ellipse(d, (42, 44, 378, 116), "#372149", PAL["dusty_pink"], 3)
    rect(d, (92, 67, 328, 91), PAL["lavender"], PAL["ink"], 2)
    for x in range(66, 360, 42):
        rect(d, (x, 55, x + 16, 64), PAL["old_gold"])
        rect(d, (x, 98, x + 16, 107), PAL["old_gold"])
    return img


def object_boxes():
    img = Image.new("RGBA", (156, 120), PAL["transparent"])
    d = ImageDraw.Draw(img)
    rect(d, (16, 50, 70, 98), PAL["box"], PAL["ink"], 4)
    rect(d, (70, 32, 126, 82), PAL["box"], PAL["ink"], 4)
    rect(d, (82, 32, 92, 82), PAL["old_gold"])
    rect(d, (16, 64, 70, 74), PAL["box_hi"])
    rect(d, (28, 50, 38, 98), PAL["old_gold"])
    rect(d, (90, 54, 112, 68), PAL["paper"], PAL["ink"], 2)
    return img


def ui_box(kind):
    if kind == "dialog":
        img = Image.new("RGBA", (928, 150), PAL["transparent"])
        d = ImageDraw.Draw(img)
        rect(d, (0, 0, 927, 149), "#140b1c", PAL["purple"], 5)
        rect(d, (10, 10, 917, 139), "#1d1028", PAL["dusty_pink"], 2)
        rect(d, (884, 118, 894, 128), PAL["old_gold"])
        return img
    if kind == "slot":
        img = Image.new("RGBA", (64, 64), PAL["transparent"])
        d = ImageDraw.Draw(img)
        rect(d, (4, 4, 60, 60), "#140b1c", PAL["purple"], 3)
        rect(d, (10, 10, 54, 54), "#20132c", PAL["lavender"], 2)
        return img
    if kind == "selector":
        img = Image.new("RGBA", (72, 72), PAL["transparent"])
        d = ImageDraw.Draw(img)
        rect(d, (2, 2, 69, 69), PAL["transparent"], PAL["old_gold"], 4)
        for pos in [(8, 8), (63, 8), (8, 63), (63, 63)]:
            star(d, *pos, "gold_hi", 4)
        return img


def icon(kind):
    img = Image.new("RGBA", (64, 64), PAL["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (6, 6, 58, 58), "#1d1028", PAL["purple"], 3)
    if kind == "package":
        small = object_package().resize((52, 39), Image.Resampling.NEAREST)
        img.alpha_composite(small, (6, 14))
    elif kind == "key":
        ellipse(d, (14, 25, 30, 41), PAL["old_gold"], PAL["ink"], 3)
        rect(d, (28, 31, 52, 35), PAL["old_gold"], PAL["ink"])
        rect(d, (46, 35, 51, 44), PAL["old_gold"], PAL["ink"])
    elif kind == "invitation":
        rect(d, (14, 18, 50, 46), PAL["paper"], PAL["ink"], 3)
        line(d, [(16, 20), (32, 33), (48, 20)], PAL["dusty_pink"], 2)
        star(d, 46, 17, "gold_hi", 3)
    elif kind == "cursor":
        poly(d, [(13, 10), (52, 32), (13, 54), (24, 32)], PAL["old_gold"], PAL["ink"])
    else:
        star(d, 32, 32, "gold_hi", 12)
    return img


def tile_sheet():
    img = Image.new("RGBA", (256, 128), PAL["transparent"])
    d = ImageDraw.Draw(img)
    # 32x32 tiles: floor variants
    for i in range(4):
        x = i * 32
        rect(d, (x, 0, x + 31, 31), PAL["bluewood"], PAL["ink"])
        line(d, [(x, 8), (x + 31, 5 + i * 3)], PAL["bluewood_hi"], 2)
        line(d, [(x, 24), (x + 31, 22 - i)], "#111936", 2)
    # wallpaper variants
    for i in range(4):
        x = i * 32
        rect(d, (x, 32, x + 31, 63), PAL["deep_purple"], PAL["ink"])
        line(d, [(x + 8, 32), (x + 8, 63)], PAL["purple"], 2)
        line(d, [(x + 24, 32), (x + 24, 63)], PAL["purple"], 2)
        star(d, x + 16, 47, "lavender_hi", 2)
    # baseboards / corners / shadows
    rect(d, (0, 64, 127, 79), PAL["black_soft"], PAL["dusty_pink"], 2)
    rect(d, (0, 80, 127, 95), PAL["purple"], PAL["ink"], 2)
    rect(d, (128, 64, 159, 95), PAL["deep_purple"], PAL["dusty_pink"], 2)
    rect(d, (160, 64, 191, 95), PAL["shadow"])
    rect(d, (192, 64, 255, 95), PAL["transparent"])
    return img


def room_initial():
    img = Image.new("RGBA", (1024, 576), PAL["transparent"])
    d = ImageDraw.Draw(img)
    # Wallpaper
    rect(d, (0, 0, 1024, 310), PAL["deep_purple"])
    for x in range(0, 1024, 48):
        rect(d, (x, 0, x + 24, 310), "#211230")
        line(d, [(x + 24, 0), (x + 24, 310)], PAL["purple"], 3)
        for y in range(42, 288, 64):
            star(d, x + 13, y, "lavender_hi", 2)
    # corners and shadow
    rect(d, (0, 0, 32, 576), "#160d22")
    rect(d, (992, 0, 1024, 576), "#160d22")
    rect(d, (0, 0, 1024, 32), "#100814")
    rect(d, (0, 288, 1024, 330), PAL["black_soft"])
    rect(d, (0, 300, 1024, 314), PAL["dusty_pink"])
    # Floor
    rect(d, (0, 314, 1024, 576), "#1d1830")
    for x in range(-80, 1120, 72):
        poly(d, [(x, 576), (x + 64, 576), (x + 112, 314), (x + 47, 314)], PAL["bluewood"], PAL["ink"])
        line(d, [(x + 28, 576), (x + 77, 314)], PAL["bluewood_hi"], 2)
    # Soft shadows
    ellipse(d, (72, 418, 414, 494), "#2b2138")
    ellipse(d, (420, 438, 800, 516), "#2b2138")
    # Integrated objects
    img.alpha_composite(object_rug(), (285, 370))
    img.alpha_composite(object_bed(), (78, 220))
    img.alpha_composite(object_table(), (466, 352))
    img.alpha_composite(object_window(), (710, 80))
    img.alpha_composite(object_door(), (904, 170))
    img.alpha_composite(object_boxes(), (620, 364))
    return img


def pumpkin_pin(d, x, y, scale=1):
    ellipse(d, (x, y, x + 12 * scale, y + 11 * scale), "#d87932", PAL["ink"], 2)
    rect(d, (x + 5 * scale, y - 3 * scale, x + 7 * scale, y + 1 * scale), PAL["green"])
    rect(d, (x + 3 * scale, y + 4 * scale, x + 4 * scale, y + 5 * scale), PAL["ink"])
    rect(d, (x + 8 * scale, y + 4 * scale, x + 9 * scale, y + 5 * scale), PAL["ink"])
    line(d, [(x + 4 * scale, y + 8 * scale), (x + 7 * scale, y + 9 * scale), (x + 10 * scale, y + 8 * scale)], PAL["ink"], 1)


def character(direction="down", frame=0, pose="idle"):
    img = Image.new("RGBA", (96, 128), PAL["transparent"])
    d = ImageDraw.Draw(img)
    bob = -2 if pose in ("interact", "package") else 0
    step = -3 if frame == 1 else 3 if frame == 2 else 0
    ellipse(d, (18, 113, 80, 124), PAL["shadow"])

    if direction == "up":
        ellipse(d, (18, 12 + bob, 78, 91 + bob), PAL["hair"], PAL["ink"], 3)
        line(d, [(25, 40 + bob), (18, 88 + bob)], PAL["hair_hi"], 3)
        line(d, [(70, 40 + bob), (79, 88 + bob)], PAL["hair_hi"], 3)
        pumpkin_pin(d, 20, 27 + bob)
        rect(d, (33, 58 + bob, 64, 87 + bob), PAL["deep_purple"], PAL["ink"], 3)
        rect(d, (39, 61 + bob, 58, 69 + bob), PAL["dusty_pink"])
        poly(d, [(29, 84 + bob), (69, 84 + bob), (76, 102 + bob), (22, 102 + bob)], "#171021", PAL["ink"])
        rect(d, (34 + step, 103, 47 + step, 117), PAL["lavender"], PAL["ink"])
        rect(d, (53 - step, 103, 67 - step, 117), PAL["lavender"], PAL["ink"])
        return img

    side = direction == "side"
    if side:
        ellipse(d, (19, 13 + bob, 76, 86 + bob), PAL["hair"], PAL["ink"], 3)
        ellipse(d, (55, 42 + bob, 88, 101 + bob), PAL["hair"], PAL["ink"], 3)
        line(d, [(66, 42 + bob), (83, 93 + bob)], PAL["hair_hi"], 3)
        ellipse(d, (33, 25 + bob, 69, 61 + bob), PAL["skin"], PAL["ink"], 3)
        poly(d, [(24, 25 + bob), (47, 8 + bob), (72, 26 + bob), (68, 42 + bob), (34, 40 + bob)], PAL["hair"], PAL["ink"])
        pumpkin_pin(d, 23, 28 + bob)
        rect(d, (56, 41 + bob, 63, 51 + bob), PAL["ink"])
        rect(d, (58, 43 + bob, 60, 45 + bob), PAL["cream"])
        line(d, [(58, 56 + bob), (64, 58 + bob)], PAL["ink"], 2)
        rect(d, (35, 58 + bob, 65, 88 + bob), PAL["deep_purple"], PAL["ink"], 3)
        rect(d, (39, 62 + bob, 61, 69 + bob), PAL["dusty_pink"])
        poly(d, [(31, 84 + bob), (67, 84 + bob), (78, 102 + bob), (26, 102 + bob)], "#171021", PAL["ink"])
        line(d, [(37, 68 + bob), (24, 84 + bob + step)], PAL["skin"], 6)
        line(d, [(63, 68 + bob), (78, 81 + bob - step)], PAL["skin"], 6)
    else:
        ellipse(d, (19, 12 + bob, 77, 87 + bob), PAL["hair"], PAL["ink"], 3)
        ellipse(d, (10, 44 + bob, 35, 102 + bob), PAL["hair"], PAL["ink"], 3)
        ellipse(d, (61, 43 + bob, 88, 102 + bob), PAL["hair"], PAL["ink"], 3)
        line(d, [(21, 48 + bob), (15, 93 + bob)], PAL["hair_hi"], 3)
        line(d, [(72, 49 + bob), (82, 94 + bob)], PAL["hair_hi"], 3)
        ellipse(d, (30, 24 + bob, 66, 63 + bob), PAL["skin"], PAL["ink"], 3)
        poly(d, [(18, 27 + bob), (36, 11 + bob), (49, 26 + bob), (65, 13 + bob), (80, 29 + bob), (72, 45 + bob), (24, 43 + bob)], PAL["hair"], PAL["ink"])
        pumpkin_pin(d, 16, 35 + bob)
        rect(d, (37, 42 + bob, 45, 53 + bob), PAL["ink"])
        rect(d, (55, 42 + bob, 63, 53 + bob), PAL["ink"])
        rect(d, (40, 44 + bob, 42, 46 + bob), PAL["cream"])
        rect(d, (58, 44 + bob, 60, 46 + bob), PAL["cream"])
        rect(d, (33, 54 + bob, 40, 57 + bob), PAL["skin_shadow"])
        rect(d, (60, 54 + bob, 67, 57 + bob), PAL["skin_shadow"])
        if pose == "surprise":
            rect(d, (48, 56 + bob, 53, 63 + bob), PAL["ink"])
            draw_exclaim(d, 78, 21 + bob)
        else:
            line(d, [(44, 58 + bob), (50, 62 + bob), (57, 58 + bob)], PAL["ink"], 2)
        rect(d, (33, 58 + bob, 65, 88 + bob), PAL["deep_purple"], PAL["ink"], 3)
        rect(d, (37, 63 + bob, 61, 70 + bob), PAL["dusty_pink"])
        rect(d, (41, 70 + bob, 57, 81 + bob), "#171021")
        poly(d, [(28, 84 + bob), (70, 84 + bob), (78, 103 + bob), (20, 103 + bob)], "#171021", PAL["ink"])
        rect(d, (28, 88 + bob, 70, 93 + bob), PAL["dusty_pink"])
        if pose == "interact":
            line(d, [(34, 69 + bob), (19, 77 + bob)], PAL["skin"], 6)
            line(d, [(64, 69 + bob), (80, 55 + bob)], PAL["skin"], 6)
            star(d, 84, 50 + bob, "gold_hi", 4)
        else:
            line(d, [(34, 69 + bob), (22, 84 + bob + step)], PAL["skin"], 6)
            line(d, [(64, 69 + bob), (76, 84 + bob - step)], PAL["skin"], 6)

    rect(d, (34 + step, 103, 48 + step, 117), PAL["lavender"], PAL["ink"])
    rect(d, (52 - step, 103, 67 - step, 117), PAL["lavender"], PAL["ink"])
    rect(d, (31 + step, 115, 50 + step, 123), PAL["black_soft"], PAL["ink"])
    rect(d, (50 - step, 115, 71 - step, 123), PAL["black_soft"], PAL["ink"])
    if pose == "package":
        rect(d, (54, 71 + bob, 87, 97 + bob), PAL["box"], PAL["ink"], 3)
        rect(d, (68, 71 + bob, 75, 97 + bob), PAL["old_gold"])
        rect(d, (75, 78 + bob, 84, 86 + bob), PAL["paper"], PAL["ink"])
        star(d, 85, 69 + bob, "gold_hi", 3)
    return img


def portrait(expression="neutral"):
    img = Image.new("RGBA", (128, 128), PAL["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (11, 9, 117, 124), PAL["hair"], PAL["ink"], 4)
    ellipse(d, (8, 52, 34, 122), PAL["hair"], PAL["ink"], 3)
    ellipse(d, (93, 52, 122, 122), PAL["hair"], PAL["ink"], 3)
    ellipse(d, (33, 25, 95, 91), PAL["skin"], PAL["ink"], 4)
    poly(d, [(18, 31), (48, 9), (63, 35), (89, 17), (108, 39), (96, 57), (29, 54)], PAL["hair"], PAL["ink"])
    pumpkin_pin(d, 18, 45, 2)
    rect(d, (45, 57, 57, 76), PAL["ink"])
    rect(d, (75, 57, 87, 76), PAL["ink"])
    rect(d, (49, 60, 53, 64), PAL["cream"])
    rect(d, (79, 60, 83, 64), PAL["cream"])
    rect(d, (29, 80, 43, 87), PAL["skin_shadow"])
    rect(d, (88, 80, 102, 87), PAL["skin_shadow"])
    if expression == "surprise":
        rect(d, (62, 86, 69, 97), PAL["ink"])
        draw_exclaim(d, 103, 25)
    else:
        line(d, [(56, 88), (65, 95), (76, 88)], PAL["ink"], 3)
    rect(d, (36, 104, 92, 128), PAL["deep_purple"], PAL["ink"], 3)
    rect(d, (43, 107, 85, 115), PAL["dusty_pink"])
    return img


def object_window():
    img = Image.new("RGBA", (160, 180), PAL["transparent"])
    d = ImageDraw.Draw(img)
    rect(d, (14, 8, 146, 166), PAL["black_soft"], PAL["dusty_pink"], 5)
    rect(d, (29, 23, 131, 151), PAL["night"], PAL["ink"], 3)
    rect(d, (76, 23, 85, 151), PAL["dusty_pink"])
    rect(d, (29, 87, 131, 96), PAL["dusty_pink"])
    ellipse(d, (102, 36, 128, 62), PAL["old_gold"])
    for x in [45, 62, 84, 106, 126]:
        line(d, [(x, 28), (x - 22, 150)], PAL["rain"], 3)
    for y in [35, 116]:
        for x in [42, 99]:
            star(d, x, y, "lavender_hi", 2)
    rect(d, (4, 74, 31, 174), PAL["deep_purple"], PAL["ink"])
    rect(d, (130, 74, 156, 174), PAL["deep_purple"], PAL["ink"])
    return img


def object_bed():
    img = Image.new("RGBA", (280, 142), PAL["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (15, 95, 260, 136), PAL["shadow"])
    rect(d, (18, 22, 242, 95), PAL["black_soft"], PAL["ink"], 5)
    rect(d, (5, 56, 272, 126), PAL["lavender"], PAL["dusty_pink"], 5)
    rect(d, (20, 69, 252, 108), PAL["deep_purple"], PAL["ink"], 3)
    rect(d, (196, 66, 264, 124), PAL["pink_hi"], PAL["ink"], 3)
    rect(d, (28, 75, 188, 87), "#171021")
    rect(d, (20, 116, 252, 126), PAL["dusty_pink"])
    for x in range(36, 180, 30):
        rect(d, (x, 93, x + 12, 100), PAL["old_gold"])
    return img


def object_table():
    img = Image.new("RGBA", (132, 92), PAL["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (16, 72, 118, 89), PAL["shadow"])
    rect(d, (12, 20, 120, 55), PAL["wood0"], PAL["ink"], 4)
    rect(d, (22, 10, 110, 26), PAL["wood1"], PAL["ink"], 3)
    rect(d, (26, 52, 36, 82), PAL["wood0"], PAL["ink"])
    rect(d, (96, 52, 106, 82), PAL["wood0"], PAL["ink"])
    rect(d, (66, 18, 76, 55), PAL["old_gold"])
    rect(d, (84, 2, 101, 20), PAL["candle"], PAL["ink"])
    star(d, 98, 4, "gold_hi", 3)
    return img


def object_rug():
    img = Image.new("RGBA", (420, 156), PAL["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (8, 20, 412, 138), PAL["deep_purple"], PAL["ink"], 5)
    ellipse(d, (39, 42, 381, 118), "#372149", PAL["dusty_pink"], 3)
    rect(d, (92, 67, 328, 91), PAL["lavender"], PAL["ink"], 2)
    for x in range(56, 366, 42):
        rect(d, (x, 54, x + 16, 64), PAL["old_gold"])
        rect(d, (x, 98, x + 16, 108), PAL["old_gold"])
    for x in range(125, 290, 36):
        star(d, x, 78, "gold_hi", 3)
    return img


def object_boxes():
    img = Image.new("RGBA", (156, 120), PAL["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (11, 89, 138, 111), PAL["shadow"])
    rect(d, (16, 50, 70, 98), PAL["box"], PAL["ink"], 4)
    rect(d, (70, 32, 126, 82), PAL["box"], PAL["ink"], 4)
    rect(d, (82, 32, 92, 82), PAL["old_gold"])
    rect(d, (16, 64, 70, 74), PAL["box_hi"])
    rect(d, (28, 50, 38, 98), PAL["old_gold"])
    rect(d, (90, 54, 112, 68), PAL["paper"], PAL["ink"], 2)
    line(d, [(95, 60), (108, 60)], PAL["lavender"], 2)
    return img


def object_package():
    img = Image.new("RGBA", (128, 96), PAL["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (16, 69, 112, 88), PAL["shadow"])
    rect(d, (21, 29, 107, 79), PAL["box"], PAL["ink"], 4)
    rect(d, (55, 29, 73, 79), PAL["old_gold"], PAL["ink"], 2)
    rect(d, (21, 46, 107, 59), PAL["box_hi"], PAL["ink"], 2)
    rect(d, (76, 35, 100, 53), PAL["paper"], PAL["ink"], 2)
    line(d, [(80, 42), (95, 42)], PAL["lavender"], 2)
    line(d, [(80, 48), (90, 48)], PAL["lavender"], 2)
    for x, y in [(17, 22), (111, 23), (91, 14), (52, 18), (33, 11)]:
        star(d, x, y, "gold_hi", 5)
    return img


def object_door():
    img = Image.new("RGBA", (96, 172), PAL["transparent"])
    d = ImageDraw.Draw(img)
    rect(d, (16, 8, 80, 166), PAL["black_soft"], PAL["dusty_pink"], 5)
    rect(d, (28, 28, 68, 87), PAL["deep_purple"], PAL["ink"], 3)
    rect(d, (28, 99, 68, 151), PAL["deep_purple"], PAL["ink"], 3)
    rect(d, (63, 86, 71, 94), PAL["old_gold"], PAL["ink"])
    rect(d, (21, 14, 75, 22), PAL["old_gold"], PAL["ink"])
    star(d, 48, 18, "gold_hi", 3)
    return img


def ui_box(kind):
    if kind == "dialog":
        img = Image.new("RGBA", (928, 150), PAL["transparent"])
        d = ImageDraw.Draw(img)
        rect(d, (0, 0, 927, 149), "#0b0714", PAL["purple"], 5)
        rect(d, (8, 8, 919, 141), "#140b1c", PAL["dusty_pink"], 2)
        rect(d, (18, 18, 909, 131), "#1d1028")
        for x in [18, 28, 899, 909]:
            for y in [18, 28, 121, 131]:
                rect(d, (x, y, x + 4, y + 4), PAL["old_gold"])
        rect(d, (884, 118, 895, 129), PAL["old_gold"])
        return img
    if kind == "slot":
        img = Image.new("RGBA", (64, 64), PAL["transparent"])
        d = ImageDraw.Draw(img)
        rect(d, (3, 3, 61, 61), "#0b0714", PAL["purple"], 3)
        rect(d, (10, 10, 54, 54), "#20132c", PAL["lavender"], 2)
        rect(d, (14, 14, 50, 50), "#171021")
        return img
    if kind == "selector":
        img = Image.new("RGBA", (72, 72), PAL["transparent"])
        d = ImageDraw.Draw(img)
        rect(d, (2, 2, 69, 69), PAL["transparent"], PAL["old_gold"], 4)
        rect(d, (8, 8, 63, 63), PAL["transparent"], PAL["dusty_pink"], 2)
        for pos in [(8, 8), (63, 8), (8, 63), (63, 63)]:
            star(d, *pos, "gold_hi", 4)
        return img


def tile_sheet():
    img = Image.new("RGBA", (256, 128), PAL["transparent"])
    d = ImageDraw.Draw(img)
    for i in range(4):
        x = i * 32
        rect(d, (x, 0, x + 31, 31), PAL["bluewood"], PAL["ink"])
        line(d, [(x, 7), (x + 31, 4 + i * 3)], PAL["bluewood_hi"], 2)
        line(d, [(x, 23), (x + 31, 21 - i)], "#111936", 2)
        rect(d, (x + 2, 2, x + 4, 4), "#314071")
    for i in range(4):
        x = i * 32
        rect(d, (x, 32, x + 31, 63), PAL["deep_purple"], PAL["ink"])
        line(d, [(x + 8, 32), (x + 8, 63)], PAL["purple"], 2)
        line(d, [(x + 24, 32), (x + 24, 63)], PAL["purple"], 2)
        star(d, x + 16, 47, "lavender_hi", 2)
        rect(d, (x + 4, 36, x + 6, 38), PAL["dusty_pink"])
    rect(d, (0, 64, 127, 79), PAL["black_soft"], PAL["dusty_pink"], 2)
    rect(d, (0, 80, 127, 95), PAL["purple"], PAL["ink"], 2)
    rect(d, (128, 64, 159, 95), PAL["deep_purple"], PAL["dusty_pink"], 2)
    rect(d, (160, 64, 191, 95), PAL["shadow"])
    rect(d, (192, 64, 255, 95), PAL["transparent"])
    return img


def room_initial():
    img = Image.new("RGBA", (1024, 576), PAL["transparent"])
    d = ImageDraw.Draw(img)
    rect(d, (0, 0, 1024, 326), PAL["deep_purple"])
    for x in range(0, 1024, 48):
        rect(d, (x, 0, x + 24, 326), "#211230")
        line(d, [(x + 24, 0), (x + 24, 326)], PAL["purple"], 3)
        for y in range(42, 302, 64):
            star(d, x + 13, y, "lavender_hi", 2)
            rect(d, (x + 34, y + 10, x + 38, y + 14), PAL["dusty_pink"])
    for x in range(84, 960, 142):
        line(d, [(x, 34), (x, 82)], PAL["black_soft"], 2)
        rect(d, (x - 24, 82, x + 24, 136), PAL["transparent"], PAL["old_gold"], 3)
        for bar in range(x - 18, x + 19, 9):
            line(d, [(bar, 88), (bar, 130)], PAL["cream"], 2)
        ellipse(d, (x - 18, 72, x + 18, 102), PAL["transparent"], PAL["old_gold"], 3)
        star(d, x + 16, 78, "gold_hi", 2)
    rect(d, (505, 72, 642, 112), PAL["black_soft"], PAL["old_gold"], 3)
    for x in range(520, 628, 18):
        rect(d, (x, 83, x + 10, 106), ["#6a4a8a", "#d98ab6", "#c99b54"][(x // 18) % 3], PAL["ink"])
    rect(d, (108, 132, 196, 202), PAL["black_soft"], PAL["old_gold"], 4)
    rect(d, (124, 148, 180, 187), "#120f2b", PAL["dusty_pink"], 3)
    rect(d, (132, 156, 172, 180), "#1b2446")
    line(d, [(132, 178), (170, 156)], PAL["rain"], 2)
    rect(d, (350, 98, 428, 158), PAL["black_soft"], PAL["old_gold"], 4)
    rect(d, (365, 112, 413, 143), PAL["deep_purple"], PAL["dusty_pink"], 2)
    pumpkin_pin(d, 384, 119, 2)
    rect(d, (760, 116, 842, 164), PAL["black_soft"], PAL["old_gold"], 4)
    rect(d, (772, 128, 832, 153), PAL["paper"], PAL["ink"], 2)
    line(d, [(780, 140), (824, 140)], PAL["lavender"], 2)
    rect(d, (0, 0, 32, 576), "#160d22")
    rect(d, (992, 0, 1024, 576), "#160d22")
    rect(d, (0, 0, 1024, 32), "#100814")
    rect(d, (0, 275, 1024, 326), PAL["black_soft"])
    for x in range(0, 1024, 32):
        rect(d, (x, 286, x + 18, 323), PAL["purple"], PAL["ink"])
    rect(d, (0, 300, 1024, 314), PAL["dusty_pink"])
    rect(d, (0, 314, 1024, 576), "#1d1830")
    for x in range(-80, 1120, 72):
        poly(d, [(x, 576), (x + 64, 576), (x + 112, 314), (x + 47, 314)], PAL["bluewood"], PAL["ink"])
        line(d, [(x + 28, 576), (x + 77, 314)], PAL["bluewood_hi"], 2)
        line(d, [(x + 58, 576), (x + 107, 314)], "#111936", 2)
    for x in range(0, 1024, 64):
        line(d, [(x, 336), (x + 18, 326)], "#28345f", 2)
    rect(d, (0, 326, 1024, 348), "#12142f")
    for x in range(0, 1024, 38):
        rect(d, (x, 329, x + 16, 342), "#1b2446")
    ellipse(d, (65, 414, 425, 500), "#2b2138")
    ellipse(d, (408, 432, 828, 524), "#2b2138")
    img.alpha_composite(object_rug(), (285, 371))
    img.alpha_composite(object_table(), (466, 352))
    img.alpha_composite(object_boxes(), (620, 364))
    return img


def object_shelf():
    img = Image.new("RGBA", (170, 130), PAL["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (18, 106, 154, 124), PAL["shadow"])
    rect(d, (16, 10, 154, 116), PAL["black_soft"], PAL["old_gold"], 4)
    for y in (36, 66, 96):
        rect(d, (24, y, 146, y + 5), PAL["old_gold"])
    for x in range(28, 140, 14):
        h = 20 + (x % 4) * 4
        rect(d, (x, 36 - h, x + 8, 34), ["#6a4a8a", "#d98ab6", "#3b2058", "#c99b54"][(x // 14) % 4], PAL["ink"])
    for x in range(34, 132, 16):
        rect(d, (x, 66 - 18, x + 9, 64), ["#8f5062", "#6a4a8a", "#ead6bd"][(x // 16) % 3], PAL["ink"])
    pumpkin_pin(d, 30, 78, 2)
    star(d, 116, 80, "gold_hi", 4)
    rect(d, (78, 74, 106, 96), PAL["paper"], PAL["ink"], 2)
    line(d, [(83, 83), (100, 83)], PAL["lavender"], 2)
    return img


def object_lamp():
    img = Image.new("RGBA", (84, 120), PAL["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (8, 102, 76, 116), PAL["shadow"])
    rect(d, (38, 46, 45, 96), PAL["old_gold"], PAL["ink"])
    rect(d, (20, 96, 63, 108), PAL["wood0"], PAL["ink"], 3)
    poly(d, [(18, 18), (66, 18), (57, 52), (27, 52)], PAL["dusty_pink"], PAL["ink"])
    rect(d, (29, 26, 55, 46), PAL["candle"])
    star(d, 42, 12, "gold_hi", 6)
    star(d, 62, 35, "gold_hi", 3)
    star(d, 22, 41, "gold_hi", 3)
    return img


def object_plant():
    img = Image.new("RGBA", (82, 104), PAL["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (8, 86, 72, 101), PAL["shadow"])
    rect(d, (24, 65, 60, 94), PAL["wood1"], PAL["ink"], 3)
    rect(d, (20, 59, 64, 70), PAL["old_gold"], PAL["ink"], 2)
    for pts in [
        [(41, 62), (22, 42), (30, 28), (46, 58)],
        [(43, 62), (64, 39), (58, 25), (46, 58)],
        [(42, 59), (35, 31), (45, 12), (50, 58)],
        [(39, 62), (18, 59), (14, 45), (40, 55)],
    ]:
        poly(d, pts, "#708e63", PAL["ink"])
    return img


def object_plush():
    img = Image.new("RGBA", (92, 96), PAL["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (16, 76, 78, 91), PAL["shadow"])
    ellipse(d, (22, 28, 70, 78), PAL["lavender"], PAL["ink"], 3)
    ellipse(d, (12, 6, 34, 40), PAL["lavender"], PAL["ink"], 3)
    ellipse(d, (58, 6, 80, 40), PAL["lavender"], PAL["ink"], 3)
    rect(d, (34, 45, 39, 51), PAL["ink"])
    rect(d, (54, 45, 59, 51), PAL["ink"])
    line(d, [(42, 59), (47, 63), (54, 59)], PAL["ink"], 2)
    rect(d, (34, 71, 42, 85), PAL["dusty_pink"], PAL["ink"])
    rect(d, (51, 71, 60, 85), PAL["dusty_pink"], PAL["ink"])
    return img


def object_letters():
    img = Image.new("RGBA", (112, 82), PAL["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (14, 64, 98, 78), PAL["shadow"])
    rect(d, (18, 28, 70, 58), PAL["paper"], PAL["ink"], 3)
    line(d, [(20, 30), (44, 45), (68, 30)], PAL["dusty_pink"], 2)
    rect(d, (56, 18, 94, 48), PAL["paper"], PAL["ink"], 3)
    line(d, [(62, 29), (87, 29)], PAL["lavender"], 2)
    line(d, [(62, 36), (80, 36)], PAL["lavender"], 2)
    star(d, 89, 18, "gold_hi", 4)
    return img


def object_vanity():
    img = Image.new("RGBA", (154, 148), PAL["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (14, 128, 140, 144), PAL["shadow"])
    rect(d, (18, 86, 136, 118), PAL["wood0"], PAL["ink"], 4)
    rect(d, (28, 96, 58, 112), PAL["deep_purple"], PAL["old_gold"], 2)
    rect(d, (94, 96, 124, 112), PAL["deep_purple"], PAL["old_gold"], 2)
    ellipse(d, (46, 4, 108, 78), PAL["black_soft"], PAL["old_gold"], 4)
    ellipse(d, (56, 14, 98, 68), PAL["night"], PAL["dusty_pink"], 2)
    line(d, [(61, 62), (93, 20)], PAL["rain"], 2)
    rect(d, (34, 118, 45, 140), PAL["wood0"], PAL["ink"])
    rect(d, (108, 118, 119, 140), PAL["wood0"], PAL["ink"])
    star(d, 116, 72, "gold_hi", 4)
    return img


def room_initial():
    img = Image.new("RGBA", (1024, 576), PAL["transparent"])
    d = ImageDraw.Draw(img)
    rect(d, (0, 0, 1024, 326), PAL["deep_purple"])
    for x in range(0, 1024, 48):
        rect(d, (x, 0, x + 24, 326), "#211230")
        line(d, [(x + 24, 0), (x + 24, 326)], PAL["purple"], 3)
        for y in range(42, 302, 64):
            star(d, x + 13, y, "lavender_hi", 2)
            rect(d, (x + 34, y + 10, x + 38, y + 14), PAL["dusty_pink"])
    for x in range(78, 965, 128):
        line(d, [(x, 28), (x, 74)], PAL["black_soft"], 2)
        rect(d, (x - 22, 74, x + 22, 130), PAL["transparent"], PAL["old_gold"], 3)
        ellipse(d, (x - 18, 64, x + 18, 96), PAL["transparent"], PAL["old_gold"], 3)
        for bar in range(x - 16, x + 17, 8):
            line(d, [(bar, 80), (bar, 124)], PAL["cream"], 2)
    img.alpha_composite(object_shelf(), (454, 48))
    img.alpha_composite(object_vanity(), (692, 120))
    rect(d, (108, 132, 196, 202), PAL["black_soft"], PAL["old_gold"], 4)
    rect(d, (124, 148, 180, 187), "#120f2b", PAL["dusty_pink"], 3)
    rect(d, (132, 156, 172, 180), "#1b2446")
    line(d, [(132, 178), (170, 156)], PAL["rain"], 2)
    rect(d, (350, 98, 428, 158), PAL["black_soft"], PAL["old_gold"], 4)
    rect(d, (365, 112, 413, 143), PAL["deep_purple"], PAL["dusty_pink"], 2)
    pumpkin_pin(d, 384, 119, 2)
    rect(d, (760, 116, 842, 164), PAL["black_soft"], PAL["old_gold"], 4)
    rect(d, (772, 128, 832, 153), PAL["paper"], PAL["ink"], 2)
    line(d, [(780, 140), (824, 140)], PAL["lavender"], 2)
    rect(d, (0, 0, 32, 576), "#160d22")
    rect(d, (992, 0, 1024, 576), "#160d22")
    rect(d, (0, 0, 1024, 32), "#100814")
    rect(d, (0, 275, 1024, 326), PAL["black_soft"])
    for x in range(0, 1024, 32):
        rect(d, (x, 286, x + 18, 323), PAL["purple"], PAL["ink"])
    rect(d, (0, 300, 1024, 314), PAL["dusty_pink"])
    rect(d, (0, 314, 1024, 576), "#1d1830")
    for x in range(-80, 1120, 72):
        poly(d, [(x, 576), (x + 64, 576), (x + 112, 314), (x + 47, 314)], PAL["bluewood"], PAL["ink"])
        line(d, [(x + 28, 576), (x + 77, 314)], PAL["bluewood_hi"], 2)
        line(d, [(x + 58, 576), (x + 107, 314)], "#111936", 2)
    for x in range(0, 1024, 64):
        line(d, [(x, 336), (x + 18, 326)], "#28345f", 2)
    rect(d, (0, 326, 1024, 348), "#12142f")
    for x in range(0, 1024, 38):
        rect(d, (x, 329, x + 16, 342), "#1b2446")
    ellipse(d, (65, 414, 425, 500), "#2b2138")
    ellipse(d, (408, 432, 828, 524), "#2b2138")
    img.alpha_composite(object_lamp(), (44, 330))
    img.alpha_composite(object_rug(), (285, 371))
    img.alpha_composite(object_table(), (466, 352))
    img.alpha_composite(object_boxes(), (620, 364))
    img.alpha_composite(object_plant(), (884, 368))
    img.alpha_composite(object_plush(), (812, 412))
    img.alpha_composite(object_letters(), (258, 404))
    return img


def main():
    for folder in ("characters", "tilesets", "ui", "objects"):
        (OUT / folder).mkdir(parents=True, exist_ok=True)

    char_specs = {
        "idle_down.png": ("down", 0, "idle"),
        "walk_down_1.png": ("down", 1, "idle"),
        "walk_down_2.png": ("down", 2, "idle"),
        "idle_up.png": ("up", 0, "idle"),
        "walk_up_1.png": ("up", 1, "idle"),
        "walk_up_2.png": ("up", 2, "idle"),
        "idle_side.png": ("side", 0, "idle"),
        "walk_side_1.png": ("side", 1, "idle"),
        "walk_side_2.png": ("side", 2, "idle"),
        "interact.png": ("down", 0, "interact"),
        "surprise.png": ("down", 0, "surprise"),
        "hold_package.png": ("down", 0, "package"),
    }
    for name, args in char_specs.items():
        save(character(*args), "characters", name)
    save(portrait("neutral"), "characters", "portrait_neutral.png")
    save(portrait("surprise"), "characters", "portrait_surprise.png")

    save(tile_sheet(), "tilesets", "initial_room_tileset.png")
    save(room_initial(), "tilesets", "initial_room.png")

    save(object_bed(), "objects", "bed.png")
    save(object_table(), "objects", "table.png")
    save(object_rug(), "objects", "rug.png")
    save(object_boxes(), "objects", "boxes.png")
    save(object_package(), "objects", "package_glow.png")
    save(object_window(), "objects", "window_rain.png")
    save(object_door(), "objects", "door.png")
    save(object_shelf(), "objects", "shelf.png")
    save(object_lamp(), "objects", "lamp.png")
    save(object_plant(), "objects", "plant.png")
    save(object_plush(), "objects", "plush.png")
    save(object_letters(), "objects", "letters.png")
    save(object_vanity(), "objects", "vanity.png")

    save(ui_box("dialog"), "ui", "dialog_box.png")
    save(ui_box("slot"), "ui", "inventory_slot.png")
    save(ui_box("selector"), "ui", "selector.png")
    for name in ("package", "key", "invitation", "cursor", "hat", "cape", "boots", "wand", "accessory"):
        save(icon(name), "ui", f"icon_{name}.png")


if __name__ == "__main__":
    main()
