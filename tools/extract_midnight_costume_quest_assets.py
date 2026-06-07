from collections import deque
from pathlib import Path
import math
import shutil
import uuid

from PIL import Image, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
REF = Path(r"c:\Users\Softm\Downloads\ChatGPT Image 6 jun 2026, 16_32_05.png")
IMAGES = ROOT / "Assets" / "Images"
MCQ = IMAGES / "MidnightCostumeQuest"


def write_meta(path: Path, folder: bool = False) -> None:
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
        return

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
        "    filterMode: 1\n"
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


def ensure_dirs() -> None:
    for folder in [
        MCQ,
        MCQ / "Character",
        MCQ / "Collectibles",
        MCQ / "Backgrounds",
        MCQ / "Enemies",
        MCQ / "Tilesets",
        MCQ / "HUD",
        MCQ / "Concept",
    ]:
        folder.mkdir(parents=True, exist_ok=True)
        write_meta(folder, folder=True)


def save(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)
    write_meta(path)


def crop(src: Image.Image, box) -> Image.Image:
    return src.crop(tuple(int(v) for v in box)).convert("RGBA")


def color_distance(a, b) -> float:
    return math.sqrt(sum((int(a[i]) - int(b[i])) ** 2 for i in range(3)))


def clean_foreground_components(img: Image.Image, min_fraction: float = 0.16, max_components: int = 6) -> Image.Image:
    alpha = img.getchannel("A")
    w, h = img.size
    a = alpha.load()
    visited = bytearray(w * h)
    components = []

    for sy in range(h):
        for sx in range(w):
            idx = sy * w + sx
            if visited[idx] or a[sx, sy] == 0:
                continue
            q = deque([(sx, sy)])
            visited[idx] = 1
            pixels = []
            while q:
                x, y = q.popleft()
                pixels.append((x, y))
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if nx < 0 or nx >= w or ny < 0 or ny >= h:
                        continue
                    nidx = ny * w + nx
                    if not visited[nidx] and a[nx, ny] > 0:
                        visited[nidx] = 1
                        q.append((nx, ny))
            components.append(pixels)

    if not components:
        return img

    components.sort(key=len, reverse=True)
    largest = len(components[0])
    keep = set()
    for pixels in components[:max_components]:
        if len(pixels) >= largest * min_fraction:
            keep.update(pixels)

    out = img.copy()
    pix = out.load()
    for y in range(h):
        for x in range(w):
            if (x, y) not in keep:
                pix[x, y] = (0, 0, 0, 0)
    return out


def edge_cutout(img: Image.Image, tolerance: int = 34, min_fraction: float = 0.16) -> Image.Image:
    src = img.convert("RGBA")
    w, h = src.size
    pix = src.load()
    bg = bytearray(w * h)
    q = deque()

    def add_seed(x: int, y: int) -> None:
        idx = y * w + x
        if not bg[idx]:
            bg[idx] = 1
            q.append((x, y))

    for x in range(w):
        add_seed(x, 0)
        add_seed(x, h - 1)
    for y in range(h):
        add_seed(0, y)
        add_seed(w - 1, y)

    while q:
        x, y = q.popleft()
        current = pix[x, y]
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if nx < 0 or nx >= w or ny < 0 or ny >= h:
                continue
            idx = ny * w + nx
            if bg[idx]:
                continue
            neighbor = pix[nx, ny]
            if color_distance(current, neighbor) <= tolerance:
                bg[idx] = 1
                q.append((nx, ny))

    out = src.copy()
    out_pix = out.load()
    for y in range(h):
        for x in range(w):
            if bg[y * w + x]:
                out_pix[x, y] = (0, 0, 0, 0)

    alpha = out.getchannel("A")
    bbox = alpha.getbbox()
    if bbox:
        out = out.crop(bbox)
    out = clean_foreground_components(out, min_fraction=min_fraction)
    alpha = out.getchannel("A")
    bbox = alpha.getbbox()
    if bbox:
        out = out.crop(bbox)
    return out


