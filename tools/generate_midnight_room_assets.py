from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import random
import uuid


ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "Assets" / "Images"
MR = IMAGES / "MidnightRoom"

PALETTE = {
    "lavender": "#c8a7ff",
    "deep_purple": "#24142f",
    "dusty_pink": "#e8a7bd",
    "soft_black": "#17131d",
    "autumn_orange": "#f28c45",
    "cream": "#fff3dc",
    "mint": "#9fd8bd",
    "moon": "#f7df8a",
    "shadow": "#3a2547",
    "plum": "#6d3c7d",
}


def ensure_dirs():
    for path in [
        MR,
        MR / "Character",
        MR / "Collectibles",
        MR / "Backgrounds",
        MR / "Tilesets",
        MR / "UI",
        MR / "RoomProgress",
        MR / "Props",
        MR / "Concept",
    ]:
        path.mkdir(parents=True, exist_ok=True)
        write_meta(path, folder=True)


def write_meta(path, folder=False):
    meta = Path(str(path) + ".meta")
    if meta.exists():
        return
    guid = uuid.uuid4().hex
    if folder:
        meta.write_text(
            "fileFormatVersion: 2\n"
            f"guid: {guid}\n"
            "folderAsset: yes\n"
            "DefaultImporter:\n"
            "  externalObjects: {}\n"
            "  userData: \n"
            "  assetBundleName: \n"
            "  assetBundleVariant: \n",
            encoding="utf-8",
        )
    else:
        meta.write_text(
            "fileFormatVersion: 2\n"
            f"guid: {guid}\n"
            "TextureImporter:\n"
            "  internalIDToNameTable: []\n"
            "  externalObjects: {}\n"
            "  serializedVersion: 12\n"
            "  mipmaps:\n"
            "    mipMapMode: 0\n"
            "    enableMipMap: 0\n"
            "    sRGBTexture: 1\n"
            "  textureSettings:\n"
            "    serializedVersion: 2\n"
            "    filterMode: 0\n"
            "    aniso: 1\n"
            "    mipBias: 0\n"
            "    wrapU: 1\n"
            "    wrapV: 1\n"
            "    wrapW: 1\n"
            "  nPOTScale: 0\n"
            "  spriteMode: 1\n"
            "  spritePixelsToUnits: 100\n"
            "  alphaUsage: 1\n"
            "  alphaIsTransparency: 1\n"
            "  textureType: 8\n"
            "  spriteSheet:\n"
            "    serializedVersion: 2\n"
            "    sprites: []\n"
            "    outline: []\n"
            "    physicsShape: []\n"
            "  userData: \n"
            "  assetBundleName: \n"
            "  assetBundleVariant: \n",
            encoding="utf-8",
        )


def save(img, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.stem}.{uuid.uuid4().hex}.tmp{path.suffix}")
    img.save(tmp)
    tmp.replace(path)
    write_meta(path)


def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/seguisb.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def rgba(hex_color, alpha=255):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def rr(draw, box, fill, outline=None, width=1, radius=14):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def ellipse(draw, box, fill, outline=None, width=1):
    draw.ellipse(box, fill=fill, outline=outline, width=width)


def polygon(draw, points, fill, outline=None):
    draw.polygon(points, fill=fill)
    if outline:
        draw.line(points + [points[0]], fill=outline, width=3, joint="curve")


def add_noise(img, amount=900, alpha=24):
    px = img.load()
    w, h = img.size
    random.seed(12)
    for _ in range(amount):
        x = random.randrange(w)
        y = random.randrange(h)
        r, g, b, a = px[x, y]
        delta = random.randrange(-10, 11)
        px[x, y] = (max(0, min(255, r + delta)), max(0, min(255, g + delta)), max(0, min(255, b + delta)), min(255, a + alpha))


def draw_star(d, cx, cy, r, color):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + math.cos(ang) * rad, cy + math.sin(ang) * rad))
    polygon(d, pts, color)


