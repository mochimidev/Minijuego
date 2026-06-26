from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "web-emulator" / "pixel-v2"

P = {
    "transparent": (0, 0, 0, 0),
    "ink": "#120815",
    "ink2": "#241022",
    "deep": "#17102f",
    "violet0": "#231542",
    "violet1": "#3d2063",
    "violet2": "#6b3490",
    "violet3": "#a86cf1",
    "pink0": "#f29ad7",
    "pink1": "#ffc0dc",
    "skin0": "#ffd2bf",
    "skin1": "#f29a9b",
    "hair0": "#25101d",
    "hair1": "#4b1e30",
    "hair2": "#8a3d50",
    "orange0": "#f1842c",
    "orange1": "#ffb347",
    "gold": "#ffd36b",
    "cream": "#fff2c7",
    "green": "#7ac66b",
    "stone0": "#3b3158",
    "stone1": "#6f5b87",
    "wood0": "#4b263a",
    "wood1": "#9a5365",
    "blue0": "#202f66",
    "red": "#ff5f8d",
    "white": "#fff6ff",
}


def c(hex_color, a=255):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def out(rel):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save(img, rel):
    img.save(out(rel))


def rect(d, xy, fill, outline=None, width=1):
    d.rectangle(xy, fill=c(fill), outline=c(outline) if outline else None, width=width)


def ellipse(d, xy, fill, outline=None, width=1):
    d.ellipse(xy, fill=c(fill), outline=c(outline) if outline else None, width=width)


def poly(d, points, fill, outline=None):
    d.polygon(points, fill=c(fill), outline=c(outline) if outline else None)


def line(d, points, fill, width=1):
    d.line(points, fill=c(fill), width=width)


def star(d, x, y, color="#ffd36b", size=3):
    rect(d, (x - 1, y - size, x + 1, y + size), color)
    rect(d, (x - size, y - 1, x + size, y + 1), color)
    rect(d, (x, y, x, y), P["cream"])