def fit_on_canvas(img: Image.Image, size, fill_ratio=0.86, y_bias=0.5) -> Image.Image:
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    max_w = int(size[0] * fill_ratio)
    max_h = int(size[1] * fill_ratio)
    scale = min(max_w / img.width, max_h / img.height)
    new_size = (max(1, int(img.width * scale)), max(1, int(img.height * scale)))
    asset = img.resize(new_size, Image.Resampling.LANCZOS)
    x = (size[0] - new_size[0]) // 2
    y = int((size[1] - new_size[1]) * y_bias)
    canvas.alpha_composite(asset, (x, y))
    return canvas


def cover_square(img: Image.Image, size=(1024, 1024)) -> Image.Image:
    scale = max(size[0] / img.width, size[1] / img.height)
    resized = img.resize((int(img.width * scale), int(img.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    out = resized.crop((left, top, left + size[0], top + size[1]))
    out = ImageEnhance.Color(out).enhance(1.08)
    out = ImageEnhance.Contrast(out).enhance(1.06)
    return out


def scene_square_preserve(img: Image.Image, size=(1024, 1024)) -> Image.Image:
    scene = ImageEnhance.Color(img.convert("RGBA")).enhance(1.08)
    scene = ImageEnhance.Contrast(scene).enhance(1.08)

    backdrop = cover_square(scene, size).filter(ImageFilter.GaussianBlur(18))
    backdrop = ImageEnhance.Brightness(backdrop).enhance(0.74)
    backdrop = ImageEnhance.Color(backdrop).enhance(1.12)

    scale = min(size[0] / scene.width, size[1] / scene.height)
    foreground_size = (int(scene.width * scale), int(scene.height * scale))
    foreground = scene.resize(foreground_size, Image.Resampling.LANCZOS)
    foreground = foreground.filter(ImageFilter.UnsharpMask(radius=1.4, percent=115, threshold=3))

    out = backdrop.copy()
    x = (size[0] - foreground.width) // 2
    y = (size[1] - foreground.height) // 2
    out.alpha_composite(foreground, (x, y))
    return out


def make_character_assets(src: Image.Image) -> None:
    full = edge_cutout(crop(src, (7, 50, 168, 383)), 30)
    save(fit_on_canvas(full, (530, 768), 0.92, 0.48), IMAGES / "Hanna.png")
    save(fit_on_canvas(full, (512, 768), 0.92, 0.48), MCQ / "Character" / "mara_midnight_full.png")

    frames = {
        "idle": (366, 82, 414, 147),
        "walk_1": (365, 158, 414, 224),
        "walk_2": (424, 158, 470, 224),
        "jump": (365, 232, 416, 296),
        "fall": (365, 307, 413, 371),
        "hurt": (181, 274, 293, 358),
        "victory": (1150, 789, 1260, 965),
    }
    frame_images = {}
    for name, box in frames.items():
        asset = edge_cutout(crop(src, box), 32)
        frame = fit_on_canvas(asset, (256, 256), 0.84, 0.54)
        frame_images[name] = frame
        save(frame, MCQ / "Character" / f"mara_{name}.png")

    save(fit_on_canvas(edge_cutout(crop(src, frames["idle"]), 32), (55, 50), 0.95, 0.54), IMAGES / "Jinete.png")

    sheet = Image.new("RGBA", (1536, 256), (0, 0, 0, 0))
    for i, key in enumerate(["idle", "walk_1", "walk_2", "jump", "fall", "hurt"]):
        sheet.alpha_composite(frame_images[key], (i * 256, 0))
    save(sheet, MCQ / "Character" / "mara_animation_states.png")


def make_collectibles(src: Image.Image) -> None:
    boxes = {
        "witch_hat": (674, 75, 737, 145),
        "bat_collar": (781, 75, 854, 147),
        "enchanted_boots": (913, 78, 969, 141),
        "magic_cape": (708, 197, 787, 282),
        "special_makeup": (833, 198, 910, 283),
        "candy": (649, 348, 719, 412),
        "star": (740, 348, 816, 412),
        "pumpkin": (826, 346, 886, 412),
        "magic_bat": (913, 346, 982, 412),
    }
    made = {}
    for name, box in boxes.items():
        asset = edge_cutout(crop(src, box), 38, min_fraction=0.035)
        icon = fit_on_canvas(asset, (256, 256), 0.82, 0.5)
        made[name] = icon
        save(icon, MCQ / "Collectibles" / f"{name}.png")

    save(
        fit_on_canvas(edge_cutout(crop(src, boxes["witch_hat"]), 38, min_fraction=0.035), (174, 157), 0.82, 0.5),
        IMAGES / "Diamante.png",
    )


def make_enemies(src: Image.Image) -> None:
    boxes = {
        "ghost": (1122, 516, 1194, 596),
        "spooky_doll": (1196, 516, 1266, 596),
        "bat": (1286, 520, 1356, 594),
        "living_pumpkin": (1394, 505, 1470, 600),
    }
    for name, box in boxes.items():
        asset = edge_cutout(crop(src, box), 34, min_fraction=0.035)
        save(fit_on_canvas(asset, (512, 512), 0.82, 0.5), MCQ / "Enemies" / f"{name}.png")

    active = edge_cutout(crop(src, boxes["ghost"]), 34, min_fraction=0.035)
    save(fit_on_canvas(active, (3464, 3464), 0.62, 0.5), IMAGES / "Espantapajaros.png")


def make_backgrounds(src: Image.Image) -> None:
    boxes = [
        ("Fondo.png", "cementerio_fashion", (10, 490, 236, 664)),
        ("Fondo2.png", "mercado_de_halloween", (250, 490, 464, 664)),
        ("Fondo3.png", "bosque_de_la_luna", (477, 490, 678, 664)),
        ("Fondo4.png", "mansion_encantada", (692, 490, 872, 664)),
        ("Fondo5.png", "plaza_del_festival", (886, 490, 1079, 664)),
    ]
    for filename, slug, box in boxes:
        bg = scene_square_preserve(crop(src, box), (1024, 1024))
        save(bg, IMAGES / "Fondos" / filename)
        save(bg, MCQ / "Backgrounds" / f"{slug}.png")


def make_tiles(src: Image.Image) -> None:
    boxes = {
        "Piso.png": (23, 760, 130, 796),
        "Gran piso.png": (20, 947, 178, 976),
        "Torre piso.png": (144, 762, 210, 833),
    }
    slugs = {
        "Piso.png": "gothic_platform",
        "Gran piso.png": "rose_stone_platform",
        "Torre piso.png": "purple_block_stack",
    }
    for filename, box in boxes.items():
        asset = edge_cutout(crop(src, box), 28)
        save(fit_on_canvas(asset, (3464, 3464), 0.92, 0.5), IMAGES / filename)
        save(fit_on_canvas(asset, (1024, 512), 0.9, 0.5), MCQ / "Tilesets" / f"{slugs[filename]}.png")


def make_hud(src: Image.Image) -> None:
    icons = {
        IMAGES / "Estrella.png": (740, 348, 816, 412),
        IMAGES / "Intento.png": (826, 346, 886, 412),
        IMAGES / "Reloj.png": (1217, 84, 1243, 114),
    }
    for path, box in icons.items():
        asset = edge_cutout(crop(src, box), 38)
        save(fit_on_canvas(asset, (512, 512), 0.78, 0.5), path)
        save(fit_on_canvas(asset, (256, 256), 0.78, 0.5), MCQ / "HUD" / path.name)


def main() -> None:
    if not REF.exists():
        raise SystemExit(f"Reference image not found: {REF}")
    ensure_dirs()
    src = Image.open(REF).convert("RGBA")
    shutil.copyfile(REF, MCQ / "Concept" / "reference_art_board.png")
    write_meta(MCQ / "Concept" / "reference_art_board.png")
    make_character_assets(src)
    make_collectibles(src)
    make_enemies(src)
    make_backgrounds(src)
    make_tiles(src)
    make_hud(src)
    print("Midnight Costume Quest image assets extracted from reference art.")


if __name__ == "__main__":
    main()
