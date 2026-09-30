#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DiscordUtility · v2.1 — remasterisée + intro cinématique
═══════════════════════════════════════════════════════════════════════
  Intro : CRT → BIOS → panne → hyperespace → noyau 3D → bannière
  forgée en glitch → checks → BIENVENUE (une touche pour passer).

  Le tool est inchangé : amis, DM simple/multiple/tous, profil,
  serveurs, départ, statistiques. Palette officielle Discord.

  ⚠  Token utilisateur = CGU violées = risque de ban. À vos risques.
"""

import os
import sys
import time
import math
import random
import shutil
import datetime
import threading
import getpass

try:
    import requests
except ImportError:
    print("\033[91m[!] Le module 'requests' est requis.\n    → pip install requests\033[0m")
    sys.exit(1)

VERSION = "2.1"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# ══════════════════════════════════════════════════════════════════════
#  1 · COULEURS (palette Discord, truecolor + repli 256)
# ══════════════════════════════════════════════════════════════════════

RESET   = "\033[0m"
BOLD    = "\033[1m"
CUR_OFF = "\033[?25l"
CUR_ON  = "\033[?25h"
HOME    = "\033[H"
CLR     = "\033[2J"

TRUECOLOR = (os.environ.get("COLORTERM", "").lower() in ("truecolor", "24bit")
             or os.environ.get("WT_SESSION") is not None
             or os.environ.get("TERM_PROGRAM") in ("iTerm.app", "vscode", "WezTerm")
             or os.name == "nt")

BLURPLE   = (88, 101, 242)
BLURPLE_L = (145, 152, 255)
GREEN     = (87, 242, 135)
YELLOW    = (254, 231, 92)
RED       = (237, 66, 69)
WHITE     = (255, 255, 255)
TXT       = (212, 214, 218)
MUT       = (130, 133, 142)
FAINT     = (82, 85, 94)

_FG, _BG = {}, {}


def _c256(c):
    return 16 + 36 * (c[0] * 5 // 255) + 6 * (c[1] * 5 // 255) + (c[2] * 5 // 255)


def fg(c):
    s = _FG.get(c)
    if s is None:
        s = ("\033[38;2;%d;%d;%dm" % c) if TRUECOLOR else ("\033[38;5;%dm" % _c256(c))
        _FG[c] = s
    return s


def bg(c):
    s = _BG.get(c)
    if s is None:
        s = ("\033[48;2;%d;%d;%dm" % c) if TRUECOLOR else ("\033[48;5;%dm" % _c256(c))
        _BG[c] = s
    return s


def mix(a, b, t):
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    return (int(a[0] + (b[0] - a[0]) * t), int(a[1] + (b[1] - a[1]) * t),
            int(a[2] + (b[2] - a[2]) * t))


def ramp(stops, n=96):
    out = []
    for i in range(n):
        t = i / (n - 1) * (len(stops) - 1)
        k = min(int(t), len(stops) - 2)
        f = t - k
        out.append(tuple(int(round(stops[k][j] + (stops[k + 1][j] - stops[k][j]) * f))
                         for j in range(3)))
    return out


R_BLURPLE = ramp([(5, 6, 16), (20, 24, 72), (52, 62, 166), (88, 101, 242),
                  (145, 152, 255), (214, 220, 255), (255, 255, 255)])


def palv(pal, t):
    i = int(t * (len(pal) - 1))
    if i < 0:
        i = 0
    elif i >= len(pal):
        i = len(pal) - 1
    return pal[i]


# ══════════════════════════════════════════════════════════════════════
#  2 · BANNIÈRE (l'originale, conservée)
# ══════════════════════════════════════════════════════════════════════

BANNER = """
 ██████████    ███                                          █████ █████  █████  █████     ███  ████   ███   █████              
▒▒███▒▒▒▒███  ▒▒▒                                          ▒▒███ ▒▒███  ▒▒███  ▒▒███     ▒▒▒  ▒▒███  ▒▒▒   ▒▒███               
 ▒███   ▒▒███ ████   █████   ██████   ██████  ████████   ███████  ▒███   ▒███  ███████   ████  ▒███  ████  ███████   █████ ████
 ▒███    ▒▒███▒▒███  ███▒▒   ███▒▒███ ███▒▒███▒▒███▒▒███ ███▒▒███  ▒███   ▒███ ▒▒▒███▒   ▒▒███  ▒███ ▒▒███ ▒▒▒███▒   ▒▒███ ▒███ 
 ▒███    ▒▒███ ▒███ ▒▒█████ ▒███ ▒▒▒ ▒███ ▒▒███ ▒███ ▒▒▒ ▒███ ▒▒███  ▒███   ▒███   ▒███     ▒▒███  ▒███  ▒███   ▒▒███     ▒███ ▒███ 
 ▒███    ███  ▒███  ▒▒▒▒███▒███  ███▒███ ▒▒███ ▒███     ▒███ ▒▒███  ▒███   ▒███   ▒███ ███ ▒▒███  ▒███  ▒███   ▒███ ███ ▒███ ▒███ 
 ██████████   █████ ██████ ▒▒██████ ▒▒██████  █████    ▒▒████████ ▒▒████████    ▒▒█████  █████ █████ █████  ▒▒█████  ▒▒███████ 
▒▒▒▒▒▒▒▒▒▒   ▒▒▒▒▒ ▒▒▒▒▒▒   ▒▒▒▒▒▒   ▒▒▒▒▒▒  ▒▒▒▒▒      ▒▒▒▒▒▒▒▒   ▒▒▒▒▒▒▒▒      ▒▒▒▒▒  ▒▒▒▒▒ ▒▒▒▒▒ ▒▒▒▒▒    ▒▒▒▒▒    ▒▒▒▒▒███ 
                                                                                                                      ███ ▒███ 
                                                                                                                     ▒▒██████  
                                                                                                                      ▒▒▒▒▒▒                                                                           