def character(outfit=0, pose="idle", pajama=False):
    img = Image.new("RGBA", (128, 144), P["transparent"])
    d = ImageDraw.Draw(img)

    walk = pose in ("walk1", "walk2")
    jump = pose == "jump"
    fall = pose == "fall"
    pickup = pose == "pickup"
    celebrate = pose == "celebrate"
    frame = -1 if pose == "walk1" else 1
    bob = -4 if jump or celebrate else 0

    has_boots = outfit >= 1 and not pajama
    has_cape = outfit >= 2 and not pajama
    has_hat = outfit >= 3 and not pajama
    has_wand = outfit >= 4 and not pajama
    has_bow = outfit >= 5 and not pajama

    # Ground shadow
    ellipse(d, (35, 124, 94, 134), "#0b0610")

    # Cape behind body.
    if has_cape:
        poly(d, [(39, 54 + bob), (21, 125), (63, 137), (107, 125), (88, 54 + bob)], P["ink"], P["pink0"])
        line(d, [(33, 111), (63, 130), (95, 111)], P["violet2"], 3)
        star(d, 94, 95, P["gold"], 4)

    # Hair mass.
    ellipse(d, (25, 11 + bob, 101, 92 + bob), P["hair0"], P["ink"], 4)
    ellipse(d, (16, 43 + bob, 51, 111 + bob), P["hair0"], P["ink"], 4)
    ellipse(d, (78, 38 + bob, 112, 108 + bob), P["hair0"], P["ink"], 4)
    line(d, [(25, 55 + bob), (18, 82 + bob), (30, 109 + bob)], P["hair2"], 4)
    line(d, [(96, 50 + bob), (110, 78 + bob), (96, 106 + bob)], P["hair2"], 4)
    line(d, [(43, 18 + bob), (35, 45 + bob)], P["hair1"], 4)
    line(d, [(78, 17 + bob), (91, 43 + bob)], P["hair1"], 4)

    # Hat or hair bow.
    if has_hat:
        poly(d, [(33, 25 + bob), (96, 25 + bob), (75, 3 + bob), (58, 4 + bob)], P["ink2"], P["pink0"])
        rect(d, (28, 26 + bob, 101, 34 + bob), P["ink2"], P["pink0"], 3)
        rect(d, (58, 20 + bob, 75, 27 + bob), P["gold"], P["ink"], 2)
        star(d, 91, 11 + bob, P["gold"], 4)
    else:
        poly(d, [(73, 13 + bob), (86, 4 + bob), (89, 21 + bob)], P["violet2"], P["pink0"])
        poly(d, [(93, 12 + bob), (108, 5 + bob), (103, 24 + bob)], P["violet2"], P["pink0"])
        rect(d, (87, 13 + bob, 95, 21 + bob), P["pink0"], P["ink"], 1)

    # Legs and feet.
    left_hip, right_hip = (52, 91), (76, 91)
    if walk:
        left_foot = (45 - frame * 7, 124)
        right_foot = (82 + frame * 7, 124)
    elif jump:
        left_foot = (48, 116)
        right_foot = (84, 113)
    elif fall:
        left_foot = (50, 125)
        right_foot = (78, 126)
    else:
        left_foot = (48, 125)
        right_foot = (82, 125)
    line(d, [left_hip, left_foot], P["skin0"], 8)
    line(d, [right_hip, right_foot], P["skin0"], 8)
    sock = P["pink0"] if not pajama else P["violet3"]
    rect(d, (left_foot[0] - 7, left_foot[1] - 11, left_foot[0] + 5, left_foot[1] - 5), sock, P["ink"], 2)
    rect(d, (right_foot[0] - 5, right_foot[1] - 11, right_foot[0] + 8, right_foot[1] - 5), sock, P["ink"], 2)
    boot_col = P["ink2"] if has_boots else P["violet2"]
    rect(d, (left_foot[0] - 13, left_foot[1] - 5, left_foot[0] + 8, left_foot[1] + 6), boot_col, P["ink"], 3)
    rect(d, (right_foot[0] - 8, right_foot[1] - 5, right_foot[0] + 15, right_foot[1] + 6), boot_col, P["ink"], 3)
    if has_boots:
        rect(d, (left_foot[0] - 5, left_foot[1] - 2, left_foot[0] + 3, left_foot[1] + 1), P["orange1"])
        rect(d, (right_foot[0] - 1, right_foot[1] - 2, right_foot[0] + 7, right_foot[1] + 1), P["orange1"])

    # Body/dress.
    body = P["pink0"] if pajama else P["deep"]
    trim = P["violet3"] if pajama else P["pink0"]
    rect(d, (43, 59 + bob, 84, 91 + bob), body, P["ink"], 4)
    poly(d, [(38, 87 + bob), (90, 87 + bob), (100, 109 + bob), (29, 109 + bob)], body, P["ink"])
    rect(d, (39, 87 + bob, 91, 93 + bob), trim)
    rect(d, (55, 65 + bob, 72, 72 + bob), P["gold"], P["ink"], 2)
    if pajama:
        for yy in (68, 79, 90):
            line(d, [(45, yy + bob), (82, yy + bob)], P["violet3"], 3)
    if has_bow:
        poly(d, [(82, 73 + bob), (101, 62 + bob), (98, 85 + bob), (84, 81 + bob)], P["violet2"], P["pink0"])
        poly(d, [(113, 73 + bob), (96, 62 + bob), (99, 85 + bob), (112, 81 + bob)], P["violet2"], P["pink0"])
        ellipse(d, (95, 70 + bob, 102, 78 + bob), P["pink0"], P["ink"])

    # Arms.
    ay = 70 + bob
    if celebrate:
        line(d, [(43, ay), (26, ay - 31)], P["skin0"], 8)
        line(d, [(84, ay), (104, ay - 33)], P["skin0"], 8)
        star(d, 107, ay - 37, P["gold"], 7)
    elif pickup:
        line(d, [(43, ay), (24, ay + 24)], P["skin0"], 8)
        line(d, [(84, ay), (105, ay + 20)], P["skin0"], 8)
    else:
        l_end = (29, ay + (15 if not walk else 10 + frame * 9))
        r_end = (101, ay + (15 if not walk else 10 - frame * 9))
        if jump:
            l_end, r_end = (30, ay + 5), (101, ay + 3)
        if fall:
            l_end, r_end = (30, ay + 20), (100, ay + 22)
        line(d, [(43, ay), l_end], P["skin0"], 8)
        line(d, [(84, ay), r_end], P["skin0"], 8)
    if has_wand:
        line(d, [(103, ay + 9), (120, ay - 18)], P["gold"], 4)
        star(d, 120, ay - 20, P["pink0"], 6)

    # Face.
    ellipse(d, (39, 24 + bob, 88, 73 + bob), P["skin0"], P["ink"], 4)
    # Bangs over face.
    poly(d, [(34, 29 + bob), (49, 13 + bob), (64, 30 + bob), (82, 17 + bob), (93, 31 + bob), (88, 43 + bob), (38, 42 + bob)], P["hair0"], P["ink"])
    line(d, [(45, 30 + bob), (52, 43 + bob)], P["hair2"], 3)
    line(d, [(73, 27 + bob), (68, 43 + bob)], P["hair2"], 3)
    # Eyes.
    rect(d, (48, 47 + bob, 56, 59 + bob), P["ink"])
    rect(d, (72, 47 + bob, 80, 59 + bob), P["ink"])
    rect(d, (50, 48 + bob, 52, 51 + bob), P["white"])
    rect(d, (74, 48 + bob, 76, 51 + bob), P["white"])
    rect(d, (46, 61 + bob, 54, 65 + bob), P["skin1"])
    rect(d, (76, 61 + bob, 84, 65 + bob), P["skin1"])
    if fall:
        line(d, [(60, 66 + bob), (69, 66 + bob)], P["ink"], 2)
    elif pickup:
        rect(d, (62, 65 + bob, 67, 70 + bob), P["ink"])
    else:
        line(d, [(59, 66 + bob), (64, 70 + bob), (71, 66 + bob)], P["ink"], 2)

    # Pumpkin clip.
    ellipse(d, (22, 31 + bob, 40, 49 + bob), P["orange0"], P["ink"], 3)
    rect(d, (30, 27 + bob, 34, 32 + bob), P["green"])
    rect(d, (28, 39 + bob, 31, 42 + bob), P["ink"])
    rect(d, (35, 39 + bob, 38, 42 + bob), P["ink"])
    line(d, [(30, 45 + bob), (34, 47 + bob), (38, 45 + bob)], P["gold"], 2)

    return img


