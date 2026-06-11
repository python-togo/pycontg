"""Generate QR code card images for PyCon Togo Support page (3 variants)."""

from pathlib import Path
import qrcode
from PIL import Image, ImageDraw, ImageFont

# ── Config ────────────────────────────────────────────────
DONATE_URL  = "https://pycontg.pytogo.org/donate"
BASE_DIR    = Path(__file__).parent.parent
OUT_DIR     = BASE_DIR / "app/static/2026/images"
LOGO_SM     = BASE_DIR / "app/static/images/pycontogo.png"
LOGO_NAV    = BASE_DIR / "app/static/images/PyContg26_png/7.png"

# Couleurs charte
GREEN       = (16, 147, 49)    # #109331
WHITE       = (255, 255, 255)
DARK_TEXT   = (30, 38, 48)
GRAY_TEXT   = (108, 117, 125)

# Couleurs drapeau Togo
TOGO_GREEN  = (0,  102, 51)    # vert
TOGO_YELLOW = (255, 206, 0)    # jaune
TOGO_RED    = (205, 42,  62)   # rouge

CARD_W  = 420
CARD_H  = 690
RADIUS  = 22

# ── Helpers ───────────────────────────────────────────────
def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, size[0]-1, size[1]-1], radius=radius, fill=255
    )
    return mask


def gen_qr(url):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").convert("RGBA")


def recolor_qr(img, dark_color, light_color=(255, 255, 255)):
    gray   = img.convert("L")
    dark   = Image.new("RGBA", img.size, dark_color + (255,))
    light  = Image.new("RGBA", img.size, light_color + (255,))
    mask   = gray.point(lambda p: 255 if p < 128 else 0, "L")
    result = light.copy()
    result.paste(dark, mask=mask)
    return result


def color_finder_rings(qr_img, box_size=10, border=3):
    """Color the outer ring of the 3 QR finder patterns with Togo flag colors.
    Modules remain black; only the finder outer squares get a color."""
    img  = qr_img.copy()
    W    = img.width
    bs   = box_size
    q    = border * bs       # quiet zone in px
    fp   = 7 * bs            # finder pattern size in px

    corners = [
        (q,          q,          TOGO_GREEN  + (255,)),  # top-left
        (W - q - fp, q,          TOGO_RED    + (255,)),  # top-right
        (q,          W - q - fp, TOGO_YELLOW + (255,)),  # bottom-left
    ]

    draw = ImageDraw.Draw(img)
    for x0, y0, color in corners:
        # 1. Fill entire 7×7 finder area with the flag color
        draw.rectangle([x0, y0, x0 + fp - 1, y0 + fp - 1], fill=color)
        # 2. Restore interior 5×5 as white
        draw.rectangle([x0 + bs,     y0 + bs,
                        x0 + fp - bs - 1, y0 + fp - bs - 1],
                       fill=(255, 255, 255, 255))
        # 3. Restore innermost 3×3 dot as black
        draw.rectangle([x0 + 2*bs,       y0 + 2*bs,
                        x0 + fp - 2*bs - 1, y0 + fp - 2*bs - 1],
                       fill=(0, 0, 0, 255))

    return img