"""


def banner_lines():
    return [l.rstrip() for l in BANNER.strip("\n").split("\n")]


def banner_colors(n):
    return [mix((150, 158, 255), (88, 101, 242), i / max(1, n - 1)) for i in range(n)]


# ══════════════════════════════════════════════════════════════════════
#  3 · TERMINAL, CLAVIER, FRAME
# ══════════════════════════════════════════════════════════════════════

def term_size():
    c, r = shutil.get_terminal_size((100, 30))
    return max(c, 40), max(r, 12)


def line_at(s):
    sys.stdout.write("\r\033[2K" + s)
    sys.stdout.flush()


def type_out(text, color=TXT, speed=0.02, prefix="  "):
    sys.stdout.write(prefix + fg(color))
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(speed)
    sys.stdout.write(RESET + "\r\n")
    sys.stdout.flush()


def tr(s, w):
    s = str(s)
    return s if len(s) <= w else s[:max(0, w - 1)] + "…"


def wrap(s, w):
    out, cur = [], ""
    for word in str(s).split():
        if len(cur) + len(word) + 1 <= w:
            cur = (cur + " " + word).strip()
        else:
            if cur:
                out.append(cur)
            while len(word) > w:
                out.append(word[:w])
                word = word[w:]
            cur = word
    if cur:
        out.append(cur)
    return out or [""]


class Keyboard:
    def __init__(self):
        self.nt = os.name == "nt"
        self.active = False

    def start(self):
        if self.active:
            return
        if self.nt:
            import msvcrt
            self.m = msvcrt
        else:
            import termios
            import tty
            self.t = termios
            self.fd = sys.stdin.fileno()
            self.old = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)
        self.active = True

    def stop(self):
        if not self.active:
            return
        if self.nt:
            while self.m.kbhit():
                self.m.getch()
        else:
            self.t.tcflush(self.fd, self.t.TCIFLUSH)
            self.t.tcsetattr(self.fd, self.t.TCSADRAIN, self.old)
        self.active = False

    def pressed(self):
        if not self.active:
            return False
        if self.nt:
            return self.m.kbhit()
        import select
        return bool(select.select([sys.stdin], [], [], 0)[0])

    def read(self):
        if self.nt:
            ch = self.m.getch()
            if ch in (b"\x00", b"\xe0"):
                n = self.m.getch()
                return {b"H": "up", b"P": "down", b"K": "left", b"M": "right"}.get(n, "?")
            if ch in (b"\r", b"\n"):
                return "enter"
            if ch == b"\x03":
                raise KeyboardInterrupt
            if ch == b"\x1b":
                return "esc"
            return ch.decode("utf-8", "ignore").lower() or "?"
        ch = sys.stdin.read(1)
        if ch == "":
            raise EOFError
        if ch == "\x03":
            raise KeyboardInterrupt
        if ch in ("\r", "\n"):
            return "enter"
        if ch == "\x1b":
            import select
            if not select.select([sys.stdin], [], [], 0.05)[0]:
                return "esc"
            c2 = sys.stdin.read(1)
            if c2 == "[":
                return {"A": "up", "B": "down", "C": "right", "D": "left"}.get(
                    sys.stdin.read(1), "?")
            return "esc"
        return ch.lower()


KB = Keyboard()


class SkipIntro(Exception):
    pass


def skip_check():
    if KB.active and KB.pressed():
        KB.read()
        raise SkipIntro()


class Frame:
    """Redessine des lignes en place, sans clear → zéro flicker (menus)."""

    def __init__(self):
        self.n = 0
        self.size = None

    def draw(self, lines):
        sz = term_size()
        if sz != self.size:
            sys.stdout.write(HOME + CLR)
            self.n = 0
            self.size = sz
        if self.n > 1:
            sys.stdout.write("\033[%dA" % (self.n - 1))
        out = []
        for i, l in enumerate(lines):
            out.append("\r\033[2K" + l)
            if i < len(lines) - 1:
                out.append("\r\n")
        out.append("\033[0J")
        sys.stdout.write("".join(out))
        sys.stdout.flush()
        self.n = len(lines)


class Clock:
    def __init__(self, fps):
        self.iv = 1.0 / fps
        self.last = time.perf_counter()

    def tick(self):
        now = time.perf_counter()
        dt = now - self.last
        if dt < self.iv:
            time.sleep(self.iv - dt)
            now = time.perf_counter()
            dt = now - self.last
        self.last = now
        return min(dt, 0.1)


# ══════════════════════════════════════════════════════════════════════
#  4 · MOTEUR D'INTRO — canevas demi-blocs (2 pixels par cellule)
# ══════════════════════════════════════════════════════════════════════

GARB = "!<>-_\\/[]{}=+*^?#%&@$01"
HALF = "▀"


class Cv:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.ph = h * 2
        self.px = [[(7, 8, 16)] * w for _ in range(self.ph)]
        self.txt = {}
        self.prev = [None] * h

    def clear(self, c=(7, 8, 16)):
        self.px = [[c] * self.w for _ in range(self.ph)]
        self.txt = {}

    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.ph:
            self.px[y][x] = c

    def add(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.ph:
            o = self.px[y][x]
            r, g, b = o[0] + c[0], o[1] + c[1], o[2] + c[2]
            self.px[y][x] = (255 if r > 255 else r, 255 if g > 255 else g,
                             255 if b > 255 else b)

    def fade(self, f):
        k = int(f * 256)
        self.px = [[((p[0] * k) >> 8, (p[1] * k) >> 8, (p[2] * k) >> 8) for p in row]
                   for row in self.px]

    def line(self, x0, y0, x1, y1, c):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for i in range(n + 1):
            t = i / float(n)
            self.add(int(x0 + (x1 - x0) * t), int(y0 + (y1 - y0) * t), c)

    def text(self, x, y, s, f):
        if not 0 <= y < self.h:
            return
        for i, ch in enumerate(s):
            if ch != " " and 0 <= x + i < self.w:
                self.txt[(x + i, y)] = (ch, f)

    def render(self):
        out = []
        w, prev, txt = self.w, self.prev, self.txt
        for y in range(self.h):
            top, bot = self.px[2 * y], self.px[2 * y + 1]
            cells = []
            ap = cells.append
            for x in range(w):
                ch = txt.get((x, y))
                if ch is not None:
                    c, f = ch
                    t_, b_ = top[x], bot[x]
                    ap((c, f, ((t_[0] + b_[0]) >> 1, (t_[1] + b_[1]) >> 1,
                               (t_[2] + b_[2]) >> 1)))
                else:
                    ap((HALF, top[x], bot[x]))
            prow = prev[y]
            if prow == cells:
                continue
            x = 0
            while x < w:
                if prow is not None and prow[x] == cells[x]:
                    x += 1
                    continue
                x0 = x
                while x < w:
                    if prow is not None and prow[x] == cells[x]:
                        break
                    x += 1
                seg = []
                lf = lb = None
                for c, f, b in cells[x0:x]:
                    if f != lf:
                        seg.append(fg(f))
                        lf = f
                    if b != lb:
                        seg.append(bg(b))
                        lb = b
                    seg.append(c)
                out.append("\033[%d;%dH%s" % (y + 1, x0 + 1, "".join(seg)))
            prev[y] = cells
        if out:
            out.append(RESET)
            sys.stdout.write("".join(out))
            sys.stdout.flush()


def nebula(cv, t, gain, pal):
    w, ph = cv.w, cv.ph
    A = [math.sin(x * 0.055 + t * 0.5) for x in range(w)]
    B = [math.sin(y * 0.085 - t * 0.4) for y in range(ph)]
    Cc = [math.sin(i * 0.04 + t * 0.25) for i in range(w + ph)]
    top = len(pal) - 1
    for y in range(ph):
        row, by = cv.px[y], B[y]
        for x in range(w):
            v = (A[x] + by + Cc[x + y] + 3.0) * 0.16667
            row[x] = pal[int(v * v * v * gain * top)]


def new_stars(n):
    return [[random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0.05, 1.0),
             -999, -999] for _ in range(n)]


def draw_stars(cv, stars, speed, dt, roll=0.0, tint=(150, 158, 255)):
    w, ph = cv.w, cv.ph
    cx, cy = w * 0.5, ph * 0.5
    sx, sy = w * 0.46, ph * 0.46
    if roll:
        cr, sr = math.cos(roll), math.sin(roll)
    for s in stars:
        s[2] -= speed * dt
        if s[2] <= 0.04:
            s[0] = random.uniform(-1, 1)
            s[1] = random.uniform(-1, 1)
            s[2] = 1.0
            s[3] = -999
            continue
        k = 1.0 / s[2]
        X, Y = s[0] * k * sx, s[1] * k * sy
        if roll:
            X, Y = X * cr - Y * sr, X * sr + Y * cr
        px, py = int(cx + X), int(cy + Y)
        if px < -4 or px > w + 3 or py < -4 or py > ph + 3:
            s[0] = random.uniform(-1, 1)
            s[1] = random.uniform(-1, 1)
            s[2] = 1.0
            s[3] = -999
            continue
        b = min(1.0, (1.0 - s[2]) * 1.35 + 0.15)
        col = (min(255, int(tint[0] * b + 105 * b * b)),
               min(255, int(tint[1] * b + 105 * b * b)),
               min(255, int(tint[2] * b + 105 * b * b)))
        if s[3] > -900:
            cv.line(s[3], s[4], px, py, col)
        else:
            cv.add(px, py, col)
        s[3], s[4] = px, py


_TC = {}


def torus_draw(cv, A, B, S, pal, cx=None, cy=None, bright=1.0):
    """Tore éclairé, z-buffer, spéculaire — hommage à donut.c."""
    if S < 4:
        return
    w, ph = cv.w, cv.ph
    cx = w / 2.0 if cx is None else cx
    cy = ph / 2.0 if cy is None else cy
    K2, R1, R2 = 7.0, 0.85, 1.9
    nth = int(6.2832 * R1 * S / K2 / 1.1) + 10
    nph = int(6.2832 * (R1 + R2) * S / K2 / 1.1) + 14
    tab = _TC.get((nth, nph))
    if tab is None:
        tab = ([(math.cos(6.2832 * i / nth), math.sin(6.2832 * i / nth))
                for i in range(nth)],
               [(math.cos(6.2832 * i / nph), math.sin(6.2832 * i / nph))
                for i in range(nph)])
        _TC[(nth, nph)] = tab
    TH, PH = tab
    cA, sA, cB, sB = math.cos(A), math.sin(A), math.cos(B), math.sin(B)
    zb = {}
    pxr = cv.px
    top = len(pal) - 1
    for ct, st in TH:
        rr = R2 + R1 * ct
        yy = R1 * st
        for cp, sp in PH:
            x = rr * cp
            z = -rr * sp
            y1 = yy * cA - z * sA
            zz = K2 + yy * sA + z * cA
            k = S / zz
            px_ = int(cx + (x * cB - y1 * sB) * k)
            py_ = int(cy - (x * sB + y1 * cB) * k)
            if 1 <= px_ < w - 1 and 1 <= py_ < ph - 1:
                ooz = 1.0 / zz
                nx, ny, nz = ct * cp, st, -ct * sp
                ny1 = ny * cA - nz * sA
                nz1 = ny * sA + nz * cA
                L = -nz1 * 0.62 + (nx * sB + ny1 * cB) * 0.55 + (nx * cB - ny1 * sB) * 0.35
                tt = (L + 0.25) * 0.85
                if tt < 0.0:
                    tt = 0.0
                elif tt > 1.0:
                    tt = 1.0
                d = 0.6 + 3.6 * (ooz - 0.14)
                if d < 1.0:
                    tt *= d
                tt *= bright
                if tt > 1.0:
                    tt = 1.0
                c = pal[int(tt * top)]
                if tt > 0.72:
                    g = int((tt - 0.72) * 300)
                    c = (min(255, c[0] + g), min(255, c[1] + g), min(255, c[2] + g))
                for oy in (0, 1):
                    ry = py_ + oy
                    for ox in (0, 1):
                        key = ry * w + px_ + ox
                        if ooz > zb.get(key, 0.0):
                            zb[key] = ooz
                            pxr[ry][px_ + ox] = c


# ══════════════════════════════════════════════════════════════════════
#  5 · L'INTRO CINÉMATIQUE — 7 ACTES EN BLURPLE
# ══════════════════════════════════════════════════════════════════════

def act_crt(cv):
    """1 — allumage cathodique : point, ligne, ouverture sur la nébuleuse."""
    w, ph = cv.w, cv.ph
    sys.stdout.write(HOME + CLR)
    sys.stdout.flush()
    time.sleep(0.8)
    for _ in range(2):                                   # le point s'allume
        skip_check()
        c = Cv(w, cv.h)
        c.put(w // 2, ph // 2, (190, 196, 255))
        c.render()
        time.sleep(0.14)
        Cv(w, cv.h).render()
        time.sleep(0.12)
    for k in range(10):                                  # point → ligne
        skip_check()
        c = Cv(w, cv.h)
        half = max(1, int((k / 9.0) * w * 0.49))
        col = mix((110, 120, 250), (240, 244, 255), k / 9.0)
        for x in range(w // 2 - half, w // 2 + half):
            c.put(x, ph // 2, col)
            c.put(x, ph // 2 + 1, col)
        c.render()
        time.sleep(0.028)
    bg = Cv(w, cv.h)                                     # ligne → écran
    nebula(bg, 1.6, 0.55, R_BLURPLE)
    step = max(1, ph // 14)
    k = 2
    while k < ph // 2 + 2:
        skip_check()
        c = Cv(w, cv.h)
        y0, y1 = max(0, ph // 2 - k), min(ph, ph // 2 + k)
        for y in range(y0, y1):
            c.px[y] = bg.px[y]
        for y in (y0, y1 - 1):
            if 0 <= y < ph:
                c.px[y] = [mix(p, (240, 244, 255), 0.8) for p in bg.px[y]]
        c.render()
        time.sleep(0.024)
        k += step
    time.sleep(0.2)
    bg.render()
    time.sleep(0.45)


def act_post():
    """2 — BIOS : lignes de statut + barre qui cale à 99 % (signature)."""
    sys.stdout.write(HOME + CLR)
    sys.stdout.flush()
    sys.stdout.write("\033[2;3H" + fg((150, 155, 185))
                     + "DISCORDUTILITY BIOS v%s — séquence d'amorçage" % VERSION
                     + RESET + "\r\n\r\n")
    sys.stdout.flush()
    rows = [("module graphique", "EN LIGNE"),
            ("moteur réseau", "OK"),
            ("clavier temps réel", "ARMÉ"),
            ("palette blurple", "CALIBRÉE"),
            ("token vault", "VIDE — en attente"),
            ("sécurité", "introuvable — ignorée")]
    for name, st in rows:
        skip_check()
        col = YELLOW if ("introuvable" in st or "VIDE" in st) else GREEN
        sys.stdout.write("  " + fg(BLURPLE_L) + "◆" + RESET + " " + fg(TXT)
                         + "%-20s" % name + RESET + fg(FAINT) + "······" + RESET
                         + " " + fg(col) + st + RESET + "\r\n")
        sys.stdout.flush()
        time.sleep(random.uniform(0.1, 0.24))
    sys.stdout.write("\r\n")
    sys.stdout.flush()
    time.sleep(0.2)
    n = 40
    for i in range(n + 1):
        skip_check()
        bar = "".join(bg(palv(R_BLURPLE, 0.25 + 0.7 * j / n)) + " " for j in range(i))
        line_at("  " + bar + bg((24, 26, 40)) + " " * (n - i) + RESET
                + fg(TXT) + " %3d %%" % (i * 100 // n) + RESET)
        time.sleep(0.022)
    for msg in ("…le token frétille.", "…discord hésite.", "…marché conclu."):
        skip_check()
        bar = "".join(bg(palv(R_BLURPLE, 0.25 + 0.7 * j / n)) + " " for j in range(n))
        line_at("  " + bar + RESET + fg(TXT) + "  99 %  " + RESET
                + fg(MUT) + msg + RESET)
        time.sleep(0.3)
    bar = "".join(bg(palv(R_BLURPLE, 0.3 + 0.7 * j / n)) + " " for j in range(n))
    line_at("  " + bar + RESET + BOLD + fg(GREEN) + " 100 %  SESSION PRÊTE" + RESET)
    time.sleep(0.55)


def act_static(cv, frames=6):
    """3 — panne de signal : quelques frames de garbage plein écran."""
    w, h = cv.w, cv.h
    for _ in range(frames):
        skip_check()
        c = Cv(w, h)
        for y in range(h):
            s = "".join(random.choice(GARB) for _ in range(w))
            c.text(0, y, s,
                   random.choice((WHITE, BLURPLE_L, (110, 118, 200), (70, 74, 110))))
        c.render()
        time.sleep(0.05)
    Cv(w, h).render()
    time.sleep(0.3)


def act_warp(cv, dur=2.6):
    """4 — hyperespace blurple : accélération exponentielle + roulis."""
    stars = new_stars(230)
    clock = Clock(20)
    t = 0.0
    while t < dur:
        dt = clock.tick()
        t += dt
        skip_check()
        p = t / dur
        cv.fade(0.6)
        draw_stars(cv, stars, 0.25 + (p ** 3) * 9.0, dt,
                   roll=0.85 * math.sin(t * 1.25), tint=(150, 158, 255))
        cv.render()
    for k in (1.0, 0.6, 0.3):                            # flash de sortie
        cv.clear((int(240 * k), int(244 * k), int(255 * k)))
        cv.render()
        time.sleep(0.045)
    cv.clear()
    cv.render()


def act_core(cv, dur=2.9):
    """5 — le noyau : tore 3D blurple qui se condense, puis anneaux."""
    clock = Clock(18)
    t = 0.0
    A = B = 0.0
    Smax = min(cv.w * 0.5, cv.ph * 0.5) * 0.85
    while t < dur:
        dt = clock.tick()
        t += dt
        skip_check()
        A += dt * 1.15
        B += dt * 0.72
        cv.clear()
        nebula(cv, t, 0.35, R_BLURPLE)
        grow = min(1.0, t / 0.7)
        torus_draw(cv, A, B, Smax * (0.55 + 0.45 * grow), R_BLURPLE,
                   bright=0.2 + 0.8 * grow)
        if t < dur - 0.9:
            cap, col = "CONNEXION AU NOYAU…", TXT
        else:
            cap, col = "NOYAU STABILISÉ", GREEN
        cv.text((cv.w - len(cap)) // 2, 1, cap, col)
        cv.text(2, 0, " une touche : passer ", (80, 85, 110))
        cv.render()
    cx, cy = cv.w / 2.0, cv.ph / 2.0                     # anneaux de confirmation
    for r in range(3, int(max(cv.w, cv.ph) * 0.55), 4):
        skip_check()
        cv.fade(0.86)
        for i in range(80):
            a = i * 0.0785
            cv.add(int(cx + math.cos(a) * r), int(cy + math.sin(a) * r * 0.55),
                   mix(BLURPLE_L, WHITE, 0.4))
        cv.render()
        time.sleep(0.02)
    cv.clear((225, 232, 255))
    cv.render()
    time.sleep(0.06)
    cv.clear()


def act_banner(cv):
    """6 — la bannière se décode en glitch, puis balayage lumineux."""
    lines = banner_lines()
    colors = banner_colors(len(lines))
    maxw = max(len(l) for l in lines)
    if cv.w < maxw + 2:                                  # terminal étroit
        lines = ["D I S C O R D U T I L I T Y"]
        colors = [BLURPLE_L]
        maxw = len(lines[0])
    x0 = max(1, (cv.w - maxw) // 2)
    y0 = max(2, (cv.ph - len(lines)) // 2 - 3)
    speeds = [random.uniform(0.5, 0.9) for _ in lines]
    clock = Clock(20)
    t = 0.0
    while True:                                          # décodage glitch
        dt = clock.tick()
        t += dt
        skip_check()
        cv.clear()
        nebula(cv, t * 0.5, 0.2, R_BLURPLE)
        cv.text(2, 0, " une touche : passer ", (80, 85, 110))
        done = True
        for i, l in enumerate(lines):
            front = int(len(l) * min(1.0, t * speeds[i]))
            if front < len(l):
                done = False
            if front:
                cv.text(x0, y0 + i, l[:front], colors[i])
            tail = "".join(random.choice(GARB) if ch != " " else " "
                           for ch in l[front:front + 7])
            if tail:
                cv.text(x0 + front, y0 + i, tail, mix(colors[i], WHITE, 0.55))
        cv.render()
        if done:
            break
    time.sleep(0.2)
    sx = -14                                             # balayage lumineux
    while sx < maxw + 14:
        clock.tick()
        skip_check()
        cv.clear()
        nebula(cv, 3.0 + sx * 0.01, 0.3, R_BLURPLE)
        cv.text(2, 0, " une touche : passer ", (80, 85, 110))
        for i, l in enumerate(lines):
            for j, ch in enumerate(l):
                if ch != " ":
                    c = colors[i]
                    d = abs(j - sx)
                    if d < 9:
                        c = mix(c, (255, 255, 255), (1 - d / 9.0) * 0.85)
                    cv.txt[(x0 + j, y0 + i)] = (ch, c)
        cv.render()
        sx += 4.5
    sub = "v%s · ÉDITION REMASTERISÉE" % VERSION         # sous-titre tapé
    sx0 = max(1, (cv.w - len(sub)) // 2)
    sy = y0 + len(lines) + 1
    for k in range(len(sub) + 1):
        skip_check()
        cv.clear()
        nebula(cv, 5.0, 0.26, R_BLURPLE)
        for i, l in enumerate(lines):
            cv.text(x0, y0 + i, l, colors[i])
        cv.text(sx0, sy, sub[:k], MUT)
        cv.render()
        time.sleep(0.03)
    time.sleep(0.55)


def act_checks(cv):
    """7 — checks de modules avec barres animées."""
    mods = [("INTERFACE", "rendu · menus · tableaux"),
            ("RÉSEAU", "api discord v9"),
            ("MESSAGERIE", "dm · campagnes"),
            ("STYLE", "blurple authentique")]
    clock = Clock(20)
    bw = 26
    x0 = 8
    y0 = max(3, (cv.h - len(mods) * 2) // 2)
    for mi, (name, desc) in enumerate(mods):
        prog = 0.0
        while True:
            clock.tick()
            skip_check()
            prog += 0.05 * random.uniform(1.4, 2.2)
            if prog >= 1.0:
                prog = 1.0
            cv.clear()
            nebula(cv, 8.0 + mi, 0.16, R_BLURPLE)
            cv.text(2, 0, " une touche : passer ", (80, 85, 110))
            for j, (n2, d2) in enumerate(mods):
                y = y0 + j * 2
                cv.text(x0, y, "%-10s" % n2,
                        WHITE if j == mi else (TXT if j < mi else FAINT))
                for i in range(bw):
                    gx = x0 + 12 + i
                    if j < mi or (j == mi and prog >= 1.0):
                        c = palv(R_BLURPLE, 0.3 + 0.6 * i / bw)
                    elif j == mi and i < int(bw * prog):
                        c = palv(R_BLURPLE, 0.3 + 0.6 * i / bw)
                    else:
                        c = (26, 28, 44)
                    cv.px[y * 2][gx] = c
                    cv.px[y * 2 + 1][gx] = c
                if j < mi or prog >= 1.0:
                    cv.text(x0 + 14 + bw, y, "✓ PRÊT", GREEN)
                elif j == mi:
                    cv.text(x0 + 14 + bw, y, "%3d %%" % int(prog * 100), MUT)
                cv.text(x0 + 12, y + 1, d2, FAINT if j > mi else MUT)
            cv.render()
            if prog >= 1.0:
                break
        time.sleep(0.08)
    time.sleep(0.35)


WFONT = {
    "B": (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    "I": (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "E": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    "N": (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    "V": (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    "U": (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
}


def welcome_pts(msg, sc):
    pts = []
    x = 0
    for ch in msg:
        g = WFONT.get(ch)
        if g:
            for r, bits in enumerate(g):
                for c in range(5):
                    if bits >> (4 - c) & 1:
                        for dy in range(sc):
                            for dx in range(sc):
                                pts.append((x + c * sc + dx, r * sc + dy))
        x += 6 * sc
    return pts, x - sc, 7 * sc


def act_welcome(cv):
    """8 — BIENVENUE en pixel-art ondulant + invite clignotante."""
    msg = "BIENVENUE"
    sc = 2 if cv.w >= 118 else 1
    pts, lw, lh = welcome_pts(msg, sc)
    ox = (cv.w - lw) // 2
    oy = max(2, (cv.ph - lh) // 2 - 2)
    prompt = "APPUYEZ SUR UNE TOUCHE POUR ENTRER"
    px_ = max(1, (cv.w - len(prompt)) // 2)
    py = oy + lh + 3
    clock = Clock(18)
    t = 0.0
    while True:
        dt = clock.tick()
        t += dt
        if KB.pressed():
            KB.read()
            return
        cv.clear()
        nebula(cv, t, 0.35, R_BLURPLE)
        for (x, y) in pts:
            v = 0.45 + 0.5 * (0.5 + 0.5 * math.sin(t * 5.0 - x * 0.22))
            cv.put(ox + x, oy + y, palv(R_BLURPLE, v))
        if t % 0.9 < 0.55:
            cv.text(px_, py, prompt, BLURPLE_L)
        cv.text(2, 0, " chargement terminé — en attente ", (80, 85, 110))
        cv.render()


def intro_cinematic():
    sys.stdout.write(CUR_OFF)
    KB.start()
    try:
        w, h = term_size()
        cv = Cv(w, h)
        act_crt(cv)
        act_post()
        act_static(cv)
        act_warp(cv)
        act_core(cv)
        act_banner(cv)
        act_checks(cv)
        act_welcome(cv)
    except SkipIntro:
        pass
    finally:
        KB.stop()
        sys.stdout.write(HOME + CLR + CUR_ON)
        sys.stdout.flush()


def crt_close():
    """Extinction cathodique : flash, fermeture verticale, ligne, point."""
    sys.stdout.write(CUR_OFF)
    w, h = term_size()
    ph = h * 2
    cv = Cv(w, h)
    cv.clear((235, 240, 255))
    cv.render()
    time.sleep(0.05)
    k = ph // 2
    while k > 1:
        c = Cv(w, h)
        y0, y1 = max(0, ph // 2 - k), min(ph, ph // 2 + k)
        for y in range(y0, y1):
            c.px[y] = [(20, 22, 35)] * w
        for y in (y0, y1 - 1):
            if 0 <= y < ph:
                c.px[y] = [(180, 190, 255)] * w
        c.render()
        time.sleep(0.02)
        k = max(1, int(k * 0.7))
    half = w // 2
    while half > 0:
        c = Cv(w, h)
        for x in range(max(0, w // 2 - half), min(w, w // 2 + half)):
            c.put(x, ph // 2, (240, 244, 255))
            c.put(x, ph // 2 + 1, (240, 244, 255))
        c.render()
        time.sleep(0.03)
        half -= max(2, w // 24)
    Cv(w, h).render()
    time.sleep(0.35)
    sys.stdout.write(CUR_ON)
    sys.stdout.flush()


# ══════════════════════════════════════════════════════════════════════
#  6 · WIDGETS UI (menus, saisies, panneaux, spinner)
# ══════════════════════════════════════════════════════════════════════

def menu_block(title, items, sel, width):
    w = max(28, min(width, 68))
    if w < len(title) + 7:
        w = len(title) + 7
    inner = w - 2
    Lw = min(22, max(len(l) for l, _ in items))
    lines = ["  " + fg(BLURPLE) + "╭─ " + BOLD + title + RESET + fg(BLURPLE)
             + " " + "─" * max(2, w - len(title) - 5) + "╮" + RESET]
    for i, (label, desc) in enumerate(items):
        lab = label[:Lw]
        desc = desc or ""
        budget = inner - 9 - Lw
        if len(desc) > budget:
            desc = desc[:max(0, budget - 1)] + "…" if budget > 1 else ""
        if i == sel:
            body = "▶ %d  %s  %s" % (i + 1, lab, desc)
            pad = " " * max(0, inner - 3 - len(body))
            row = "│" + bg(BLURPLE) + BOLD + fg(WHITE) + " " + body + pad + RESET \
                  + fg(BLURPLE) + "│"
        else:
            pad = " " * max(0, inner - 3 - (1 + 2 * 2 + Lw + 2 + len(desc)))
            row = "│  " + fg(BLURPLE_L) + "%d" % (i + 1) + RESET + "  " + fg(TXT) \
                  + lab + RESET + "  " + fg(MUT) + desc + RESET + pad + fg(BLURPLE) + "│"
        lines.append("  " + fg(BLURPLE) + row + RESET)
    lines.append("  " + fg(BLURPLE) + "╰" + "─" * (w - 2) + "╯" + RESET)
    return lines


def select(title, items, pre=None, footer=None):
    """Menu à flèches → index choisi, ou None si annulé."""
    KB.start()
    sys.stdout.write(CUR_OFF)
    frame = Frame()
    sel = 0
    try:
        last = 0.0
        while True:
            now = time.time()
            if last == 0.0 or now - last >= 1.0:
                lines = []
                if pre:
                    lines += pre() if callable(pre) else pre
                lines += menu_block(title, items, sel, term_size()[0] - 6)
                lines.append("")
                lines.append("  " + fg(FAINT) + (footer or
                            "↑↓ naviguer · entrée valider · 1-%d direct · q retour"
                            % len(items)) + RESET)
                frame.draw(lines)
                last = now
            if not KB.pressed():
                time.sleep(0.05)
                continue
            k = KB.read()
            last = 0.0
            if k == "up":
                sel = (sel - 1) % len(items)
            elif k == "down":
                sel = (sel + 1) % len(items)
            elif k in ("enter", " "):
                return sel
            elif k in ("q", "esc", "b"):
                return None
            elif k.isdigit() and 1 <= int(k) <= len(items):
                return int(k) - 1
    finally:
        KB.stop()
        sys.stdout.write(CUR_ON + "\r\n")
        sys.stdout.flush()


def ask(prompt, default=None, hidden=False):
    KB.stop()
    sys.stdout.write(CUR_ON)
    tail = " " + fg(FAINT) + "[%s]" % default + RESET if default is not None else ""
    sys.stdout.write("\r\n  " + fg(BLURPLE_L) + "◆" + RESET + " " + prompt + tail + "\r\n")
    sys.stdout.flush()
    if hidden:
        try:
            v = getpass.getpass("")
        except Exception:
            v = input()
    else:
        try:
            v = input("  " + fg(BLURPLE) + "»" + RESET + " ")
        except EOFError:
            v = ""
    v = v.strip()
    if not v and default is not None:
        return str(default)
    return v


def confirm(msg, danger=False):
    KB.stop()
    sys.stdout.write(CUR_ON)
    col = RED if danger else BLURPLE
    try:
        v = input("  " + fg(col) + BOLD + msg + RESET + " "
                  + fg(YELLOW) + "[o/N] " + RESET).strip().lower()
    except EOFError:
        v = ""
    return v in ("o", "oui", "y", "yes")


def wait_key(msg="  [entrée] pour continuer"):
    print(fg(FAINT) + msg + RESET)
    KB.start()
    try:
        while not KB.pressed():
            time.sleep(0.03)
        KB.read()
    finally:
        KB.stop()


def note(msg, color=YELLOW):
    print("  " + fg(color) + msg + RESET)


def run_task(label, fn, *args, **kwargs):
    """fn dans un thread pendant qu'un spinner tourne → (ok, valeur)."""
    res = {}
    done = [False]

    def _work():
        try:
            res["v"] = fn(*args, **kwargs)
        except BaseException as e:
            res["e"] = e
        done[0] = True

    threading.Thread(target=_work, daemon=True).start()
    fr = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    i = 0
    while not done[0]:
        line_at("  " + fg(BLURPLE) + fr[i % 10] + RESET + "  " + fg(TXT) + label
                + fg(FAINT) + "…" + RESET)
        i += 1
        time.sleep(0.07)
    if "e" in res:
        line_at("  " + fg(RED) + "✗" + RESET + "  " + label + fg(FAINT)
                + "  —  %s" % res["e"] + RESET)
        print()
        return False, res["e"]
    line_at("  " + fg(GREEN) + "✓" + RESET + "  " + label)
    print()
    return True, res.get("v")


