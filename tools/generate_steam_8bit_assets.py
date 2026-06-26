from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "web-emulator" / "steam-8bit"
BG = OUT / "Backgrounds"
OBJ = OUT / "Objects"

PAL = {
    "ink": "#090714",
    "void": "#130b1f",
    "plum": "#25143c",
    "violet": "#432060",
    "lav": "#8d5bd4",
    "pink": "#f2a0d6",
    "gold": "#ffd36b",
    "amber": "#d98248",
    "mint": "#8df5c8",
    "blue": "#283a76",
    "fog": "#5d5376",
}


def ensure_dirs():
    BG.mkdir(parents=True, exist_ok=True)
    OBJ.mkdir(parents=True, exist_ok=True)


def img(w, h, transparent=False):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0) if transparent else PAL["ink"])


def rect(d, xy, fill, outline=None, width=1):
    d.rectangle(xy, fill=fill, outline=outline, width=width)


def tri(d, pts, fill, outline=None):
    d.polygon(pts, fill=fill)
    if outline:
        d.line(pts + [pts[0]], fill=outline, width=1)


def star(d, x, y, color=PAL["gold"]):
    d.point((x, y), fill="#fff3c6")
    d.line((x - 2, y, x + 2, y), fill=color)
    d.line((x, y - 2, x, y + 2), fill=color)