def draw_character(d, ox, oy, scale=1.0, pose="idle", side=False, expression="happy"):
    s = scale
    ink = rgba(PALETTE["soft_black"])
    skin = (255, 205, 190, 255)
    blush = rgba(PALETTE["dusty_pink"], 180)
    hair = (33, 28, 41, 255)
    coat = rgba(PALETTE["deep_purple"])
    skirt = rgba(PALETTE["plum"])
    boot = rgba(PALETTE["soft_black"])
    scarf = rgba(PALETTE["autumn_orange"])
    sock = rgba(PALETTE["lavender"])
    bob = 0 if pose == "idle" else (-4 if pose == "jump" else 5 if pose == "fall" else 2)
    leg_shift = 0 if pose in ["idle", "jump", "fall"] else 8
    arm_shift = -10 if pose == "jump" else 7 if pose == "fall" else 0
    x, y = ox, oy + bob

    # legs and boots
    d.rounded_rectangle((x + 42 * s, y + 126 * s, x + 55 * s, y + 176 * s), radius=int(5 * s), fill=sock)
    d.rounded_rectangle((x + 76 * s, y + 126 * s, x + 89 * s, y + 176 * s), radius=int(5 * s), fill=sock)
    d.rounded_rectangle((x + (36 - leg_shift) * s, y + 166 * s, x + 61 * s, y + 184 * s), radius=int(8 * s), fill=boot)
    d.rounded_rectangle((x + (70 + leg_shift) * s, y + 166 * s, x + 96 * s, y + 184 * s), radius=int(8 * s), fill=boot)

    # skirt and coat
    polygon(d, [(x + 35 * s, y + 96 * s), (x + 97 * s, y + 96 * s), (x + 108 * s, y + 142 * s), (x + 26 * s, y + 142 * s)], skirt, ink)
    rr(d, (x + 31 * s, y + 72 * s, x + 103 * s, y + 128 * s), coat, ink, 3, int(16 * s))
    d.line((x + 67 * s, y + 75 * s, x + 67 * s, y + 128 * s), fill=rgba(PALETTE["lavender"]), width=max(2, int(2 * s)))
    rr(d, (x + 46 * s, y + 82 * s, x + 88 * s, y + 103 * s), scarf, None, 1, int(10 * s))

    # arms
    d.rounded_rectangle((x + 17 * s, y + (80 + arm_shift) * s, x + 38 * s, y + 126 * s), radius=int(9 * s), fill=coat, outline=ink, width=max(2, int(2 * s)))
    d.rounded_rectangle((x + 94 * s, y + (80 - arm_shift) * s, x + 115 * s, y + 126 * s), radius=int(9 * s), fill=coat, outline=ink, width=max(2, int(2 * s)))

    # head and hair
    ellipse(d, (x + 30 * s, y + 13 * s, x + 105 * s, y + 92 * s), hair, ink, max(2, int(2 * s)))
    ellipse(d, (x + 39 * s, y + 30 * s, x + 98 * s, y + 91 * s), skin, ink, max(2, int(2 * s)))
    d.pieslice((x + 28 * s, y + 7 * s, x + 108 * s, y + 76 * s), 180, 360, fill=hair)
    for bx in [40, 52, 64, 76, 88]:
        polygon(d, [(x + bx * s, y + 28 * s), (x + (bx + 9) * s, y + 28 * s), (x + (bx + 3) * s, y + 53 * s)], hair)
    ellipse(d, (x + 46 * s, y + 53 * s, x + 55 * s, y + 64 * s), ink)
    ellipse(d, (x + 80 * s, y + 53 * s, x + 89 * s, y + 64 * s), ink)
    ellipse(d, (x + 49 * s, y + 55 * s, x + 52 * s, y + 58 * s), (255, 255, 255, 230))
    ellipse(d, (x + 83 * s, y + 55 * s, x + 86 * s, y + 58 * s), (255, 255, 255, 230))
    if expression == "surprised":
        ellipse(d, (x + 64 * s, y + 69 * s, x + 73 * s, y + 78 * s), ink)
    elif expression == "focused":
        d.line((x + 61 * s, y + 72 * s, x + 75 * s, y + 70 * s), fill=ink, width=max(2, int(2 * s)))
    else:
        d.arc((x + 58 * s, y + 62 * s, x + 80 * s, y + 79 * s), 20, 160, fill=ink, width=max(2, int(2 * s)))
    ellipse(d, (x + 36 * s, y + 65 * s, x + 49 * s, y + 76 * s), blush)
    ellipse(d, (x + 86 * s, y + 65 * s, x + 99 * s, y + 76 * s), blush)
    draw_star(d, x + 101 * s, y + 23 * s, 8 * s, rgba(PALETTE["moon"]))