def panel(title, rows, width=64, accent=BLURPLE):
    w = term_size()[0]
    bw = max(36, min(width, w - 4))
    lab_w = 14
    val_max = bw - 18
    print()
    print("  " + fg(accent) + "╭─ " + BOLD + title + RESET + fg(accent) + " "
          + "─" * max(2, bw - len(title) - 5) + "╮" + RESET)
    for row in rows:
        if isinstance(row, tuple):
            label, value, color = row
        else:
            label, value, color = "", row, MUT
        chunks = wrap(value, val_max)
        first = True
        for chunk in chunks:
            lpart = (label if first else "").ljust(lab_w)
            print("  " + fg(accent) + "│ " + RESET + fg(MUT) + lpart + RESET + " "
                  + fg(color) + chunk + RESET + " " * (val_max - len(chunk))
                  + fg(accent) + "│" + RESET)
            first = False
    print("  " + fg(accent) + "╰" + "─" * (bw - 2) + "╯" + RESET)


# ══════════════════════════════════════════════════════════════════════
#  7 · COUCHE API — logique d'origine conservée
# ══════════════════════════════════════════════════════════════════════

def get_own_user(token):
    try:
        r = requests.get("https://discord.com/api/v9/users/@me",
                         headers={"Authorization": token, "User-Agent": UA}, timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def get_guilds(token):
    try:
        r = requests.get("https://discord.com/api/v9/users/@me/guilds",
                         headers={"Authorization": token, "User-Agent": UA}, timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def leave_guild(token, guild_id):
    try:
        r = requests.delete("https://discord.com/api/v9/users/@me/guilds/%s" % guild_id,
                            headers={"Authorization": token, "User-Agent": UA}, timeout=10)
        return r.status_code == 204
    except Exception:
        return False


def fetch_relationships(token):
    url = "https://discord.com/api/v9/users/@me/relationships"
    try:
        r = requests.get(url, headers={"Authorization": token, "User-Agent": UA},
                         timeout=10)
    except Exception as e:
        return None, "erreur réseau : %s" % e
    if r.status_code == 200:
        return r.json(), None
    if r.status_code == 401:
        return None, "token invalide ou expiré"
    if r.status_code == 429:
        return None, "rate limit — attendez %s s" % r.headers.get("Retry-After", "?")
    return None, "erreur %d : %s" % (r.status_code, r.text[:120])


def get_friends_list(token):
    data, err = fetch_relationships(token)
    if data is None:
        return None, err
    return [rel for rel in data if rel.get("type") == 1], None


def format_date(date_iso, date_only=False):
    if not date_iso:
        return "Unknown date"
    try:
        dt = datetime.datetime.fromisoformat(date_iso.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y") if date_only else dt.strftime("%d/%m/%Y at %H:%M")
    except Exception:
        return date_iso


def search_friends(friends, query):
    query = query.lower()
    return [rel for rel in friends
            if query in (rel.get("user", {}).get("username") or "").lower()
            or query in (rel.get("user", {}).get("global_name") or "").lower()]


def send_dm(token, user_id, content, file_path=None):
    headers = {"Authorization": token, "User-Agent": UA}
    try:
        r = requests.post("https://discord.com/api/v9/users/@me/channels",
                          headers=headers, json={"recipient_id": user_id}, timeout=10)
        if r.status_code not in (200, 201):
            return False
        channel_id = r.json()["id"]
        url = "https://discord.com/api/v9/channels/%s/messages" % channel_id
        if file_path and os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                r2 = requests.post(url, headers=headers,
                                   data={"content": content}, files={"file": f},
                                   timeout=30)
        else:
            r2 = requests.post(url, headers={**headers,
                                            "Content-Type": "application/json"},
                               json={"content": content}, timeout=10)
        return r2.status_code == 200
    except Exception:
        return False


# ══════════════════════════════════════════════════════════════════════
#  8 · ÉCRANS PARTAGÉS
# ══════════════════════════════════════════════════════════════════════

def header_lines(state=None, section=None):
    w, h = term_size()
    lines = []
    bl = banner_lines()
    bw = max(len(l) for l in bl)
    if w >= bw + 2 and h >= len(bl) + 15:
        for l, c in zip(bl, banner_colors(len(bl))):
            lines.append(fg(c) + l + RESET)
        lines.append("")
    else:
        lines.append("  " + fg(BLURPLE) + BOLD + "D I S C O R D U T I L I T Y"
                     + RESET + fg(FAINT) + "   v" + VERSION + RESET)
        lines.append("")
    if state:
        u = state.get("user") or {}
        now = datetime.datetime.now().strftime("%H:%M:%S")
        info = ("  " + fg(BLURPLE_L) + BOLD + "◈ @" + (u.get("username") or "?") + RESET
                + fg(FAINT) + "  ·  " + RESET + fg(TXT)
                + "%d ami(s)" % len(state.get("friends") or []) + RESET
                + fg(FAINT) + "  ·  " + now + RESET)
        if section:
            info += fg(FAINT) + "  ·  " + RESET + fg(MUT) + section + RESET
        lines.append(info)
        lines.append("")
    elif section:
        lines.append("  " + fg(MUT) + "— " + section + " —" + RESET)
        lines.append("")
    return lines


def warning_screen():
    sys.stdout.write(HOME + CLR)
    w = term_size()[0]
    bw = min(w - 4, 72)

    def cline(s):
        print("  " + fg(RED) + "║" + RESET + fg(TXT)
              + s.center(bw - 2)[:bw - 2] + RESET + fg(RED) + "║" + RESET)

    print()
    print("  " + fg(RED) + "╔" + "═" * (bw - 2) + "╗" + RESET)
    cline("")
    print("  " + fg(RED) + "║" + RESET + fg(RED) + BOLD
          + "⚠  A V E R T I S S E M E N T".center(bw - 2)[:bw - 2] + RESET
          + fg(RED) + "║" + RESET)
    cline("")
    for txt in ("Cet outil interroge des endpoints privés de Discord",
                "avec votre token utilisateur.",
                "",
                "L'automatisation d'un compte utilisateur viole les conditions",
                "d'utilisation de Discord et peut entraîner la suspension",
                "définitive de votre compte.",
                "",
                "Aucune donnée n'est stockée ni transmise à un tiers —",
                "tout se passe entre vous et l'API Discord.",
                "",
                "Vous l'utilisez sous votre seule responsabilité."):
        cline(txt)
    print("  " + fg(RED) + "╚" + "═" * (bw - 2) + "╝" + RESET)
    print()
    wait_key("  " + fg(FAINT) + "[entrée] continuer  ·  [ctrl+c] abandonner" + RESET)


def login():
    for attempt in range(3):
        sys.stdout.write(HOME + CLR)
        print()
        print("  " + fg(BLURPLE) + BOLD + "CONNEXION" + RESET)
        print("  " + fg(FAINT) + "─" * 34 + RESET)
        print()
        print("  " + fg(TXT) + "Collez votre token utilisateur Discord." + RESET)
        print("  " + fg(FAINT) + "(saisie masquée — collez au clic droit ou Ctrl+Shift+V)"
              + RESET)
        token = ask("Token", hidden=True)
        if not token:
            note("Token requis.", RED)
            time.sleep(1.2)
            continue
        if len(token) < 40:
            note("Ce token semble court — vérifiez le collage.", YELLOW)
            if not confirm("Continuer quand même ?"):
                continue
        print()
        run_task("négociation de la session", time.sleep, 0.55)
        ok, user = run_task("récupération de l'identité", get_own_user, token)
        if not (ok and user):
            note("Token invalide ou expiré.", RED)
            note("Tentative %d/3." % (attempt + 1), MUT)
            wait_key()
            continue
        print("      " + fg(FAINT) + "→ @%s · ID %s"
              % (user.get("username"), user.get("id")) + RESET)
        ok, val = run_task("chargement des relations", get_friends_list, token)
        friends, err = val
        if friends is None:
            note("Échec : %s" % (err or "erreur inconnue"), RED)
            wait_key()
            continue
        print("      " + fg(FAINT) + "→ %d relation(s) d'amitié" % len(friends) + RESET)
        time.sleep(0.4)

        sys.stdout.write(HOME + CLR)
        for l in header_lines({"user": user, "friends": friends}):
            print(l)
        panel("SESSION OUVERTE", [
            ("Connecté", "@" + user.get("username", "?"), GREEN),
            ("ID", user.get("id", "?"), TXT),
            ("Amis", str(len(friends)), TXT),
        ])
        type_out("Bienvenue, @%s." % user.get("username", "?"), TXT, 0.03)
        wait_key()
        return {"token": token, "user": user, "friends": friends}
    return None


# ══════════════════════════════════════════════════════════════════════
#  9 · NAVIGATEURS DE LISTES
# ══════════════════════════════════════════════════════════════════════

def show_friend_detail(rel):
    user = rel.get("user", {})
    uid = user.get("id", "?")
    av = user.get("avatar")
    avu = ("https://cdn.discordapp.com/avatars/%s/%s.png" % (uid, av)
           if av else "aucun (avatar par défaut)")
    sys.stdout.write(HOME + CLR)
    for l in header_lines(section="fiche ami"):
        print(l)
    panel("FICHE AMI", [
        ("Utilisateur", "@" + (user.get("username") or "?"), TXT),
        ("Affiché", user.get("global_name") or "—", TXT),
        ("ID", uid, TXT),
        ("Amis depuis", format_date(rel.get("since")), TXT),
        ("Avatar", avu, MUT),
        ("Statut", "indisponible via REST (gateway requise)", MUT),
    ])
    wait_key()


def browse_friends(friends, mode="browse", title="AMIS"):
    if not friends:
        note("Aucun ami à afficher.", YELLOW)
        wait_key()
        return None
    KB.start()
    sys.stdout.write(CUR_OFF)
    frame = Frame()
    cur = 0
    try:
        while True:
            w, h = term_size()
            per = max(3, min(10, h - 13))
            pages = (len(friends) + per - 1) // per
            page = cur // per
            date_w = 12
            uname_w = max(8, min(16, w - 30))
            disp_w = max(0, min(18, w - 24 - uname_w - date_w))
            lines = []
            t = title + (" — CHOISIR" if mode == "pick" else "")
            lines.append("  " + fg(BLURPLE) + BOLD + t + RESET + fg(FAINT)
                         + "   ·   %d ami(s)   ·   page %d/%d"
                         % (len(friends), page + 1, pages) + RESET)
            lines.append("")
            hdr = "  " + fg(FAINT) + "#   " + "@username".ljust(uname_w)
            if disp_w >= 8:
                hdr += "nom affiché".ljust(disp_w)
            hdr += "ajouté le" + RESET
            lines.append(hdr)
            lines.append("  " + fg(FAINT) + "─" * min(w - 2, 6 + uname_w + disp_w
                                                     + date_w) + RESET)
            for r in range(per):
                gi = page * per + r
                if gi >= len(friends):
                    break
                rel = friends[gi]
                user = rel.get("user", {})
                uname = tr("@" + (user.get("username") or "?"), uname_w)
                d = tr(format_date(rel.get("since"), date_only=True), date_w)
                body = "%-4d%s" % (gi + 1, uname.ljust(uname_w))
                if disp_w >= 8:
                    body += tr(user.get("global_name") or "—", disp_w).ljust(disp_w)
                body += d
                if gi == cur:
                    pad = " " * max(1, (w - 3) - len(body))
                    lines.append("  " + bg(BLURPLE) + fg(WHITE) + BOLD + "▶ "
                                 + body + pad + RESET)
                else:
                    seg = ("  " + fg(BLURPLE_L) + "%-4d" % (gi + 1) + RESET
                           + fg(TXT) + uname.ljust(uname_w) + RESET)
                    if disp_w >= 8:
                        seg += fg(MUT) + tr(user.get("global_name") or "—",
                                            disp_w).ljust(disp_w) + RESET
                    seg += fg(FAINT) + d + RESET
                    lines.append("  " + seg)
            lines.append("")
            foot = ("↑↓ choisir · ←→ page · entrée valider · q annuler"
                    if mode == "pick" else
                    "↑↓ défiler · ←→ page · entrée détails · q retour")
            lines.append("  " + fg(FAINT) + foot + RESET)
            frame.draw(lines)
            k = KB.read()
            if k == "up":
                cur = (cur - 1) % len(friends)
            elif k == "down":
                cur = (cur + 1) % len(friends)
            elif k == "right":
                cur = min(len(friends) - 1, (page + 1) * per)
            elif k == "left":
                cur = max(0, (page - 1) * per)
            elif k in ("enter", " "):
                if mode == "pick":
                    return cur
                show_friend_detail(friends[cur])
                frame = Frame()
            elif k in ("q", "esc", "b"):
                return None
    finally:
        KB.stop()
        sys.stdout.write(CUR_ON + "\r\n")
        sys.stdout.flush()


def browse_guilds(guilds, pick=False):
    if not guilds:
        return None
    KB.start()
    sys.stdout.write(CUR_OFF)
    frame = Frame()
    cur = 0
    try:
        while True:
            w, h = term_size()
            per = max(3, min(10, h - 11))
            pages = (len(guilds) + per - 1) // per
            page = cur // per
            id_w = 19 if w >= 64 else 0
            name_w = max(8, min(24, w - 14 - id_w))
            lines = []
            t = "SERVEURS — %d" % len(guilds) + (" — CHOISIR" if pick else "")
            lines.append("  " + fg(BLURPLE) + BOLD + t + RESET + fg(FAINT)
                         + "   ·   page %d/%d" % (page + 1, pages) + RESET)
            lines.append("")
            hdr = "  " + fg(FAINT) + "#   " + "nom".ljust(name_w)
            if id_w:
                hdr += "ID".ljust(id_w)
            hdr += "rôle" + RESET
            lines.append(hdr)
            lines.append("  " + fg(FAINT) + "─" * min(w - 2, 8 + name_w + id_w + 8)
                         + RESET)
            for r in range(per):
                gi = page * per + r
                if gi >= len(guilds):
                    break
                g = guilds[gi]
                owner = g.get("owner", False)
                body = "%-4d%s" % (gi + 1, tr(g.get("name", "?"), name_w)
                                   .ljust(name_w))
                if id_w:
                    body += str(g.get("id", "?")).ljust(id_w)
                body += "★ créa" if owner else "membre"
                if gi == cur:
                    pad = " " * max(1, (w - 3) - len(body))
                    lines.append("  " + bg(BLURPLE) + fg(WHITE) + BOLD + "▶ "
                                 + body + pad + RESET)
                else:
                    seg = ("  " + fg(BLURPLE_L) + "%-4d" % (gi + 1) + RESET
                           + fg(TXT) + tr(g.get("name", "?"), name_w)
                           .ljust(name_w) + RESET)
                    if id_w:
                        seg += fg(MUT) + str(g.get("id", "?")).ljust(id_w) + RESET
                    seg += (fg(YELLOW) + "★ créa" if owner else fg(MUT) + "membre") + RESET
                    lines.append("  " + seg)
            lines.append("")
            foot = ("↑↓ choisir · ←→ page · entrée valider · q annuler" if pick
                    else "↑↓ défiler · ←→ page · entrée détails · q retour")
            lines.append("  " + fg(FAINT) + foot + RESET)
            frame.draw(lines)
            k = KB.read()
            if k == "up":
                cur = (cur - 1) % len(guilds)
            elif k == "down":
                cur = (cur + 1) % len(guilds)
            elif k == "right":
                cur = min(len(guilds) - 1, (page + 1) * per)
            elif k == "left":
                cur = max(0, (page - 1) * per)
            elif k in ("enter", " "):
                if pick:
                    return cur
                sys.stdout.write(HOME + CLR)
                for l in header_lines(section="serveurs"):
                    print(l)
                g = guilds[cur]
                panel("SERVEUR", [
                    ("Nom", g.get("name", "?"), TXT),
                    ("ID", str(g.get("id", "?")), TXT),
                    ("Rôle", "★ créateur" if g.get("owner") else "membre", TXT),
                ])
                wait_key()
                frame = Frame()
            elif k in ("q", "esc", "b"):
                return None
    finally:
        KB.stop()
        sys.stdout.write(CUR_ON + "\r\n")
        sys.stdout.flush()


# ══════════════════════════════════════════════════════════════════════
# 10 · MESSAGERIE
# ══════════════════════════════════════════════════════════════════════

def ask_attachment():
    while True:
        p = ask("Pièce jointe — chemin du fichier (vide : aucune)")
        if not p:
            return None
        if os.path.isfile(p):
            note("Fichier : %s (%.1f Ko)"
                 % (os.path.basename(p), os.path.getsize(p) / 1024.0), GREEN)
            return p
        note("Fichier introuvable : " + tr(p, 40), RED)
        if confirm("Envoyer sans pièce jointe ?"):
            return None


def confirm_send(targets, msg, file_path):
    sys.stdout.write(HOME + CLR)
    for l in header_lines(section="confirmation"):
        print(l)
    names = ["@" + n for _, n in targets]
    panel("RÉCAPITULATIF", [
        ("Destinataires", "%d" % len(targets), TXT),
        ("Aperçu", ", ".join(tr(n, 18) for n in names[:5])
         + ("…" if len(names) > 5 else ""), MUT),
        ("Message", tr(msg, 70), TXT),
        ("Pièce jointe", os.path.basename(file_path) if file_path else "aucune", MUT),
    ])
    return confirm("Tout est bon — envoyer ?")


def campaign(state, targets, msg, file_path, delay):
    total = len(targets)
    ok = 0
    failed = []
    t0 = time.time()
    bar_w = min(26, max(10, term_size()[0] // 3))
    for i, (uid, name) in enumerate(targets, 1):
        fill = int(bar_w * i / total)
        bar = fg(BLURPLE) + "█" * fill + fg(FAINT) + "░" * (bar_w - fill) + RESET
        base = "  %s %3d%%  → @%s" % (bar, i * 100 // total, tr(name, 14))
        line_at(base + fg(FAINT) + "  envoi…" + RESET)
        if send_dm(state["token"], uid, msg, file_path):
            ok += 1
            line_at(base + fg(GREEN) + "  ✓" + RESET)
        else:
            failed.append(name)
            line_at(base + fg(RED) + "  ✗" + RESET)
        if i < total and delay > 0:
            rem = delay
            while rem > 0:
                line_at(base + fg(FAINT) + "  cooldown %.0fs" % rem + RESET)
                time.sleep(min(0.25, rem))
                rem -= 0.25
    print()
    panel("CAMPAGNE TERMINÉE", [
        ("Envoyés", "%d / %d" % (ok, total), GREEN if ok == total else YELLOW),
        ("Échecs", str(len(failed)), RED if failed else MUT),
        ("Durée", "%.0f s" % (time.time() - t0), TXT),
    ])
    if failed:
        note("Échecs : " + ", ".join("@" + tr(n, 16) for n in failed[:6])
             + ("…" if len(failed) > 6 else ""), RED)
    wait_key()


def dm_single(state):
    idx = browse_friends(state["friends"], mode="pick", title="DESTINATAIRE")
    if idx is None:
        return
    rel = state["friends"][idx]
    uid = rel["user"]["id"]
    name = rel["user"].get("username", "?")
    msg = ask("Message à envoyer")
    if not msg:
        note("Message vide — annulé.", YELLOW)
        wait_key()
        return
    file = ask_attachment()
    if not confirm_send([(uid, name)], msg, file):
        note("Envoi annulé.", MUT)
        return
    ok, _ = run_task("envoi du message → @%s" % name,
                     send_dm, state["token"], uid, msg, file)
    note("Message envoyé à @%s." % name if ok else "Échec de l'envoi.",
         GREEN if ok else RED)
    wait_key()


def dm_multi(state):
    friends = state["friends"]
    if not friends:
        note("Aucun ami.", YELLOW)
        wait_key()
        return
    browse_friends(friends, mode="browse", title="AMIS — relevé des numéros")
    raw = ask("Numéros des amis (ex : 1,3,7)")
    idxs = []
    for part in raw.replace(";", ",").split(","):
        p = part.strip()
        if p.isdigit():
            v = int(p)
            if 1 <= v <= len(friends) and v not in idxs:
                idxs.append(v)
    if not idxs:
        note("Aucun numéro valide.", RED)
        wait_key()
        return
    targets = [(friends[i - 1]["user"]["id"],
                friends[i - 1]["user"].get("username", "?")) for i in idxs]
    msg = ask("Message à envoyer")
    if not msg:
        note("Message vide — annulé.", YELLOW)
        wait_key()
        return
    file = ask_attachment()
    if not confirm_send(targets, msg, file):
        note("Envoi annulé.", MUT)
        return
    campaign(state, targets, msg, file, 2.0)


def dm_all(state):
    friends = state["friends"]
    if not friends:
        note("Aucun ami.", YELLOW)
        wait_key()
        return
    sys.stdout.write(HOME + CLR)
    for l in header_lines(section="campagne générale"):
        print(l)
    panel("ENVOI GÉNÉRAL", [
        ("Cible", "TOUS vos amis", RED),
        ("Nombre", "%d destinataires" % len(friends), TXT),
        ("Risque", "rate limit / signalement si abus", YELLOW),
    ])
    typed = ask("Tapez OUI pour confirmer")
    if typed.lower() not in ("oui", "yes"):
        note("Campagne annulée.", MUT)
        return
    msg = ask("Message à envoyer")
    if not msg:
        note("Message vide — annulé.", YELLOW)
        wait_key()
        return
    file = ask_attachment()
    d = ask("Délai entre chaque envoi (secondes)", default="2")
    try:
        delay = max(0.0, float(d))
    except ValueError:
        delay = 2.0
    targets = [(r["user"]["id"], r["user"].get("username", "?")) for r in friends]
    if not confirm_send(targets, msg, file):
        note("Envoi annulé.", MUT)
        return
    campaign(state, targets, msg, file, delay)


# ══════════════════════════════════════════════════════════════════════
# 11 · ÉCRANS DU TOOL
# ══════════════════════════════════════════════════════════════════════

def friends_screen(state):
    items = [("Liste des amis", "parcourir · fiches détaillées"),
             ("Rechercher", "par pseudo ou nom affiché"),
             ("Statuts de présence", "pourquoi c'est gris"),
             ("Retour", "menu principal")]
    while True:
        idx = select("GESTION DES AMIS", items,
                     pre=lambda: header_lines(state, "amis"))
        if idx is None or idx == 3:
            return
        if idx == 0:
            browse_friends(state["friends"])
        elif idx == 1:
            q = ask("Nom à rechercher")
            if not q:
                note("Recherche vide.", YELLOW)
                wait_key()
                continue
            res = search_friends(state["friends"], q)
            if res:
                note("%d résultat(s)." % len(res), GREEN)
                browse_friends(res, title="RÉSULTATS")
            else:
                note("Aucun ami ne correspond.", YELLOW)
                wait_key()
        elif idx == 2:
            sys.stdout.write(HOME + CLR)
            for l in header_lines(section="présence"):
                print(l)
            panel("STATUTS DE PRÉSENCE", [
                ("Limite", "L'API REST ne fournit pas les statuts", TXT),
                ("Détail", "en ligne / absent / inactif nécessitent une "
                           "connexion Gateway (websocket), impossible ici.", MUT),
            ])
            wait_key()


def messaging_screen(state):
    items = [("DM à un ami", "choisir · écrire · envoyer"),
             ("DM à plusieurs", "sélection par numéros"),
             ("DM à tous les amis", "campagne complète"),
             ("Retour", "menu principal")]
    while True:
        idx = select("MESSAGERIE", items,
                     pre=lambda: header_lines(state, "messagerie"))
        if idx is None or idx == 3:
            return
        if idx == 0:
            dm_single(state)
        elif idx == 1:
            dm_multi(state)
        elif idx == 2:
            dm_all(state)


def profile_flow(state):
    ok, user = run_task("récupération du profil", get_own_user, state["token"])
    if not user:
        note("Impossible de récupérer le profil.", RED)
        wait_key()
        return
    sys.stdout.write(HOME + CLR)
    for l in header_lines(section="mon compte"):
        print(l)
    verified = user.get("verified", False)
    panel("MON COMPTE", [
        ("Utilisateur", "@" + user.get("username", "?"), TXT),
        ("Affiché", user.get("global_name") or "—", TXT),
        ("Discrim.", user.get("discriminator", "0"), TXT),
        ("ID", user.get("id", "?"), TXT),
        ("Email", user.get("email") or "masqué", MUT),
        ("Vérifié", "✓ oui" if verified else "✗ non",
         GREEN if verified else RED),
        ("Créé le", format_date(user.get("created_at")), TXT),
    ])
    wait_key()


def guilds_flow(state, leave=False):
    ok, guilds = run_task("récupération des serveurs", get_guilds, state["token"])
    if not guilds:
        note("Impossible de récupérer les serveurs.", RED)
        wait_key()
        return
    if not guilds:
        note("Aucun serveur.", YELLOW)
        wait_key()
        return
    while True:
        g = browse_guilds(guilds, pick=leave)
        if g is None:
            return
        if not leave:
            continue
        guild = guilds[g]
        gname = guild.get("name", "?")
        gid = guild.get("id")
        sys.stdout.write(HOME + CLR)
        for l in header_lines(section="quitter un serveur"):
            print(l)
        panel("QUITTER UN SERVEUR", [
            ("Serveur", gname, TXT),
            ("ID", str(gid), TXT),
            ("Rôle", "★ créateur" if guild.get("owner") else "membre", TXT),
        ])
        if not confirm("Quitter « %s » définitivement ?" % tr(gname, 30), danger=True):
            continue
        ok, _ = run_task("départ de « %s »" % tr(gname, 24),
                         leave_guild, state["token"], gid)
        if ok:
            note("Vous avez quitté « %s »." % gname, GREEN)
            ok2, guilds = run_task("actualisation de la liste", get_guilds,
                                   state["token"])
            if not guilds:
                guilds = []
        else:
            note("Échec du départ.", RED)
        wait_key()


def servers_screen(state):
    items = [("Mon profil", "identité du compte"),
             ("Mes serveurs", "liste · fiches"),
             ("Quitter un serveur", "sélection + confirmation"),
             ("Retour", "menu principal")]
    while True:
        idx = select("COMPTE & SERVEURS", items,
                     pre=lambda: header_lines(state, "serveurs"))
        if idx is None or idx == 3:
            return
        if idx == 0:
            profile_flow(state)
        elif idx == 1:
            guilds_flow(state, leave=False)
        elif idx == 2:
            guilds_flow(state, leave=True)


def stats_screen(state):
    friends = state["friends"]
    sys.stdout.write(HOME + CLR)
    for l in header_lines(section="statistiques"):
        print(l)
    total = len(friends)
    oldest = newest = None
    oldest_dt = newest_dt = None
    years = {}
    for rel in friends:
        since = rel.get("since")
        if not since:
            continue
        try:
            dt = datetime.datetime.fromisoformat(since.replace("Z", "+00:00"))
        except Exception:
            continue
        if oldest_dt is None or dt < oldest_dt:
            oldest_dt, oldest = dt, rel.get("user", {}).get("username")
        if newest_dt is None or dt > newest_dt:
            newest_dt, newest = dt, rel.get("user", {}).get("username")
        years[dt.year] = years.get(dt.year, 0) + 1
    rows = [("Amis au total", str(total), TXT)]
    if oldest:
        rows.append(("Plus ancien ami", "@%s — %s"
                     % (oldest, oldest_dt.strftime("%d/%m/%Y")), TXT))
    if newest:
        rows.append(("Plus récent ami", "@%s — %s"
                     % (newest, newest_dt.strftime("%d/%m/%Y")), TXT))
    if years:
        top = max(years, key=years.get)
        rows.append(("Année record", "%d — %d ami(s)" % (top, years[top]), YELLOW))
    panel("STATISTIQUES — AMIS", rows)
    print()
    if years:
        print("  " + fg(BLURPLE) + BOLD + "AMIS AJOUTÉS PAR ANNÉE" + RESET)
        print("  " + fg(FAINT) + "─" * 38 + RESET)
        mx = max(years.values())
        for y in sorted(years):
            c = years[y]
            bar = fg(YELLOW if c == mx else BLURPLE) \
                  + "█" * max(1, int(round(c / mx * 22))) + RESET
            print("  " + fg(MUT) + str(y) + RESET + " " + bar + " "
                  + fg(TXT) + str(c) + RESET)
    else:
        note("Pas assez de données pour le graphique.", MUT)
    print()
    wait_key()


# ══════════════════════════════════════════════════════════════════════
# 12 · MENU, EXTINCTION, ENTRÉE
# ══════════════════════════════════════════════════════════════════════

def main_menu(state):
    items = [("Amis", "lister · chercher · fiches"),
             ("Messagerie", "DM ciblé · multiple · tous"),
             ("Compte & Serveurs", "profil · liste · départ"),
             ("Statistiques", "amis dans le temps"),
             ("Quitter", "fermer la session")]
    screens = (friends_screen, messaging_screen, servers_screen, stats_screen)
    while True:
        idx = select("MENU PRINCIPAL", items,
                     pre=lambda: header_lines(state, "menu principal"),
                     footer="↑↓ naviguer · entrée valider · 1-5 direct · q quitter")
        if idx is None or idx == 4:
            return
        screens[idx](state)


def outro(cancelled=False):
    sys.stdout.write(HOME + CLR + CUR_OFF)
    try:
        print()
        if cancelled:
            type_out("Connexion abandonnée.", MUT, 0.03)
        else:
            type_out("Session terminée.", MUT, 0.03)
        time.sleep(0.15)
        type_out("DiscordUtility v%s — remasterisée" % VERSION, BLURPLE_L, 0.022)
        time.sleep(0.15)
        type_out("Restez discret. Le style, c'est la sécurité.", MUT, 0.03)
        print()
        time.sleep(0.6)
        crt_close()                                      # …et la télé s'éteint
        print("  " + fg(FAINT) + "DiscordUtility v%s — à bientôt." % VERSION + RESET)
        print()
    finally:
        sys.stdout.write(CUR_ON + RESET)
        sys.stdout.flush()


def setup():
    if os.name == "nt":
        os.system("")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.stdout.write("\033]0;DiscordUtility v%s\007" % VERSION)
    sys.stdout.flush()


def main():
    setup()
    try:
        intro_cinematic()
        warning_screen()
        state = login()
        if state is None:
            outro(cancelled=True)
            return
        main_menu(state)
        outro()
    except KeyboardInterrupt:
        sys.stdout.write("\r\n")
        note("Interrompu.", RED)
    except EOFError:
        note("Entrée standard fermée.", RED)
    finally:
        KB.stop()
        sys.stdout.write(CUR_ON + RESET)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
