#!/usr/bin/env python3
"""Kalp şeklinde QR kod üretici.

Kullanım: python3 kalp-qr.py https://site-adresin -o kalp-qr.png -t "Defne için"
Gerekenler: pip install -r requirements.txt
"""
import argparse, math, random, sys
import qrcode
from PIL import Image, ImageDraw, ImageFont

FONTS = [  # kalın italik serif; ilk bulunan kullanılır
    "/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf",
    "C:/Windows/Fonts/georgiaz.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldItalic.ttf",
    "/usr/share/fonts/dejavu/DejaVuSerif-BoldItalic.ttf",
]

def hex_renk(s):
    s = s.lstrip("#")
    if len(s) == 3: s = "".join(c * 2 for c in s)
    if len(s) != 6: raise argparse.ArgumentTypeError(f"geçersiz renk: {s!r} (örnek: #d6336c)")
    try: return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError: raise argparse.ArgumentTypeError(f"geçersiz renk: {s!r} (örnek: #d6336c)")

def yazi_tipi(boyut):
    for yol in FONTS:
        try: return ImageFont.truetype(yol, boyut)
        except OSError: pass
    return ImageFont.load_default()

def hucreler(url, gap):
    """QR modüllerini ve kalp kulaklarını (u, v) ızgara hücreleri olarak döndürür."""
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, border=0)
    qr.add_data(url); qr.make(fit=True)
    M = qr.get_matrix(); N = len(M); R = N / 2
    rnd = random.Random(1101)
    cells = {(u, v) for v in range(N) for u in range(N) if M[v][u]}
    # Kulaklar: kalbin üst kenarlarına yarım daireler (aynı modül ızgarasında)
    for v in range(-N, N):
        for u in range(-N, N):
            cu, cv = u + .5, v + .5
            top = cv < -gap and (cu - R) ** 2 + cv ** 2 <= R * R and 0 <= cu <= N
            left = cu < -gap and cu ** 2 + (cv - R) ** 2 <= R * R and 0 <= cv <= N
            if (top or left) and rnd.random() < 0.5:
                cells.add((u, v))
    return cells, N

def ciz(url, gap=1, text="", renk=(214, 51, 108), arka=(255, 246, 250), modul=34):
    cells, N = hucreler(url, gap)
    k = modul / math.sqrt(2)  # 45 derece döndürme
    def P(u, v): return ((u - v) * k, (u + v) * k)
    pts = [P(u + a, v + b) for (u, v) in cells for a in (0, 1) for b in (0, 1)]
    minx = min(p[0] for p in pts); maxx = max(p[0] for p in pts)
    miny = min(p[1] for p in pts); maxy = max(p[1] for p in pts)
    margin = 140
    W = int(maxx - minx + 2 * margin); H = int(maxy - miny + 2 * margin + (140 if text else 0))
    img = Image.new("RGB", (W, H), arka); d = ImageDraw.Draw(img)
    ox, oy = margin - minx, margin - miny
    for (u, v) in cells:
        poly = [P(u, v), P(u + 1, v), P(u + 1, v + 1), P(u, v + 1)]
        d.polygon([(x + ox, y + oy) for x, y in poly], fill=renk)
    if text:
        font = yazi_tipi(84)
        tw = d.textlength(text, font=font)
        d.text(((W - tw) / 2, maxy + oy + 50), text, font=font, fill=renk)
    return img, N

def main(argv=None):
    ap = argparse.ArgumentParser(description="Kalp şeklinde, okunabilir bir QR kod üretir.")
    ap.add_argument("url", help="QR kodun açacağı adres")
    ap.add_argument("-o", "--out", default="kalp-qr.png", help="çıktı dosyası (PNG)")
    ap.add_argument("-t", "--text", default="", help="kalbin altına yazılacak kısa yazı")
    ap.add_argument("--gap", type=int, default=1, help="QR ile kalp kulakları arasındaki boşluk (modül)")
    ap.add_argument("--renk", type=hex_renk, default=hex_renk("#d6336c"), help="kalp rengi (varsayılan #d6336c)")
    ap.add_argument("--arka", type=hex_renk, default=hex_renk("#fff6fa"), help="arka plan rengi (varsayılan #fff6fa)")
    a = ap.parse_args(argv)
    img, N = ciz(a.url, a.gap, a.text, a.renk, a.arka)
    img.save(a.out); print(f"{a.out}: {img.size[0]}x{img.size[1]} px, {N}x{N} modül")

if __name__ == "__main__":
    main()