def embed_logo(qr_img, logo_path, ratio=0.16):
    logo = Image.open(logo_path).convert("RGBA")
    target = int(min(qr_img.size) * ratio)
    logo.thumbnail((target, target), Image.LANCZOS)
    pad = 7
    bw, bh = logo.width + pad * 2, logo.height + pad * 2
    bg = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    bg.paste(Image.new("RGBA", (bw, bh), (255, 255, 255, 255)),
             mask=rounded_mask((bw, bh), 8))
    bg.paste(logo, (pad, pad), logo)
    out = qr_img.copy()
    out.paste(bg, ((qr_img.width - bw) // 2, (qr_img.height - bh) // 2), bg)
    return out


def remove_black_bg(img_path, threshold=22):
    """Make near-black pixels transparent (for logos on dark background)."""
    img = Image.open(img_path).convert("RGBA")
    gray = img.convert("L")
    alpha_mask = gray.point(lambda p: 0 if p < threshold else 255, "L")
    img.putalpha(alpha_mask)
    return img


def load_font(size):
    for f in ["C:/Windows/Fonts/segoeui.ttf",
              "C:/Windows/Fonts/arial.ttf",
              "C:/Windows/Fonts/Arial.ttf"]:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            pass
    return ImageFont.load_default()


def finalize(card, out_path, w=CARD_W, h=CARD_H):
    result = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    result.paste(card, mask=rounded_mask((w, h), RADIUS))
    result.save(out_path, "PNG")
    print(f"  OK: {out_path.name}")


# ── Option A — Style PayDunya vert ────────────────────────
def make_a():
    card = Image.new("RGBA", (CARD_W, CARD_H), GREEN)
    draw = ImageDraw.Draw(card)

    logo = remove_black_bg(LOGO_NAV)
    logo.thumbnail((200, 90), Image.LANCZOS)
    card.paste(logo, ((CARD_W - logo.width) // 2, 28), logo)

    qr  = color_finder_rings(gen_qr(DONATE_URL))
    qr  = embed_logo(qr, LOGO_SM)
    qr  = qr.resize((300, 300), Image.LANCZOS)
    qbg = Image.new("RGBA", (320, 320), (0, 0, 0, 0))
    qbg.paste(Image.new("RGBA", (320, 320), (255, 255, 255, 220)),
              mask=rounded_mask((320, 320), 16))
    qbg.paste(qr, (10, 10), qr)
    card.paste(qbg, ((CARD_W - 320) // 2, 148), qbg)

    draw.line([(50, 488), (CARD_W-50, 488)], fill=(255,255,255,50), width=1)
    draw.text((CARD_W//2, 510), "Scannez avec votre appareil photo",
              font=load_font(17), fill=(255,255,255,225), anchor="mm")
    draw.text((CARD_W//2, 540), "Mobile Money  -  Visa  -  PayPal",
              font=load_font(13), fill=(255,255,255,150), anchor="mm")

    finalize(card, OUT_DIR / "support_qr_a.png")


# ── Option B — Style carte blanche ────────────────────────
def make_b():
    card = Image.new("RGBA", (CARD_W, CARD_H), WHITE)
    draw = ImageDraw.Draw(card)

    # Header vert
    draw.rounded_rectangle([0, 0, CARD_W, 120], radius=RADIUS, fill=GREEN)
    draw.rectangle([0, RADIUS, CARD_W, 120], fill=GREEN)

    logo = remove_black_bg(LOGO_NAV)
    logo.thumbnail((180, 80), Image.LANCZOS)
    card.paste(logo, ((CARD_W - logo.width) // 2, (120 - logo.height) // 2), logo)

    qr = color_finder_rings(gen_qr(DONATE_URL))
    qr = embed_logo(qr, LOGO_SM)
    qr = qr.resize((280, 280), Image.LANCZOS)
    card.paste(qr, ((CARD_W - 280) // 2, 138), qr)

    draw.text((CARD_W//2, 440), "Scannez pour soutenir PyCon Togo",
              font=load_font(17), fill=GREEN, anchor="mm")
    draw.text((CARD_W//2, 465), "Mobile Money  -  Visa  -  PayPal",
              font=load_font(13), fill=GRAY_TEXT, anchor="mm")

    draw.rounded_rectangle([50, 500, CARD_W-50, 548], radius=24, fill=GREEN)
    draw.text((CARD_W//2, 524), "Soutenir PyCon Togo",
              font=load_font(16), fill=WHITE, anchor="mm")

    finalize(card, OUT_DIR / "support_qr_b.png")


# ── Option C — Style carte propre (CHOSEN) ────────────────
def make_c():
    W, H = CARD_W, CARD_H
    card = Image.new("RGBA", (W, H), WHITE)
    draw = ImageDraw.Draw(card)

    # ── Logo PyCon Togo (fond noir rendu transparent) ─────
    logo = remove_black_bg(LOGO_NAV, threshold=22)
    bbox = logo.getbbox()           # supprime le padding transparent
    if bbox:
        logo = logo.crop(bbox)
    logo.thumbnail((300, 134), Image.LANCZOS)
    lx = (W - logo.width) // 2
    card.paste(logo, (lx, 22), logo)

    # ── Séparateur doré ───────────────────────────────────
    sep_y = 22 + logo.height + 8
    sep_w = 50
    draw.rectangle([(W - sep_w)//2, sep_y, (W + sep_w)//2, sep_y + 3],
                   fill=TOGO_YELLOW)

    # ── Texte de description (couleur sombre) ────────────
    txt_y = sep_y + 14
    font_desc = load_font(15)
    lines_fr = [
        "Aidez-nous a faire grandir la",
        "communaute Python au Togo.",
        "Chaque contribution compte.",
    ]
    for i, line in enumerate(lines_fr):
        draw.text((W//2, txt_y + i * 21), line,
                  font=font_desc, fill=DARK_TEXT, anchor="mm")

    # ── QR code : modules noirs + coins finder colorés ───
    qr_raw  = gen_qr(DONATE_URL)
    qr_col  = color_finder_rings(qr_raw)
    QR_SIZE = 334
    qr_final = qr_col.resize((QR_SIZE, QR_SIZE), Image.LANCZOS)

    qr_top = txt_y + len(lines_fr) * 21 + 14
    # Fond blanc légèrement teinté derrière le QR
    qbg_size = QR_SIZE + 16
    qbg = Image.new("RGBA", (qbg_size, qbg_size), (248, 251, 249, 255))
    qbg_r = Image.new("RGBA", (qbg_size, qbg_size), (0, 0, 0, 0))
    qbg_r.paste(qbg, mask=rounded_mask((qbg_size, qbg_size), 14))
    qbg_r.paste(qr_final, (8, 8), qr_final)
    card.paste(qbg_r, ((W - qbg_size) // 2, qr_top), qbg_r)

    # ── Bouton CTA vert ───────────────────────────────────
    btn_top = qr_top + qbg_size + 16
    draw.rounded_rectangle([44, btn_top, W - 44, btn_top + 50],
                           radius=25, fill=GREEN)
    draw.text((W//2, btn_top + 25), "Soutenir PyCon Togo",
              font=load_font(17), fill=WHITE, anchor="mm")

    # ── Domaine en bas ────────────────────────────────────
    domain_y = btn_top + 66
    draw.text((W//2, domain_y), "pycontg.pytogo.org",
              font=load_font(12), fill=(180, 180, 180), anchor="mm")

    # Recadrer la hauteur réelle utilisée
    actual_h = domain_y + 28
    card = card.crop((0, 0, W, actual_h))

    result = Image.new("RGBA", (W, actual_h), (0, 0, 0, 0))
    result.paste(card, mask=rounded_mask((W, actual_h), RADIUS))
    result.save(OUT_DIR / "support_qr_c.png", "PNG")
    print(f"  OK: support_qr_c.png  ({W}x{actual_h}px)")

    import shutil
    shutil.copy(OUT_DIR / "support_qr_c.png", OUT_DIR / "support_qr.png")
    print("  >> support_qr.png -> Option C")


# ── Main ──────────────────────────────────────────────────
if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Generation des QR codes...")
    print("\n Option A - Style vert")
    make_a()
    print("\n Option B - Style carte blanche header vert")
    make_b()
    print("\n Option C - Style carte propre (CHOSEN)")
    make_c()
    print(f"\nTermine -> {OUT_DIR}")