def collectible(kind):
    img = Image.new("RGBA", (80, 80), P["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (9, 9, 71, 71), "#2a1740")
    for pos in [(15, 18), (65, 21), (58, 62), (20, 58)]:
        star(d, *pos, P["gold"], 4)
    if kind == "hat":
        poly(d, [(15, 53), (66, 53), (48, 17), (34, 17)], P["ink2"], P["pink0"])
        rect(d, (10, 53, 70, 63), P["ink2"], P["pink0"], 3)
        rect(d, (34, 44, 51, 50), P["gold"], P["ink"], 2)
    elif kind == "cape":
        poly(d, [(28, 16), (53, 16), (66, 65), (40, 55), (14, 65)], P["ink2"], P["pink0"])
        line(d, [(30, 20), (40, 55), (51, 20)], P["violet3"], 4)
        star(d, 54, 48, P["gold"], 4)
    elif kind == "boots":
        rect(d, (19, 22, 34, 55), P["ink2"], P["pink0"], 3)
        rect(d, (42, 22, 57, 55), P["ink2"], P["pink0"], 3)
        rect(d, (15, 52, 36, 66), P["ink2"], P["ink"], 3)
        rect(d, (40, 52, 64, 66), P["ink2"], P["ink"], 3)
        rect(d, (24, 38, 31, 43), P["orange1"])
        rect(d, (47, 38, 54, 43), P["orange1"])
    elif kind == "wand":
        line(d, [(21, 63), (58, 23)], P["gold"], 5)
        star(d, 60, 21, P["pink0"], 9)
        star(d, 68, 13, P["gold"], 5)
    elif kind == "accessory":
        poly(d, [(22, 34), (7, 22), (12, 55), (24, 45)], P["violet2"], P["pink0"])
        poly(d, [(58, 34), (73, 22), (68, 55), (56, 45)], P["violet2"], P["pink0"])
        ellipse(d, (31, 31, 49, 49), P["pink0"], P["ink"], 3)
        star(d, 40, 40, P["gold"], 4)
    return img


def enemy(kind):
    img = Image.new("RGBA", (96, 96), P["transparent"])
    d = ImageDraw.Draw(img)
    ellipse(d, (25, 78, 71, 88), "#0b0610")
    if kind == "ghost":
        ellipse(d, (22, 10, 74, 63), "#f3d9ff", P["ink"], 4)
        rect(d, (22, 41, 74, 74), "#f3d9ff", P["ink"], 4)
        poly(d, [(22, 74), (31, 63), (40, 74), (49, 63), (58, 74), (74, 62), (74, 78), (22, 78)], "#f3d9ff", P["ink"])
        rect(d, (38, 34, 45, 44), P["ink"])
        rect(d, (56, 34, 63, 44), P["ink"])
        line(d, [(43, 55), (50, 60), (58, 55)], P["ink"], 3)
        rect(d, (66, 19, 73, 27), P["violet3"], P["ink"])
    elif kind == "shadow":
        ellipse(d, (20, 17, 76, 74), "#100613", P["pink0"], 4)
        poly(d, [(23, 64), (14, 83), (35, 73), (48, 88), (61, 73), (82, 83), (73, 64)], "#100613", P["pink0"])
        rect(d, (38, 43, 45, 50), P["pink0"])
        rect(d, (57, 43, 64, 50), P["pink0"])
        star(d, 74, 25, P["pink0"], 4)
    elif kind == "doll":
        ellipse(d, (27, 10, 69, 54), P["pink1"], P["ink"], 4)
        poly(d, [(24, 52), (72, 52), (82, 80), (16, 80)], P["violet2"], P["ink"])
        poly(d, [(26, 13), (12, 40), (33, 31)], P["hair0"], P["ink"])
        poly(d, [(68, 13), (85, 40), (63, 31)], P["hair0"], P["ink"])
        rect(d, (38, 28, 44, 37), P["ink"])
        rect(d, (56, 28, 62, 37), P["ink"])
        line(d, [(43, 45), (50, 49), (58, 45)], P["ink"], 2)
        rect(d, (25, 80, 39, 90), P["ink2"], P["ink"])
        rect(d, (58, 80, 72, 90), P["ink2"], P["ink"])
    elif kind == "pumpkin":
        ellipse(d, (19, 24, 77, 77), P["orange0"], P["ink"], 4)
        rect(d, (45, 15, 52, 25), P["green"], P["ink"])
        rect(d, (36, 43, 43, 50), P["cream"])
        rect(d, (57, 43, 64, 50), P["cream"])
        line(d, [(35, 62), (48, 69), (63, 62)], P["ink"], 4)
        line(d, [(20, 53), (6, 43)], P["orange0"], 7)
        line(d, [(76, 53), (91, 43)], P["orange0"], 7)
    return img


def platform(kind):
    img = Image.new("RGBA", (256, 64), P["transparent"])
    d = ImageDraw.Draw(img)
    if kind == "wood":
        rect(d, (7, 22, 248, 53), P["wood0"], P["ink"], 4)
        rect(d, (14, 14, 241, 28), P["wood1"], P["ink"], 3)
        rect(d, (23, 20, 231, 24), P["pink1"])
        for x in range(30, 230, 38):
            line(d, [(x, 29), (x - 7, 52)], P["ink2"], 3)
        star(d, 226, 17, P["gold"], 4)
    elif kind == "tomb":
        for x in range(12, 229, 34):
            rect(d, (x, 16, x + 26, 52), P["stone0"], P["ink"], 3)
            ellipse(d, (x, 7, x + 26, 31), P["stone0"], P["ink"], 3)
            rect(d, (x + 8, 25, x + 18, 28), P["stone1"])
        rect(d, (5, 49, 251, 61), P["violet1"], P["ink"], 4)
        rect(d, (13, 43, 242, 48), P["pink0"])
    elif kind == "book":
        rect(d, (13, 25, 243, 55), P["deep"], P["ink"], 4)
        rect(d, (24, 13, 232, 37), P["violet2"], P["ink"], 4)
        rect(d, (35, 20, 220, 26), P["pink1"])
        rect(d, (34, 48, 221, 53), P["gold"])
        for x in range(50, 220, 54):
            rect(d, (x, 28, x + 8, 53), P["ink2"])
    elif kind == "branch":
        line(d, [(13, 41), (70, 24), (132, 34), (244, 21)], P["ink"], 22)
        line(d, [(13, 40), (70, 23), (132, 33), (244, 20)], P["hair2"], 7)
        line(d, [(76, 25), (49, 8)], P["ink"], 11)
        line(d, [(160, 28), (192, 6)], P["ink"], 10)
        for x, y in [(48, 9), (190, 7), (126, 28), (227, 21)]:
            rect(d, (x, y, x + 8, y + 8), P["pink0"], P["ink"])
    elif kind == "pumpkin":
        rect(d, (0, 40, 255, 61), P["deep"], P["ink"], 3)
        for x in range(9, 237, 42):
            ellipse(d, (x, 9, x + 42, 51), P["orange0"], P["ink"], 4)
            rect(d, (x + 19, 4, x + 25, 11), P["green"], P["ink"])
            rect(d, (x + 14, 26, x + 19, 31), P["cream"])
            rect(d, (x + 27, 26, x + 32, 31), P["cream"])
            line(d, [(x + 15, 38), (x + 22, 42), (x + 31, 38)], P["ink"], 2)
        rect(d, (0, 36, 255, 42), P["pink0"])
    elif kind == "parcel":
        rect(d, (13, 18, 243, 56), "#74454e", P["ink"], 4)
        rect(d, (120, 18, 136, 56), P["gold"], P["ink"], 2)
        rect(d, (13, 30, 243, 41), "#b96b5a", P["ink"], 2)
        star(d, 224, 20, P["gold"], 5)
    return img


def ui(kind):
    img = Image.new("RGBA", (48, 48), P["transparent"])
    d = ImageDraw.Draw(img)
    if kind == "heart_full":
        ellipse(d, (7, 10, 25, 28), P["red"], P["ink"], 3)
        ellipse(d, (23, 10, 41, 28), P["red"], P["ink"], 3)
        poly(d, [(6, 22), (42, 22), (24, 42)], P["red"], P["ink"])
        rect(d, (15, 15, 18, 18), P["pink1"])
    elif kind == "heart_empty":
        ellipse(d, (7, 10, 25, 28), P["violet1"], P["ink"], 3)
        ellipse(d, (23, 10, 41, 28), P["violet1"], P["ink"], 3)
        poly(d, [(6, 22), (42, 22), (24, 42)], P["violet1"], P["ink"])
    elif kind == "parcel":
        rect(d, (8, 15, 40, 38), "#74454e", P["ink"], 3)
        rect(d, (22, 15, 27, 38), P["gold"])
        rect(d, (8, 23, 40, 28), "#b96b5a")
    return img


def decor(kind):
    img = Image.new("RGBA", (96, 96), P["transparent"])
    d = ImageDraw.Draw(img)
    if kind == "package":
        rect(d, (15, 34, 81, 75), "#74454e", P["ink"], 4)
        rect(d, (42, 34, 54, 75), P["gold"], P["ink"], 2)
        rect(d, (15, 48, 81, 58), "#b96b5a", P["ink"], 2)
        star(d, 74, 25, P["gold"], 6)
        star(d, 24, 29, P["pink0"], 4)
    elif kind == "door":
        rect(d, (23, 11, 73, 88), P["ink2"], P["pink0"], 4)
        rect(d, (33, 23, 62, 51), P["violet1"], P["ink"], 3)
        rect(d, (58, 60, 64, 66), P["gold"], P["ink"])
    elif kind == "lamp":
        line(d, [(48, 0), (48, 19)], P["ink"], 3)
        ellipse(d, (31, 15, 65, 31), P["ink"], P["gold"], 2)
        rect(d, (32, 25, 64, 66), P["ink"], P["gold"], 3)
        rect(d, (40, 32, 56, 56), P["orange1"], P["gold"], 2)
        star(d, 48, 45, P["cream"], 5)
    elif kind == "window":
        rect(d, (15, 9, 81, 82), P["ink"], P["pink0"], 4)
        rect(d, (25, 19, 71, 72), P["blue0"], P["ink"], 2)
        line(d, [(48, 19), (48, 72)], P["pink0"], 2)
        line(d, [(25, 45), (71, 45)], P["pink0"], 2)
        for rx in [31, 47, 64]:
            line(d, [(rx, 21), (rx - 6, 70)], P["violet3"], 2)
        ellipse(d, (58, 24, 72, 38), P["gold"])
    return img


def background(kind):
    img = Image.new("RGBA", (512, 288), c(P["deep"]))
    d = ImageDraw.Draw(img)
    for y, col in [(0, "#0d0920"), (54, "#17102f"), (112, "#2d1852"), (188, "#3b1d55")]:
        rect(d, (0, y, 512, min(288, y + 70)), col)
    if kind == "menu":
        ellipse(d, (45, 36, 125, 116), P["gold"])
        ellipse(d, (72, 25, 147, 100), P["deep"])
        rect(d, (182, 106, 330, 238), P["deep"], P["pink0"], 3)
        poly(d, [(168, 106), (256, 43), (346, 106)], P["violet0"], P["pink0"])
        for x in [210, 286]:
            rect(d, (x, 151, x + 35, 203), P["ink"], P["pink0"], 2)
            rect(d, (x + 9, 165, x + 24, 195), P["orange0"])
        rect(d, (0, 238, 512, 288), "#151020")
        fence(d)
    elif kind in ("bedroom", "hallway", "library"):
        rect(d, (0, 0, 512, 193), "#1d1432")
        for x in range(0, 512, 50):
            rect(d, (x, 0, x + 30, 193), "#25183f")
            line(d, [(x + 31, 0), (x + 31, 193)], "#3d265b", 2)
        rect(d, (0, 193, 512, 288), "#211326")
        for x in range(-30, 530, 58):
            poly(d, [(x, 288), (x + 56, 288), (x + 80, 193), (x + 22, 193)], "#2e1b34", P["ink"])
        if kind == "bedroom":
            window(d, 356, 34)
            rect(d, (40, 138, 188, 191), "#4b2549", P["pink0"], 3)
            rect(d, (56, 116, 169, 150), "#2b1835", P["ink"], 3)
            rect(d, (51, 154, 177, 179), P["pink1"], P["ink"], 2)
        elif kind == "hallway":
            window(d, 226, 28)
            for x in [70, 395]:
                rect(d, (x, 78, x + 54, 190), "#24152e", P["pink0"], 3)
                rect(d, (x + 39, 138, x + 45, 144), P["gold"])
        elif kind == "library":
            for x in [32, 336]:
                rect(d, (x, 70, x + 120, 193), "#20152b", P["pink0"], 3)
                for yy in range(85, 180, 25):
                    line(d, [(x + 8, yy), (x + 112, yy)], "#a15c64", 2)
                    for xx in range(x + 14, x + 100, 18):
                        rect(d, (xx, yy - 16, xx + 10, yy - 2), P["violet2"])
            window(d, 226, 24)
    elif kind in ("garden", "cemetery", "party"):
        ellipse(d, (249, 24, 335, 110), "#f5c77c")
        ellipse(d, (278, 14, 351, 91), "#19113a")
        for x in [20, 92, 382, 455]:
            line(d, [(x, 192), (x + 35, 42)], P["ink"], 8)
            line(d, [(x + 12, 112), (x + 50, 90)], P["ink"], 4)
        fence(d)
        rect(d, (0, 232, 512, 288), "#21162d")
        if kind == "cemetery":
            for x in [70, 118, 352, 420]:
                rect(d, (x, 183, x + 34, 232), P["stone0"], P["ink"], 3)
                ellipse(d, (x, 165, x + 34, 201), P["stone0"], P["ink"], 3)
        elif kind == "garden":
            for x in range(35, 480, 78):
                rect(d, (x, 217, x + 16, 248), P["green"])
                ellipse(d, (x - 8, 197, x + 24, 225), P["orange0"], P["ink"], 3)
        elif kind == "party":
            for x in range(30, 470, 44):
                line(d, [(x, 62), (x + 28, 82)], P["gold"], 2)
                poly(d, [(x + 6, 68), (x + 20, 76), (x + 7, 92)], P["orange0"], P["ink"])
            rect(d, (164, 128, 350, 231), "#25163b", P["pink0"], 3)
            for x in [192, 292]:
                rect(d, (x, 156, x + 32, 202), P["orange0"], P["ink"], 3)
    return img


def fence(d):
    for x in range(0, 512, 56):
        line(d, [(x, 230), (x + 23, 174)], P["ink"], 6)
    line(d, [(0, 219), (512, 206)], P["ink"], 6)


def window(d, x, y):
    rect(d, (x, y, x + 84, y + 112), P["ink"], P["pink0"], 3)
    rect(d, (x + 10, y + 11, x + 74, y + 100), P["blue0"])
    line(d, [(x + 42, y + 11), (x + 42, y + 100)], P["pink0"], 2)
    line(d, [(x + 10, y + 55), (x + 74, y + 55)], P["pink0"], 2)
    for rx in [x + 18, x + 38, x + 62]:
        line(d, [(rx, y + 14), (rx - 9, y + 98)], P["violet3"], 2)


def make_sheet():
    cells = [
        ("pajama_idle", "Characters/pajama_idle.png"),
        ("pajama_worry", "Characters/pajama_worry.png"),
        ("idle", "Characters/idle.png"),
        ("walk_1", "Characters/walk_1.png"),
        ("walk_2", "Characters/walk_2.png"),
        ("jump", "Characters/jump.png"),
        ("fall", "Characters/fall.png"),
        ("pickup", "Characters/pickup.png"),
        ("celebrate", "Characters/celebrate.png"),
        ("ghost", "Enemies/ghost.png"),
        ("shadow", "Enemies/shadow.png"),
        ("doll", "Enemies/doll.png"),
        ("pumpkin_monster", "Enemies/pumpkin_monster.png"),
        ("hat", "Collectibles/witch_hat.png"),
        ("cape", "Collectibles/magic_cape.png"),
        ("boots", "Collectibles/enchanted_boots.png"),
        ("wand", "Collectibles/magic_wand.png"),
        ("accessory", "Collectibles/moon_accessory.png"),
    ]
    sheet = Image.new("RGBA", (768, 576), (9, 7, 22, 255))
    d = ImageDraw.Draw(sheet)
    for i, (_, rel) in enumerate(cells):
        img = Image.open(out(rel))
        x = (i % 6) * 128
        y = (i // 6) * 192
        rect(d, (x + 4, y + 4, x + 124, y + 188), "#17102f", "#6b3490", 2)
        sheet.alpha_composite(img, (x, y + 18))
    sheet.save(out("sprite_sheet_preview.png"))


def main():
    for folder in ["Characters", "Collectibles", "Enemies", "Platforms", "Decor", "UI", "Backgrounds"]:
        (OUT / folder).mkdir(parents=True, exist_ok=True)

    char_specs = [
        ("pajama_idle.png", 0, "idle", True),
        ("pajama_worry.png", 0, "fall", True),
        ("idle.png", 5, "idle", False),
        ("walk_1.png", 5, "walk1", False),
        ("walk_2.png", 5, "walk2", False),
        ("jump.png", 5, "jump", False),
        ("fall.png", 5, "fall", False),
        ("pickup.png", 5, "pickup", False),
        ("celebrate.png", 5, "celebrate", False),
    ]
    for i in range(6):
        char_specs.append((f"progress_{i}.png", i, "idle", i == 0))
    for name, outfit, pose, pajama in char_specs:
        save(character(outfit, pose, pajama), f"Characters/{name}")

    for kind, name in [("hat", "witch_hat.png"), ("cape", "magic_cape.png"), ("boots", "enchanted_boots.png"), ("wand", "magic_wand.png"), ("accessory", "moon_accessory.png")]:
        save(collectible(kind), f"Collectibles/{name}")

    for kind in ["ghost", "shadow", "doll", "pumpkin"]:
        save(enemy(kind), f"Enemies/{'pumpkin_monster' if kind == 'pumpkin' else kind}.png")

    for kind in ["wood", "tomb", "book", "branch", "pumpkin", "parcel"]:
        save(platform(kind), f"Platforms/{kind}.png")

    for kind in ["heart_full", "heart_empty", "parcel"]:
        save(ui(kind), f"UI/{kind}.png")

    for kind in ["package", "door", "lamp", "window"]:
        save(decor(kind), f"Decor/{kind}.png")

    for kind in ["menu", "bedroom", "hallway", "library", "garden", "cemetery", "party"]:
        save(background(kind), f"Backgrounds/{kind}.png")

    make_sheet()


if __name__ == "__main__":
    main()