def checker_floor(d, y, c1, c2):
    for yy in range(y, 144, 8):
        for xx in range(0, 256, 8):
            rect(d, (xx, yy, xx + 7, yy + 7), c1 if ((xx + yy) // 8) % 2 else c2)
    d.line((0, y, 255, y), fill=PAL["pink"], width=1)


def dithering(d, color="#1c1230"):
    for y in range(0, 144, 6):
        for x in range((y // 6) % 2 * 4, 256, 8):
            d.point((x, y), fill=color)


def moon(d, x=198, y=22):
    d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=PAL["gold"])
    d.ellipse((x - 6, y - 18, x + 17, y + 8), fill=PAL["ink"])
    for sx, sy in [(24, 18), (57, 31), (218, 51), (126, 17), (237, 29)]:
        star(d, sx, sy)


def draw_house(d, ox, oy, scale=1):
    rect(d, (ox + 8, oy + 36, ox + 92, oy + 96), PAL["plum"], PAL["pink"])
    rect(d, (ox + 26, oy + 15, ox + 74, oy + 43), "#1b102d", PAL["lav"])
    tri(d, [(ox, oy + 38), (ox + 50, oy + 4), (ox + 100, oy + 38)], PAL["void"], PAL["pink"])
    tri(d, [(ox + 18, oy + 17), (ox + 50, oy - 3), (ox + 82, oy + 17)], PAL["void"], PAL["pink"])
    for wx, wy in [(ox + 20, oy + 51), (ox + 63, oy + 51), (ox + 43, oy + 24)]:
        rect(d, (wx, wy, wx + 13, wy + 17), "#1a244d", PAL["pink"])
        rect(d, (wx + 3, wy + 3, wx + 10, wy + 14), PAL["amber"])
        d.line((wx + 6, wy + 3, wx + 6, wy + 14), fill=PAL["gold"])
    rect(d, (ox + 43, oy + 72, ox + 61, oy + 96), "#150d20", PAL["pink"])
    rect(d, (ox + 57, oy + 84, ox + 58, oy + 85), PAL["gold"])


def menu_background():
    im = img(256, 144)
    d = ImageDraw.Draw(im)
    for y in range(144):
        color = "#090714" if y < 52 else "#120a22" if y < 100 else "#1a1028"
        d.line((0, y, 255, y), fill=color)
    moon(d)
    for x in range(-8, 270, 20):
        d.line((x, 112, x + 6, 42), fill="#10091e", width=3)
        d.line((x + 5, 70, x - 8, 48), fill="#10091e", width=1)
        d.line((x + 5, 76, x + 19, 53), fill="#10091e", width=1)
    draw_house(d, 140, 38)
    d.line((0, 100, 255, 96), fill="#08060f", width=2)
    for x in range(0, 256, 12):
        rect(d, (x, 91, x + 2, 116), "#08060f")
        tri(d, [(x - 1, 91), (x + 1, 87), (x + 3, 91)], "#08060f")
    checker_floor(d, 116, "#24143a", "#171024")
    rect(d, (88, 101, 105, 119), "#3b214f", PAL["gold"])
    rect(d, (92, 97, 99, 101), PAL["pink"])
    dithering(d, "#24143a")
    im.save(BG / "menu_estate.png")


def bedroom():
    im = img(256, 144)
    d = ImageDraw.Draw(im)
    rect(d, (0, 0, 255, 86), "#1a102b")
    rect(d, (0, 0, 255, 14), "#0c0815")
    for x in range(0, 256, 16):
        rect(d, (x, 14, x + 7, 86), "#211338")
    rect(d, (176, 14, 222, 63), "#0f1026", PAL["pink"])
    for x in range(183, 217, 10):
        d.line((x, 18, x, 58), fill=PAL["lav"])
    d.line((176, 38, 222, 38), fill=PAL["lav"])
    rect(d, (20, 70, 83, 98), "#351b46", PAL["pink"])
    rect(d, (23, 62, 58, 78), "#4c2861", PAL["gold"])
    rect(d, (106, 79, 145, 106), "#382050", PAL["gold"])
    rect(d, (117, 70, 134, 81), PAL["pink"], PAL["gold"])
    checker_floor(d, 98, "#291640", "#181026")
    dithering(d)
    im.save(BG / "bedroom_deluxe.png")


def hallway():
    im = img(256, 144)
    d = ImageDraw.Draw(im)
    rect(d, (0, 0, 255, 94), "#120d22")
    for x in range(8, 256, 24):
        rect(d, (x, 20, x + 8, 93), "#201337", PAL["violet"])
    for x in [88, 177]:
        rect(d, (x, 54, x + 31, 103), "#110a1b", PAL["pink"])
        rect(d, (x + 7, 64, x + 24, 103), "#211132", PAL["lav"])
        rect(d, (x + 23, 83, x + 24, 84), PAL["gold"])
    rect(d, (128, 41, 153, 68), "#25143c", PAL["gold"])
    rect(d, (133, 46, 148, 63), "#0d0a19", PAL["pink"])
    checker_floor(d, 103, "#26143d", "#130d20")
    dithering(d)
    im.save(BG / "hallway_deluxe.png")


def library():
    im = img(256, 144)
    d = ImageDraw.Draw(im)
    rect(d, (0, 0, 255, 95), "#140c20")
    for shelf_x in [13, 168]:
        rect(d, (shelf_x, 21, shelf_x + 66, 90), "#231233", PAL["gold"])
        for y in [29, 47, 65]:
            d.line((shelf_x + 3, y, shelf_x + 63, y), fill=PAL["gold"])
            for x in range(shelf_x + 6, shelf_x + 60, 7):
                rect(d, (x, y - 14, x + 4, y - 1), ["#7b4bc4", "#d98248", "#f2a0d6"][(x + y) % 3])
    rect(d, (103, 75, 153, 101), "#321a42", PAL["gold"])
    rect(d, (111, 69, 145, 80), "#eee0ad", PAL["pink"])
    checker_floor(d, 101, "#281640", "#171024")
    dithering(d)
    im.save(BG / "library_deluxe.png")


def mirror_room():
    im = img(256, 144)
    d = ImageDraw.Draw(im)
    rect(d, (0, 0, 255, 99), "#100c22")
    for x in range(12, 250, 30):
        rect(d, (x, 22, x + 18, 80), "#1e1a3d", PAL["lav"])
        d.line((x + 3, 76, x + 16, 26), fill=PAL["pink"])
        d.line((x + 8, 78, x + 18, 42), fill=PAL["gold"])
    rect(d, (106, 23, 151, 94), "#12162f", PAL["gold"])
    rect(d, (113, 30, 144, 86), "#253970", PAL["pink"])
    d.line((117, 83, 140, 35), fill="#cbe7ff")
    d.line((125, 83, 145, 48), fill=PAL["lav"])
    checker_floor(d, 99, "#24143d", "#120d21")
    dithering(d)
    im.save(BG / "mirror_deluxe.png")


def garden():
    im = img(256, 144)
    d = ImageDraw.Draw(im)
    rect(d, (0, 0, 255, 144), "#080914")
    moon(d, 205, 24)
    for x in range(0, 256, 18):
        d.line((x, 106, x + 5, 40), fill="#101522", width=3)
        d.line((x + 4, 58, x - 7, 48), fill="#101522")
        d.line((x + 5, 66, x + 18, 52), fill="#101522")
    rect(d, (0, 105, 255, 143), "#111d21")
    for x in range(0, 256, 10):
        d.line((x, 120, x + 6, 107), fill="#264d3b")
        if x % 30 == 0:
            rect(d, (x + 4, 95, x + 8, 99), PAL["gold"])
    rect(d, (180, 88, 216, 119), "#17221f", PAL["mint"])
    for x in [184, 194, 204]:
        rect(d, (x, 78, x + 5, 92), PAL["gold"])
        rect(d, (x + 1, 80, x + 4, 91), PAL["pink"])
    dithering(d, "#1a2930")
    im.save(BG / "garden_deluxe.png")


def cemetery():
    im = img(256, 144)
    d = ImageDraw.Draw(im)
    rect(d, (0, 0, 255, 144), "#080713")
    moon(d, 205, 22)
    rect(d, (0, 102, 255, 143), "#15151f")
    for x in range(8, 256, 18):
        rect(d, (x, 71 + (x % 3) * 5, x + 9, 105), "#1c1a2b", PAL["fog"])
        d.arc((x, 63 + (x % 3) * 5, x + 9, 78 + (x % 3) * 5), 180, 360, fill=PAL["fog"])
    for x in range(0, 256, 32):
        rect(d, (x, 91, x + 2, 118), "#090714")
        tri(d, [(x - 2, 91), (x + 1, 86), (x + 4, 91)], "#090714")
    checker_floor(d, 112, "#1f1c2d", "#11101c")
    dithering(d, "#242139")
    im.save(BG / "cemetery_deluxe.png")


def party():
    im = img(256, 144)
    d = ImageDraw.Draw(im)
    rect(d, (0, 0, 255, 96), "#190b25")
    for x in range(0, 256, 20):
        tri(d, [(x, 20), (x + 10, 30), (x + 20, 20)], ["#ffd36b", "#f2a0d6", "#8d5bd4"][(x // 20) % 3])
    rect(d, (0, 28, 255, 31), PAL["gold"])
    for x in [34, 72, 182, 220]:
        rect(d, (x, 48, x + 18, 78), "#24143a", PAL["pink"])
        rect(d, (x + 4, 54, x + 14, 75), PAL["amber"])
    rect(d, (104, 70, 152, 99), "#321a42", PAL["gold"])
    rect(d, (114, 62, 142, 73), "#f0d7ac", PAL["pink"])
    checker_floor(d, 99, "#311848", "#181026")
    dithering(d)
    im.save(BG / "party_deluxe.png")


def transparent_object(name, size, draw_fn):
    im = img(size[0], size[1], transparent=True)
    d = ImageDraw.Draw(im)
    draw_fn(d)
    im.save(OBJ / name)


def objects():
    transparent_object("bed_big.png", (80, 42), lambda d: (
        rect(d, (2, 18, 76, 38), "#351b46", PAL["pink"]),
        rect(d, (6, 9, 43, 23), "#4c2861", PAL["gold"]),
        rect(d, (47, 14, 72, 26), "#7b4bc4", PAL["pink"]),
        rect(d, (0, 36, 78, 41), "#160d22"),
    ))
    transparent_object("haunted_painting.png", (38, 42), lambda d: (
        rect(d, (2, 3, 35, 39), PAL["gold"], "#3a224d"),
        rect(d, (6, 7, 31, 35), "#10162c", PAL["pink"]),
        rect(d, (14, 15, 17, 18), PAL["gold"]),
        rect(d, (23, 15, 26, 18), PAL["gold"]),
        d.line((13, 27, 27, 27), fill=PAL["pink"], width=1),
    ))
    transparent_object("open_spellbook.png", (64, 34), lambda d: (
        rect(d, (5, 12, 58, 30), "#51305f", PAL["gold"]),
        rect(d, (8, 6, 31, 25), "#eee0ad", PAL["pink"]),
        rect(d, (33, 6, 56, 25), "#eee0ad", PAL["pink"]),
        d.line((32, 8, 32, 27), fill="#7a5a72"),
        star(d, 45, 15),
        star(d, 19, 17, PAL["lav"]),
    ))
    transparent_object("mirror_full.png", (58, 84), lambda d: (
        rect(d, (8, 2, 49, 81), PAL["gold"], "#3a224d"),
        rect(d, (14, 8, 43, 72), "#24386e", PAL["pink"]),
        d.line((18, 69, 39, 16), fill="#bfe7ff", width=1),
        d.line((27, 70, 44, 33), fill=PAL["lav"], width=1),
    ))
    transparent_object("moon_flowers.png", (58, 48), lambda d: (
        rect(d, (3, 35, 54, 46), "#17221f", PAL["mint"]),
        *[(
            d.line((x + 4, 36, x + 4, 17), fill=PAL["mint"], width=1),
            rect(d, (x, 10, x + 9, 19), PAL["gold"], PAL["pink"]),
            rect(d, (x + 3, 13, x + 6, 16), "#fff3c6"),
        ) for x in (8, 23, 38)]
    ))
    transparent_object("final_table.png", (72, 46), lambda d: (
        rect(d, (8, 15, 64, 31), "#4c2861", PAL["gold"]),
        rect(d, (14, 7, 58, 17), "#f0d7ac", PAL["pink"]),
        rect(d, (14, 31, 21, 44), "#24143a"),
        rect(d, (51, 31, 58, 44), "#24143a"),
        star(d, 36, 12),
    ))
    transparent_object("gothic_door.png", (38, 68), lambda d: (
        rect(d, (4, 14, 33, 66), "#120a1b", PAL["pink"]),
        d.arc((4, 0, 33, 28), 180, 360, fill=PAL["pink"]),
        rect(d, (11, 24, 26, 66), "#231132", PAL["lav"]),
        rect(d, (27, 43, 29, 45), PAL["gold"]),
    ))


def main():
    ensure_dirs()
    menu_background()
    bedroom()
    hallway()
    library()
    mirror_room()
    garden()
    cemetery()
    party()
    objects()
    print(f"Generated assets in {OUT}")


if __name__ == "__main__":
    main()