def transparent(size):
    return Image.new("RGBA", size, (0, 0, 0, 0))


def character_assets():
    img = transparent((530, 768))
    d = ImageDraw.Draw(img)
    draw_character(d, 95, 108, 2.6, "idle")
    d.text((42, 30), "Mara Noctua", fill=rgba(PALETTE["deep_purple"]), font=font(44, True))
    d.text((42, 84), "Midnight Room protagonist", fill=rgba(PALETTE["plum"]), font=font(24))
    save(img, IMAGES / "Hanna.png")
    save(img, MR / "Character" / "mara_front_concept.png")

    side = transparent((530, 768))
    d = ImageDraw.Draw(side)
    draw_character(d, 105, 110, 2.55, "walk", side=True, expression="focused")
    d.text((42, 30), "Side silhouette", fill=rgba(PALETTE["deep_purple"]), font=font(42, True))
    save(side, MR / "Character" / "mara_side_concept.png")

    exp = transparent((1024, 512))
    d = ImageDraw.Draw(exp)
    for i, e in enumerate(["happy", "focused", "surprised", "happy"]):
        draw_character(d, 45 + i * 245, 80, 1.35, "idle", expression=e)
        d.text((65 + i * 245, 24), ["soft smile", "focused", "spark", "cozy"][i], fill=rgba(PALETTE["deep_purple"]), font=font(22, True))
    save(exp, MR / "Character" / "mara_expressions.png")

    sheet = transparent((1024, 512))
    d = ImageDraw.Draw(sheet)
    frames = [("idle", "idle"), ("walk", "walk 1"), ("walk", "walk 2"), ("jump", "jump"), ("fall", "fall")]
    for i, (pose, label) in enumerate(frames):
        draw_character(d, 20 + i * 200, 74, 1.05, pose)
        d.text((58 + i * 200, 24), label, fill=rgba(PALETTE["deep_purple"]), font=font(20, True))
        d.rectangle((10 + i * 200, 58, 178 + i * 200, 292), outline=rgba(PALETTE["lavender"], 120), width=2)
    save(sheet, MR / "Character" / "mara_sprite_sheet_idle_walk_jump_fall.png")


