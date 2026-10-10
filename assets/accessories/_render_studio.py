"""Studio-style catalog product renders for a phone-accessory store.

Neutral light-gray backdrop, one soft contact shadow, no text or logos.
Photoreal CG, not a camera capture — materials use layered shading only.
"""
from __future__ import annotations

import math
import os
import random

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

W = H = 1200
BG = (245, 246, 248)  # #F5F6F8


def new_canvas() -> Image.Image:
    return Image.new("RGB", (W, H), BG)


def lerp(a, b, t):
    return a + (b - a) * t


def mix(c1, c2, t):
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))


def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, int(v)))


def shade(c, k):
    return tuple(clamp(x * k) for x in c)


def contact_shadow(canvas: Image.Image, cx, cy, rx, ry, alpha=90, blur=18):
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(40, 42, 48, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base = canvas.convert("RGBA")
    return Image.alpha_composite(base, layer).convert("RGB")


def grain(img: Image.Image, amount=6, seed=1) -> Image.Image:
    rnd = random.Random(seed)
    noise = Image.new("L", img.size)
    pix = noise.load()
    # sparse sample then blur — cheaper than per-pixel full noise
    step = 3
    for y in range(0, img.size[1], step):
        for x in range(0, img.size[0], step):
            v = 128 + rnd.randint(-amount, amount)
            for dy in range(step):
                for dx in range(step):
                    if x + dx < img.size[0] and y + dy < img.size[1]:
                        pix[x + dx, y + dy] = v
    noise = noise.filter(ImageFilter.GaussianBlur(0.6))
    nrgb = Image.merge("RGB", (noise, noise, noise))
    return ImageChops.add(ImageChops.subtract(img, Image.new("RGB", img.size, (amount // 2,) * 3)), ImageEnhance.Brightness(nrgb).enhance(0.04), scale=1.0)


def vertical_bg(img: Image.Image) -> Image.Image:
    """Very slight top-to-bottom studio falloff so the field isn't a flat fill."""
    overlay = Image.new("RGB", img.size, (0, 0, 0))
    px = overlay.load()
    for y in range(img.size[1]):
        t = y / (img.size[1] - 1)
        # top a touch lighter, bottom a touch cooler/darker
        v = int(lerp(252, 236, t))
        row = (v, v + 1, min(255, v + 3))
        for x in range(img.size[0]):
            px[x, y] = row
    return Image.blend(img, overlay, 0.35)


def rounded_mask(w, h, r):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    return m


def paste_rgba(base: Image.Image, sprite: Image.Image, xy):
    b = base.convert("RGBA")
    b.alpha_composite(sprite, xy)
    return b.convert("RGB")


# ---------------------------------------------------------------------------
# phone case
# ---------------------------------------------------------------------------

def phone_case(color, clear=False, w=250, h=500, radius=46, seed=3) -> Image.Image:
    """Front-facing silicone case with a camera island. Returns RGBA sprite."""
    spr = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    mask = rounded_mask(w, h, radius)

    body = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = body.load()
    rnd = random.Random(seed)
    for y in range(h):
        for x in range(w):
            # soft vertical highlight, left-of-center key light
            nx = (x / (w - 1) - 0.38) * 2
            ny = (y / (h - 1) - 0.22) * 2
            light = 1.0 - 0.10 * nx - 0.06 * ny
            # edge darkening
            edge = min(x, y, w - 1 - x, h - 1 - y)
            if edge < 18:
                light *= lerp(0.78, 1.0, edge / 18)
            if clear:
                # translucent milky clear silicone
                base = (232, 236, 240)
                a = 118
                c = shade(base, light)
                # faint internal phone-body hint
                inner = 1 if 14 < x < w - 14 and 14 < y < h - 14 else 0
                if inner:
                    c = mix(c, (210, 216, 224), 0.35)
                speckle = rnd.randint(-2, 2)
                px[x, y] = (clamp(c[0] + speckle), clamp(c[1] + speckle), clamp(c[2] + speckle), a)
            else:
                c = shade(color, light)
                speckle = rnd.randint(-3, 3)
                px[x, y] = (clamp(c[0] + speckle), clamp(c[1] + speckle), clamp(c[2] + speckle), 255)

    body.putalpha(ImageChops.multiply(body.getchannel("A"), mask))

    # rim highlight along left and top
    rim = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rim)
    rim_col = (255, 255, 255, 70 if not clear else 140)
    rd.rounded_rectangle([1, 1, w - 2, h - 2], radius=radius, outline=rim_col, width=2)
    rim.putalpha(ImageChops.multiply(rim.getchannel("A"), mask))

    # camera island, top-left
    d = ImageDraw.Draw(body)
    ix, iy, iw, ih, ir = 18, 18, 92, 92, 22
    island = (28, 30, 34, 255) if not clear else (48, 52, 58, 230)
    d.rounded_rectangle([ix, iy, ix + iw, iy + ih], radius=ir, fill=island)
    # two lenses + flash
    for cx, cy, rr in ((ix + 28, iy + 30, 14), (ix + 62, iy + 30, 14), (ix + 28, iy + 64, 11)):
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(12, 14, 18, 255))
        d.ellipse([cx - rr + 3, cy - rr + 3, cx + rr - 3, cy + rr - 3], fill=(36, 42, 52, 255))
        d.ellipse([cx - 4, cy - 6, cx - 1, cy - 3], fill=(180, 200, 220, 180))
    d.ellipse([ix + 58, iy + 58, ix + 70, iy + 70], fill=(230, 230, 220, 255))
    d.ellipse([ix + 61, iy + 60, ix + 65, iy + 64], fill=(255, 255, 255, 200))

    # side button nubs on the right edge
    for by, bh in ((150, 28), (196, 48), (258, 48)):
        d.rounded_rectangle([w - 4, by, w + 6, by + bh], radius=3, fill=shade(color if not clear else (180, 186, 194), 0.85) + ((220 if clear else 255),))

    spr.alpha_composite(body)
    spr.alpha_composite(rim)
    return spr


def render_cases(path):
    img = vertical_bg(new_canvas())
    # three cases, slightly overlapping, standing (front view, slight perspective via offset)
    specs = [
        # (x, y, color, clear, seed) drawn back-to-front
        (250, 300, (58, 62, 68), False, 4),     # charcoal, back right
        (455, 270, (22, 22, 24), False, 7),     # matte black, middle
        (660, 310, (230, 234, 238), True, 2),   # clear, front left-of-right
    ]
    # shadows first
    for x, y, *_ in specs:
        img = contact_shadow(img, x + 125, y + 490, 110, 16, alpha=70, blur=14)
    for x, y, color, clear, seed in specs:
        spr = phone_case(color, clear=clear, seed=seed)
        img = paste_rgba(img, spr, (x, y))
    img = grain(img, 5, seed=11)
    img.save(path, "PNG")


# ---------------------------------------------------------------------------
# tempered glass + cloth
# ---------------------------------------------------------------------------

def render_glass(path):
    img = vertical_bg(new_canvas())
    # glass lying flat, slight angle — draw into a layer then rotate
    gw, gh = 430, 860
    glass = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
    mask = rounded_mask(gw, gh, 54)
    gpx = glass.load()
    for y in range(gh):
        for x in range(gw):
            # cool transparent pane with a diagonal specular streak
            dx = (x / gw) * 0.7 + (y / gh) * 0.3
            streak = math.exp(-((dx - 0.42) ** 2) / 0.004) * 0.55
            base_a = 42 + int(streak * 90)
            tint = mix((214, 224, 232), (255, 255, 255), streak)
            gpx[x, y] = (*tint, base_a)
    glass.putalpha(ImageChops.multiply(glass.getchannel("A"), mask))
    # crisp edge
    edge = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
    ImageDraw.Draw(edge).rounded_rectangle([1, 1, gw - 2, gh - 2], radius=54, outline=(255, 255, 255, 170), width=2)
    edge.putalpha(ImageChops.multiply(edge.getchannel("A"), mask))
    glass.alpha_composite(edge)
    # speaker / sensor cutouts near top, faint
    d = ImageDraw.Draw(glass)
    d.rounded_rectangle([gw // 2 - 46, 28, gw // 2 + 46, 42], radius=7, fill=(180, 190, 200, 70))
    d.ellipse([gw // 2 - 78, 26, gw // 2 - 62, 42], fill=(180, 190, 200, 60))

    glass = glass.rotate(18, expand=True, resample=Image.BICUBIC)
    gx = 250
    gy = 150
    # shadow under the rotated pane
    img = contact_shadow(img, gx + glass.size[0] // 2 + 10, gy + glass.size[1] // 2 + 18, 250, 40, alpha=55, blur=16)

    # microfiber cloth, folded, to the lower right of the glass
    cloth = folded_cloth(340, 210, seed=9)
    cloth = cloth.rotate(-8, expand=True, resample=Image.BICUBIC)
    cx, cy = 700, 760
    img = contact_shadow(img, cx + cloth.size[0] // 2, cy + cloth.size[1] - 8, 150, 18, alpha=60, blur=12)
    img = paste_rgba(img, glass, (gx, gy))
    img = paste_rgba(img, cloth, (cx, cy))
    img = grain(img, 4, seed=21)
    img.save(path, "PNG")


def folded_cloth(w, h, seed=1) -> Image.Image:
    spr = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = spr.load()
    rnd = random.Random(seed)
    base = (122, 126, 132)
    for y in range(h):
        for x in range(w):
            # weave
            weave = 6 if ((x // 2 + y // 2) % 2 == 0) else -4
            # fold: a diagonal ridge across the upper third
            fold = 0
            ridge = y - int(h * 0.38) - int((x - w / 2) * 0.08)
            if abs(ridge) < 10:
                fold = int(18 * (1 - abs(ridge) / 10))
            elif ridge < 0:
                fold = 8  # upper layer slightly lighter
            light = 1.0 + fold / 80
            c = shade(base, light)
            px[x, y] = (clamp(c[0] + weave + rnd.randint(-2, 2)),
                        clamp(c[1] + weave + rnd.randint(-2, 2)),
                        clamp(c[2] + weave + rnd.randint(-2, 2)), 255)
    # soft rounded corners
    m = rounded_mask(w, h, 16)
    spr.putalpha(ImageChops.multiply(spr.getchannel("A"), m))
    # hem line
    d = ImageDraw.Draw(spr)
    d.line([(12, h - 18), (w - 12, h - 22)], fill=(90, 94, 100, 140), width=2)
    return spr


# ---------------------------------------------------------------------------
# charger + cable
# ---------------------------------------------------------------------------

def render_chargers(path):
    img = vertical_bg(new_canvas())
    # upright compact wall charger, slightly right of center-left
    cw, ch = 210, 250
    body = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    mask = rounded_mask(cw, ch, 36)
    px = body.load()
    white = (244, 244, 246)
    for y in range(ch):
        for x in range(cw):
            nx = (x / (cw - 1) - 0.35)
            light = 1.02 - 0.10 * nx - 0.04 * (y / ch)
            edge = min(x, y, cw - 1 - x, ch - 1 - y)
            if edge < 10:
                light *= lerp(0.90, 1.0, edge / 10)
            c = shade(white, light)
            px[x, y] = (*c, 255)
    body.putalpha(ImageChops.multiply(body.getchannel("A"), mask))
    d = ImageDraw.Draw(body)
    # top seam / face
    d.rounded_rectangle([2, 2, cw - 3, ch - 3], radius=34, outline=(255, 255, 255, 200), width=2)
    # USB-C port oval, front face, lower third
    port = [cw // 2 - 28, ch - 78, cw // 2 + 28, ch - 58]
    d.rounded_rectangle(port, radius=10, fill=(60, 62, 68, 255))
    d.rounded_rectangle([port[0] + 6, port[1] + 5, port[2] - 6, port[3] - 5], radius=6, fill=(28, 30, 34, 255))
    # tiny metal tongue
    d.rectangle([cw // 2 - 8, port[1] + 7, cw // 2 + 8, port[3] - 7], fill=(170, 174, 180, 255))

    bx, by = 390, 430
    img = contact_shadow(img, bx + cw // 2 + 6, by + ch + 6, 120, 16, alpha=75, blur=12)
    img = paste_rgba(img, body, (bx, by))

    # short white cable loosely coiled to the right
    cable = coiled_cable(420, 420, color=(236, 236, 238), coils=3.2, thick=16, seed=5, braid=False)
    img = contact_shadow(img, 860, 640, 150, 28, alpha=55, blur=14)
    img = paste_rgba(img, cable, (640, 430))
    img = grain(img, 4, seed=31)
    img.save(path, "PNG")


def coiled_cable(w, h, color, coils, thick, seed, braid=False) -> Image.Image:
    spr = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(draw_layer)
    cx, cy = w / 2, h / 2
    rnd = random.Random(seed)
    steps = int(coils * 140)
    pts = []
    for i in range(steps):
        t = i / steps
        ang = t * coils * 2 * math.pi
        # flat oval
        rx = w * 0.36 * (0.55 + 0.45 * t)
        ry = h * 0.30 * (0.55 + 0.45 * t)
        jx = rnd.uniform(-1.2, 1.2)
        jy = rnd.uniform(-1.2, 1.2)
        pts.append((cx + math.cos(ang) * rx + jx, cy + math.sin(ang) * ry * 0.72 + jy))
    # draw as a thick stroke with a highlight pass
    def stroke(points, width, fill):
        d.line(points, fill=fill, width=width, joint="curve")
        # round caps
        r = width // 2
        for p in (points[0], points[-1]):
            d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=fill)

    shadow_c = shade(color, 0.72) + (255,)
    stroke(pts, thick + 2, shadow_c)
    stroke(pts, thick, color + (255,))
    # highlight along inner
    hi = shade(color, 1.12) + (255,)
    stroke([(p[0] - 1, p[1] - 2) for p in pts], max(3, thick // 4), hi)

    if braid:
        # diagonal hatch suggesting a braid, clipped to the cable via the alpha
        hatch = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        hd = ImageDraw.Draw(hatch)
        dark = shade(color, 0.78) + (90,)
        light = shade(color, 1.15) + (70,)
        for i in range(-h, w + h, 7):
            hd.line([(i, 0), (i + h, h)], fill=dark if (i // 7) % 2 == 0 else light, width=2)
        # keep hatch only where the cable is
        alpha = draw_layer.getchannel("A")
        hatch.putalpha(ImageChops.multiply(hatch.getchannel("A"), alpha))
        draw_layer.alpha_composite(hatch)

    # USB-C plug at the outer end
    end = pts[-1]
    prev = pts[-8]
    ang = math.atan2(end[1] - prev[1], end[0] - prev[0])
    plug = usb_c_plug(color)
    plug = plug.rotate(-math.degrees(ang), expand=True, resample=Image.BICUBIC)
    draw_layer.alpha_composite(plug, (int(end[0] - plug.size[0] / 2), int(end[1] - plug.size[1] / 2)))
    return draw_layer


def usb_c_plug(cable_color) -> Image.Image:
    w, h = 54, 22
    spr = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(spr)
    # metal housing
    d.rounded_rectangle([8, 2, w - 2, h - 3], radius=6, fill=(186, 190, 196, 255))
    d.rounded_rectangle([14, 6, w - 8, h - 7], radius=4, fill=(150, 154, 160, 255))
    # strain relief matching cable
    d.rounded_rectangle([0, 4, 16, h - 5], radius=4, fill=shade(cable_color, 0.9) + (255,))
    return spr


def render_cables(path):
    img = vertical_bg(new_canvas())
    cable = coiled_cable(780, 520, color=(62, 66, 72), coils=4.0, thick=22, seed=8, braid=True)
    img = contact_shadow(img, W // 2 + 8, H // 2 + 30, 280, 48, alpha=60, blur=16)
    img = paste_rgba(img, cable, ((W - 780) // 2, (H - 520) // 2 + 20))
    img = grain(img, 4, seed=41)
    img.save(path, "PNG")


# ---------------------------------------------------------------------------
# earbuds
# ---------------------------------------------------------------------------

def render_earbuds(path):
    img = vertical_bg(new_canvas())
    # open case, viewed from a slight front-above angle: lid behind, base in front
    cw, ch = 560, 250
    case = Image.new("RGBA", (cw, 430), (0, 0, 0, 0))

    def pill_body(target, box, radius, color, seed):
        x0, y0, x1, y1 = box
        w, h = x1 - x0, y1 - y0
        tile = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        px = tile.load()
        rnd = random.Random(seed)
        for y in range(h):
            for x in range(w):
                nx = (x / max(1, w - 1) - 0.32)
                ny = (y / max(1, h - 1) - 0.25)
                light = 1.03 - 0.08 * nx - 0.05 * ny
                edge = min(x, y, w - 1 - x, h - 1 - y)
                if edge < 12:
                    light *= lerp(0.88, 1.0, edge / 12)
                c = shade(color, light)
                s = rnd.randint(-2, 2)
                px[x, y] = (clamp(c[0] + s), clamp(c[1] + s), clamp(c[2] + s), 255)
        m = rounded_mask(w, h, radius)
        tile.putalpha(ImageChops.multiply(tile.getchannel("A"), m))
        target.alpha_composite(tile, (x0, y0))

    # lid, behind and slightly higher, tilted open (drawn as a shallower ellipse-ish slab)
    pill_body(case, (40, 10, 520, 150), 46, (236, 236, 238), seed=3)
    # hinge shadow between lid and base
    hd = ImageDraw.Draw(case)
    hd.pieslice([70, 120, 490, 200], 0, 180, fill=(210, 212, 216, 255))
    # base
    pill_body(case, (20, 150, 540, 400), 56, (248, 248, 250), seed=6)
    # interior well
    well = Image.new("RGBA", case.size, (0, 0, 0, 0))
    wd = ImageDraw.Draw(well)
    wd.rounded_rectangle([58, 188, 502, 372], radius=46, fill=(226, 228, 232, 255))
    case.alpha_composite(well)

    # two earbuds sitting in the well
    def earbud(flip=False) -> Image.Image:
        ew, eh = 150, 110
        spr = Image.new("RGBA", (ew, eh), (0, 0, 0, 0))
        d = ImageDraw.Draw(spr)
        # stem
        stem_box = [78, 28, 112, 100] if not flip else [38, 28, 72, 100]
        d.rounded_rectangle(stem_box, radius=14, fill=(244, 244, 246, 255))
        d.rounded_rectangle([stem_box[0] + 2, stem_box[1] + 2, stem_box[2] - 2, stem_box[1] + 18],
                            radius=8, fill=(255, 255, 255, 180))
        # bud head
        head = [18, 8, 100, 78] if not flip else [50, 8, 132, 78]
        d.ellipse(head, fill=(250, 250, 252, 255))
        # silicone tip
        tip = [8, 22, 46, 64] if not flip else [104, 22, 142, 64]
        d.ellipse(tip, fill=(232, 234, 238, 255))
        d.ellipse([tip[0] + 8, tip[1] + 8, tip[2] - 8, tip[3] - 8], fill=(90, 94, 100, 255))
        # mesh dot on stem
        mx = (stem_box[0] + stem_box[2]) // 2
        d.ellipse([mx - 5, 78, mx + 5, 88], fill=(70, 74, 80, 255))
        if flip:
            spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
        return spr

    case.alpha_composite(earbud(False), (90, 210))
    case.alpha_composite(earbud(True), (310, 210))
    # small status LED, no logo
    ld = ImageDraw.Draw(case)
    ld.ellipse([268, 368, 280, 380], fill=(190, 194, 198, 255))

    cx = (W - case.size[0]) // 2
    cy = 360
    img = contact_shadow(img, W // 2 + 10, cy + 400, 250, 22, alpha=70, blur=16)
    img = paste_rgba(img, case, (cx, cy))
    img = grain(img, 4, seed=51)
    img.save(path, "PNG")


def main():
    out = os.path.dirname(os.path.abspath(__file__))
    jobs = [
        ("cases.png", render_cases),
        ("glass.png", render_glass),
        ("chargers.png", render_chargers),
        ("cables.png", render_cables),
        ("earbuds.png", render_earbuds),
    ]
    for name, fn in jobs:
        dest = os.path.join(out, name)
        fn(dest)
        print("wrote", dest, os.path.getsize(dest))


if __name__ == "__main__":
    main()