def item_icon(kind, label, size=(256, 256)):
    img = transparent(size)
    d = ImageDraw.Draw(img)
    w, h = size
    cx, cy = w // 2, h // 2
    shadow = rgba(PALETTE["deep_purple"], 45)
    ellipse(d, (48, 188, 208, 220), shadow)
    if kind == "lipstick":
        rr(d, (95, 72, 152, 186), rgba(PALETTE["soft_black"]), rgba(PALETTE["deep_purple"]), 4, 18)
        rr(d, (108, 42, 139, 92), rgba(PALETTE["dusty_pink"]), rgba(PALETTE["deep_purple"]), 4, 11)
        d.rectangle((101, 130, 146, 142), fill=rgba(PALETTE["lavender"]))
    elif kind == "liner":
        d.line((70, 172, 176, 66), fill=rgba(PALETTE["deep_purple"]), width=22)
        d.line((82, 180, 184, 78), fill=(117, 75, 53, 255), width=10)
        polygon(d, [(174, 58), (202, 32), (188, 74)], rgba(PALETTE["soft_black"]), rgba(PALETTE["deep_purple"]))
    elif kind == "candle":
        rr(d, (73, 92, 183, 195), rgba(PALETTE["cream"]), rgba(PALETTE["deep_purple"]), 4, 22)
        ellipse(d, (76, 78, 180, 116), rgba(PALETTE["dusty_pink"]), rgba(PALETTE["deep_purple"]), 4)
        polygon(d, [(128, 42), (145, 76), (128, 91), (111, 76)], rgba(PALETTE["autumn_orange"]), rgba(PALETTE["deep_purple"]))
    elif kind == "plush":
        ellipse(d, (54, 72, 206, 196), rgba(PALETTE["lavender"]), rgba(PALETTE["deep_purple"]), 4)
        ellipse(d, (45, 60, 86, 104), rgba(PALETTE["lavender"]), rgba(PALETTE["deep_purple"]), 4)
        ellipse(d, (170, 60, 211, 104), rgba(PALETTE["lavender"]), rgba(PALETTE["deep_purple"]), 4)
        ellipse(d, (92, 119, 105, 133), rgba(PALETTE["soft_black"]))
        ellipse(d, (154, 119, 167, 133), rgba(PALETTE["soft_black"]))
        d.arc((110, 135, 158, 164), 20, 160, fill=rgba(PALETTE["soft_black"]), width=4)
    elif kind == "moonlamp":
        ellipse(d, (65, 42, 190, 167), rgba(PALETTE["moon"]), rgba(PALETTE["deep_purple"]), 4)
        ellipse(d, (104, 30, 202, 152), (0, 0, 0, 0))
        rr(d, (81, 174, 176, 194), rgba(PALETTE["soft_black"]), None, 1, 8)
    elif kind == "poster":
        rr(d, (63, 43, 193, 200), rgba(PALETTE["dusty_pink"]), rgba(PALETTE["deep_purple"]), 5, 10)
        draw_star(d, 130, 105, 38, rgba(PALETTE["moon"]))
        d.rectangle((82, 155, 174, 166), fill=rgba(PALETTE["deep_purple"]))
    elif kind == "vinyl":
        ellipse(d, (53, 46, 203, 196), rgba(PALETTE["soft_black"]), rgba(PALETTE["deep_purple"]), 5)
        ellipse(d, (94, 87, 162, 155), rgba(PALETTE["dusty_pink"]), rgba(PALETTE["deep_purple"]), 4)
        ellipse(d, (119, 112, 137, 130), rgba(PALETTE["cream"]))
    elif kind == "plant":
        rr(d, (88, 135, 168, 205), rgba(PALETTE["autumn_orange"]), rgba(PALETTE["deep_purple"]), 4, 14)
        for ang in [-70, -35, 0, 35, 70]:
            x = cx + math.cos(math.radians(ang)) * 50
            y = 118 + math.sin(math.radians(ang)) * 25
            ellipse(d, (x - 24, y - 36, x + 24, y + 18), rgba(PALETTE["mint"]), rgba(PALETTE["deep_purple"]), 3)
    elif kind == "mirror":
        rr(d, (72, 36, 184, 190), rgba(PALETTE["cream"]), rgba(PALETTE["deep_purple"]), 5, 48)
        rr(d, (91, 58, 165, 166), rgba(PALETTE["lavender"], 150), None, 1, 33)
        d.line((104, 84, 146, 58), fill=(255, 255, 255, 170), width=5)
    elif kind == "stickers":
        for x, y, c in [(78, 76, "lavender"), (137, 65, "dusty_pink"), (165, 134, "moon"), (90, 150, "mint")]:
            draw_star(d, x, y, 28, rgba(PALETTE[c]))
    elif kind == "accessory":
        d.arc((75, 76, 183, 178), 180, 360, fill=rgba(PALETTE["deep_purple"]), width=12)
        ellipse(d, (61, 121, 93, 166), rgba(PALETTE["lavender"]), rgba(PALETTE["deep_purple"]), 4)
        ellipse(d, (165, 121, 197, 166), rgba(PALETTE["lavender"]), rgba(PALETTE["deep_purple"]), 4)
    d.text((w // 2, h - 28), label, anchor="mm", fill=rgba(PALETTE["deep_purple"]), font=font(16, True))
    return img


def collectibles():
    items = [
        ("lipstick", "Labial"),
        ("liner", "Delineador"),
        ("candle", "Vela"),
        ("plush", "Peluche"),
        ("moonlamp", "Luna"),
        ("poster", "Poster"),
        ("vinyl", "Vinilo"),
        ("plant", "Planta"),
        ("mirror", "Espejo"),
        ("stickers", "Stickers"),
        ("accessory", "Audifonos"),
    ]
    for kind, label in items:
        save(item_icon(kind, label), MR / "Collectibles" / f"{kind}.png")
    save(item_icon("lipstick", "Hallazgo", (174, 157)), IMAGES / "Diamante.png")
    atlas = transparent((1024, 768))
    d = ImageDraw.Draw(atlas)
    d.text((40, 24), "Midnight Room collectible set", fill=rgba(PALETTE["deep_purple"]), font=font(36, True))
    for idx, (kind, label) in enumerate(items):
        icon = item_icon(kind, label, (160, 160))
        atlas.alpha_composite(icon, (36 + (idx % 5) * 190, 95 + (idx // 5) * 230))
    save(atlas, MR / "Collectibles" / "collectibles_atlas.png")


def background(name, index, mood):
    img = Image.new("RGBA", (1024, 1024), rgba(PALETTE["deep_purple"]))
    d = ImageDraw.Draw(img)
    top = rgba(["#21152c", "#1b162a", "#2a1835", "#27142b", "#201827"][index - 1])
    bottom = rgba(["#6d3c7d", "#48335d", "#8f4d55", "#4a2f58", "#17131d"][index - 1])
    for y in range(1024):
        t = y / 1023
        col = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(4))
        d.line((0, y, 1024, y), fill=col)
    ellipse(d, (720, 80, 895, 255), rgba(PALETTE["moon"], 210))
    ellipse(d, (775, 55, 920, 240), top)
    for _ in range(65):
        x = random.randrange(0, 1024)
        y = random.randrange(40, 420)
        draw_star(d, x, y, random.randrange(3, 8), rgba(PALETTE["cream"], random.randrange(90, 180)))
    if index == 1:
        for x in range(-80, 1100, 120):
            trunk = rgba("#39252f")
            d.rectangle((x + 45, 470, x + 70, 900), fill=trunk)
            for dx, dy, c in [(-20, 400, "autumn_orange"), (32, 365, "dusty_pink"), (65, 415, "lavender")]:
                ellipse(d, (x + dx, dy, x + dx + 125, dy + 125), rgba(PALETTE[c], 230))
        d.rectangle((0, 825, 1024, 1024), fill=rgba("#3c2235"))
    elif index == 2:
        d.rectangle((0, 700, 1024, 1024), fill=rgba("#201521"))
        for x in range(50, 980, 180):
            d.rectangle((x, 360, x + 90, 700), fill=rgba("#34243f"))
            for wy in range(390, 650, 58):
                rr(d, (x + 18, wy, x + 70, wy + 28), rgba(PALETTE["moon"], 160), None, 1, 5)
            d.line((x + 45, 700, x + 45, 560), fill=rgba(PALETTE["soft_black"]), width=7)
            ellipse(d, (x + 23, 535, x + 67, 580), rgba(PALETTE["autumn_orange"], 210))
    elif index == 3:
        rr(d, (120, 260, 904, 830), rgba("#3b263f"), rgba(PALETTE["lavender"], 180), 5, 25)
        rr(d, (170, 335, 420, 760), rgba("#251729"), rgba(PALETTE["dusty_pink"]), 4, 14)
        rr(d, (520, 335, 820, 760), rgba("#251729"), rgba(PALETTE["dusty_pink"]), 4, 14)
        d.text((512, 285), "MOON & THREAD", anchor="mm", fill=rgba(PALETTE["moon"]), font=font(38, True))
        d.rectangle((0, 820, 1024, 1024), fill=rgba("#251a2f"))
    elif index == 4:
        d.rectangle((0, 735, 1024, 1024), fill=rgba("#2c1b28"))
        for x in range(40, 960, 210):
            polygon(d, [(x, 520), (x + 95, 430), (x + 190, 520)], rgba(PALETTE["autumn_orange"]), rgba(PALETTE["deep_purple"]))
            rr(d, (x + 20, 520, x + 170, 760), rgba("#3a2440"), rgba(PALETTE["lavender"]), 4, 10)
            d.rectangle((x + 43, 607, x + 147, 625), fill=rgba(PALETTE["moon"]))
    elif index == 5:
        d.rectangle((0, 500, 1024, 1024), fill=rgba("#34243f"))
        rr(d, (120, 205, 880, 800), rgba("#493051"), rgba(PALETTE["lavender"], 150), 4, 30)
        rr(d, (210, 470, 520, 720), rgba("#2a1d2e"), rgba(PALETTE["dusty_pink"]), 4, 18)
        rr(d, (590, 310, 775, 645), rgba("#2a1d2e"), rgba(PALETTE["moon"]), 4, 18)
        ellipse(d, (675, 365, 735, 425), rgba(PALETTE["moon"]))
    add_noise(img, 1500, 8)
    d.text((40, 930), mood, fill=rgba(PALETTE["cream"], 190), font=font(30, True))
    return img


def backgrounds():
    names = [
        ("Fondo.png", "Bosque de otono"),
        ("Fondo2.png", "Calle nocturna"),
        ("Fondo3.png", "Tienda vintage"),
        ("Fondo4.png", "Mercado Halloween"),
        ("Fondo5.png", "Habitacion cozy"),
    ]
    for i, (filename, mood) in enumerate(names, start=1):
        img = background(filename, i, mood)
        save(img, IMAGES / "Fondos" / filename)
        save(img, MR / "Backgrounds" / filename)
    save(background("rooftop", 2, "Azotea bajo la luna"), MR / "Backgrounds" / "rooftop_moon.png")


def tile(fill, trim, pattern="leaves", size=(3464, 3464)):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    w, h = size
    margin = max(24, int(w * 0.038))
    top = max(60, int(h * 0.24))
    bottom = max(top + 120, int(h * 0.82))
    lip = min(bottom, top + max(42, int(h * 0.085)))
    stroke = max(3, int(w * 0.006))
    radius = max(14, int(w * 0.02))
    rr(d, (margin, top, w - margin, bottom), rgba(fill), rgba(PALETTE["deep_purple"]), stroke, radius)
    d.rectangle((margin, top, w - margin, lip), fill=rgba(trim))
    step = max(92, int(w * 0.08))
    motif = max(26, int(w * 0.018))
    for x in range(margin + step // 2, w - margin - step // 2, step):
        if pattern == "leaves":
            ellipse(d, (x, top + motif, x + motif * 2, top + motif * 2), rgba(PALETTE["autumn_orange"], 180), rgba(PALETTE["deep_purple"], 150), max(2, stroke // 2))
        elif pattern == "stars":
            draw_star(d, x + motif, top + motif * 1.6, motif, rgba(PALETTE["moon"], 190))
        else:
            rr(d, (x, top + motif, x + motif * 2, top + motif * 2.4), rgba(PALETTE["lavender"], 170), None, 1, max(5, motif // 3))
    return img


def tiles():
    save(tile("#493051", PALETTE["dusty_pink"], "leaves"), IMAGES / "Piso.png")
    save(tile("#382446", PALETTE["lavender"], "stars"), IMAGES / "Gran piso.png")
    save(tile("#2a1d2e", PALETTE["autumn_orange"], "bricks"), IMAGES / "Torre piso.png")
    save(tile("#493051", PALETTE["dusty_pink"], "leaves", (1024, 512)), MR / "Tilesets" / "autumn_platform.png")
    save(tile("#382446", PALETTE["lavender"], "stars", (1024, 512)), MR / "Tilesets" / "moon_platform.png")
    save(tile("#2a1d2e", PALETTE["autumn_orange"], "bricks", (1024, 512)), MR / "Tilesets" / "vintage_platform.png")


def simple_icon(kind):
    img = transparent((512, 512))
    d = ImageDraw.Draw(img)
    rr(d, (82, 82, 430, 430), rgba(PALETTE["deep_purple"]), rgba(PALETTE["lavender"]), 10, 80)
    if kind == "clock":
        ellipse(d, (150, 130, 362, 342), rgba(PALETTE["cream"]), rgba(PALETTE["deep_purple"]), 8)
        d.line((256, 236, 256, 165), fill=rgba(PALETTE["deep_purple"]), width=14)
        d.line((256, 236, 310, 270), fill=rgba(PALETTE["deep_purple"]), width=14)
    elif kind == "attempt":
        draw_star(d, 256, 236, 120, rgba(PALETTE["autumn_orange"]))
        d.text((256, 235), "!", anchor="mm", fill=rgba(PALETTE["deep_purple"]), font=font(150, True))
    elif kind == "goal":
        draw_star(d, 256, 235, 125, rgba(PALETTE["moon"]))
        rr(d, (190, 300, 322, 342), rgba(PALETTE["dusty_pink"]), None, 1, 18)
    return img


def ui_assets():
    save(simple_icon("clock"), IMAGES / "Reloj.png")
    save(simple_icon("attempt"), IMAGES / "Intento.png")
    save(simple_icon("goal"), IMAGES / "Estrella.png")
    save(item_icon("plush", "Enemigo", (3464, 3464)), IMAGES / "Espantapajaros.png")
    save(item_icon("moonlamp", "", (55, 50)), IMAGES / "Jinete.png")

    screens = [
        ("main_menu", "Midnight Room", "Explora el otono, encuentra tesoros y decora tu refugio."),
        ("pause_menu", "Pausa", "Continuar  |  Coleccion  |  Habitacion"),
        ("victory", "Habitacion actualizada", "Nuevos objetos desbloqueados para decorar."),
        ("collection", "Coleccion", "Objetos encontrados, faltantes y recompensas."),
        ("room", "Mi habitacion", "Vista de progreso personalizable."),
    ]
    for name, title, subtitle in screens:
        img = Image.new("RGBA", (1280, 720), rgba(PALETTE["deep_purple"]))
        d = ImageDraw.Draw(img)
        for y in range(720):
            t = y / 719
            col = (
                int(36 * (1 - t) + 86 * t),
                int(20 * (1 - t) + 48 * t),
                int(47 * (1 - t) + 85 * t),
                255,
            )
            d.line((0, y, 1280, y), fill=col)
        ellipse(d, (915, 72, 1128, 285), rgba(PALETTE["moon"], 220))
        rr(d, (78, 76, 1180, 640), rgba("#fff3dc", 34), rgba(PALETTE["lavender"], 170), 4, 28)
        d.text((138, 130), title, fill=rgba(PALETTE["cream"]), font=font(68, True))
        d.text((142, 220), subtitle, fill=rgba(PALETTE["dusty_pink"]), font=font(28))
        for i, label in enumerate(["Jugar", "Coleccion", "Habitacion"]):
            rr(d, (140, 320 + i * 78, 452, 374 + i * 78), rgba(PALETTE["soft_black"], 210), rgba(PALETTE["lavender"]), 3, 18)
            d.text((172, 331 + i * 78), label, fill=rgba(PALETTE["cream"]), font=font(26, True))
        for i, kind in enumerate(["lipstick", "candle", "plush", "moonlamp", "plant"]):
            icon = item_icon(kind, "", (112, 112))
            img.alpha_composite(icon, (710 + (i % 3) * 135, 315 + (i // 3) * 130))
        save(img, MR / "UI" / f"{name}_mockup.png")

    hud = transparent((1024, 256))
    d = ImageDraw.Draw(hud)
    for i, (kind, text) in enumerate([("lipstick", "08/15"), ("clock", "42s"), ("attempt", "02"), ("goal", "75%")]):
        rr(d, (30 + i * 245, 58, 235 + i * 245, 154), rgba(PALETTE["soft_black"], 220), rgba(PALETTE["lavender"]), 3, 24)
        if kind in ["clock", "attempt", "goal"]:
            icon = simple_icon(kind).resize((62, 62))
        else:
            icon = item_icon(kind, "", (62, 62))
        hud.alpha_composite(icon, (48 + i * 245, 74))
        d.text((125 + i * 245, 85), text, fill=rgba(PALETTE["cream"]), font=font(30, True))
    save(hud, MR / "UI" / "hud_progress_indicators.png")


def room_progress():
    for stage in range(6):
        img = Image.new("RGBA", (1024, 768), rgba("#2a1d2e"))
        d = ImageDraw.Draw(img)
        d.rectangle((0, 450, 1024, 768), fill=rgba("#493051"))
        rr(d, (80, 120, 944, 620), rgba("#3b263f"), rgba(PALETTE["lavender"], 140), 4, 28)
        rr(d, (120, 380, 430, 585), rgba("#24142f"), rgba(PALETTE["dusty_pink"]), 4, 16)
        rr(d, (600, 230, 805, 565), rgba("#24142f"), rgba(PALETTE["moon"]), 4, 20)
        if stage >= 1:
            img.alpha_composite(item_icon("poster", "", (128, 128)), (470, 200))
        if stage >= 2:
            img.alpha_composite(item_icon("moonlamp", "", (128, 128)), (660, 308))
        if stage >= 3:
            img.alpha_composite(item_icon("plant", "", (128, 128)), (245, 390))
        if stage >= 4:
            img.alpha_composite(item_icon("plush", "", (128, 128)), (325, 410))
        if stage >= 5:
            img.alpha_composite(item_icon("vinyl", "", (128, 128)), (500, 390))
            img.alpha_composite(item_icon("stickers", "", (128, 128)), (710, 155))
        d.text((70, 42), f"Habitacion - progreso {stage * 20}%", fill=rgba(PALETTE["cream"]), font=font(38, True))
        save(img, MR / "RoomProgress" / f"room_progress_{stage:02d}.png")


def props():
    props_list = [
        ("lamp", "moonlamp"),
        ("poster_alt", "poster"),
        ("vinyl_player", "vinyl"),
        ("plant_pot", "plant"),
        ("mirror_vintage", "mirror"),
        ("sticker_pack", "stickers"),
    ]
    for filename, kind in props_list:
        save(item_icon(kind, "", (256, 256)), MR / "Props" / f"{filename}.png")


def concept_board():
    img = Image.new("RGBA", (1600, 1000), rgba(PALETTE["cream"]))
    d = ImageDraw.Draw(img)
    d.text((60, 50), "Midnight Room - Art Direction Board", fill=rgba(PALETTE["deep_purple"]), font=font(54, True))
    d.text((62, 115), "Cozy spooky cute + pastel goth + autumn room collecting", fill=rgba(PALETTE["plum"]), font=font(28))
    x = 62
    for name, col in PALETTE.items():
        rr(d, (x, 170, x + 120, 250), rgba(col), rgba(PALETTE["deep_purple"]), 2, 14)
        d.text((x, 260), name.replace("_", " "), fill=rgba(PALETTE["deep_purple"]), font=font(15, True))
        x += 140
    mara = Image.open(IMAGES / "Hanna.png").resize((276, 400))
    img.alpha_composite(mara, (70, 360))
    atlas = Image.open(MR / "Collectibles" / "collectibles_atlas.png").resize((640, 480))
    img.alpha_composite(atlas, (430, 330))
    room = Image.open(MR / "RoomProgress" / "room_progress_05.png").resize((450, 338))
    img.alpha_composite(room, (1110, 390))
    save(img, MR / "Concept" / "midnight_room_art_direction_board.png")


def main():
    random.seed(7)
    ensure_dirs()
    character_assets()
    collectibles()
    backgrounds()
    tiles()
    ui_assets()
    room_progress()
    props()
    concept_board()
    print("Midnight Room assets generated.")


if __name__ == "__main__":
    main()
