"""
DART spacecraft collision with asteroid Dimorphos visualization.
Perfectly inelastic collision shown in before/after panels.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import matplotlib.patheffects as pe
import matplotlib.font_manager as fm
import numpy as np

# Register Arial → Liberation Sans (metric-compatible drop-in replacement).
# If true Arial TTFs are ever installed, matplotlib will prefer them automatically.
_arial_candidates = [f for f in fm.fontManager.ttflist
                     if 'Liberation Sans' in f.name and 'Italic' not in f.style]
if _arial_candidates:
    matplotlib.rcParams['font.family'] = 'Liberation Sans'

FONT = 'Liberation Sans'   # used everywhere instead of 'Arial'

# ── Physics ──────────────────────────────────────────────────────────────────
m_dart   = 570          # kg
v_dart   = 6600         # m/s  (approaching from the left)
m_dim    = 4.3e9        # kg   (Dimorphos, stationary)
v_dim    = 0.0          # m/s

# Conservation of momentum (perfectly inelastic)
v_after  = (m_dart * v_dart + m_dim * v_dim) / (m_dart + m_dim)  # ≈ 8.75e-4 m/s

# ── Helpers ───────────────────────────────────────────────────────────────────
def draw_sphere(ax, cx, cy, radius, face_color, edge_color, zorder=3):
    """Draw a filled circle representing a sphere."""
    circle = plt.Circle((cx, cy), radius, color=face_color,
                         ec=edge_color, lw=1.8, zorder=zorder)
    ax.add_patch(circle)
    # simple highlight for 3-D feel
    highlight = plt.Circle((cx - radius * 0.3, cy + radius * 0.3),
                            radius * 0.25, color='white', alpha=0.35, zorder=zorder + 1)
    ax.add_patch(highlight)

def arrow(ax, x0, y0, dx, dy, color, lw=2.5, head=0.04, zorder=5):
    ax.annotate('', xy=(x0 + dx, y0 + dy), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=f'->, head_width={head}, head_length={head*0.6}',
                                color=color, lw=lw),
                zorder=zorder)

def label(ax, x, y, text, color='white', fs=9, bold=False, ha='center', va='center'):
    weight = 'bold' if bold else 'normal'
    ax.text(x, y, text, ha=ha, va=va, fontsize=fs, color=color,
            fontfamily=FONT, fontweight=weight, zorder=10,
            path_effects=[pe.withStroke(linewidth=2, foreground='black')])

# ── Figure layout ─────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 6.5), facecolor='#0a0a1a')
fig.suptitle('DART Mission — Perfectly Inelastic Collision with Dimorphos',
             fontsize=14, fontweight='bold', color='white', fontfamily=FONT, y=0.97)

ax_left  = fig.add_axes([0.03, 0.12, 0.44, 0.78])
ax_right = fig.add_axes([0.53, 0.12, 0.44, 0.78])

SPACE_COLOR = '#0a0a1a'
for ax in (ax_left, ax_right):
    ax.set_facecolor(SPACE_COLOR)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    # subtle starfield
    rng = np.random.default_rng(42)
    xs = rng.uniform(0, 10, 120)
    ys = rng.uniform(0, 6, 120)
    sizes = rng.uniform(0.5, 2.5, 120)
    ax.scatter(xs, ys, s=sizes, color='white', alpha=0.6, zorder=0)

# ── Object sizes (visual, not to scale) ──────────────────────────────────────
R_DART  = 0.25   # spacecraft — small
R_DIM   = 1.10   # Dimorphos  — large

# ── BEFORE panel ─────────────────────────────────────────────────────────────
ax = ax_left
ax.set_title('BEFORE', fontsize=12, fontweight='bold',
             color='#7ecfff', fontfamily=FONT, pad=6)

# Dimorphos — stationary, right side
cx_dim, cy_dim = 7.5, 3.0
draw_sphere(ax, cx_dim, cy_dim, R_DIM,
            face_color='#8c7560', edge_color='#c4a882')

# DART — approaching from the left
cx_dart, cy_dart = 2.2, 3.0
draw_sphere(ax, cx_dart, cy_dart, R_DART,
            face_color='#4a9eff', edge_color='#a0cfff')

# Velocity arrow for DART
arrow(ax, cx_dart + R_DART + 0.05, cy_dart,
      1.8, 0, color='#4a9eff', head=0.05)

# Labels on objects
label(ax, cx_dart, cy_dart,       'DART',         fs=8,  bold=True)
label(ax, cx_dim,  cy_dim,        'Dimorphos',    fs=9,  bold=True)

# Mass + velocity callouts
label(ax, cx_dart, cy_dart - 0.65,
      f'm₁ = {m_dart:,} kg',       color='#a8d8ff', fs=8.5)
label(ax, cx_dart + 1.05, cy_dart + 0.38,
      f'v₁ = {v_dart:,} m/s →',   color='#4a9eff', fs=8.5, bold=True)

label(ax, cx_dim, cy_dim - 1.55,
      f'm₂ = {m_dim:.2e} kg',      color='#d4b896', fs=8.5)
label(ax, cx_dim, cy_dim - 1.95,
      'v₂ = 0 m/s (stationary)',   color='#a0a0a0', fs=8.5)

# v2 = 0 marker
ax.plot(cx_dim, cy_dim, 'x', color='#a0a0a0', ms=7, mew=2, zorder=6)

# dashed trajectory line
ax.plot([cx_dart + R_DART, cx_dim - R_DIM], [cy_dart, cy_dim],
        '--', color='#4a9eff', lw=1, alpha=0.5, zorder=1)

# ── AFTER panel ───────────────────────────────────────────────────────────────
ax = ax_right
ax.set_title('AFTER', fontsize=12, fontweight='bold',
             color='#ff9f60', fontfamily=FONT, pad=6)

# Combined system — centred, slightly larger (merged)
cx_sys, cy_sys = 4.5, 3.0
R_SYS = R_DIM + 0.06   # tiny visual increase to hint merger
draw_sphere(ax, cx_sys, cy_sys, R_SYS,
            face_color='#8c7560', edge_color='#ff9f60')

# DART embedded (small blue dot)
draw_sphere(ax, cx_sys - 0.55, cy_sys + 0.55, R_DART * 0.8,
            face_color='#4a9eff', edge_color='#a0cfff', zorder=8)

# Slow post-impact velocity arrow
arrow(ax, cx_sys + R_SYS + 0.05, cy_sys,
      1.6, 0, color='#ff9f60', head=0.05)

# Labels
label(ax, cx_sys, cy_sys, 'Dimorphos\n+ DART', fs=8.5, bold=True)

m_total = m_dart + m_dim
label(ax, cx_sys, cy_sys - 1.6,
      f'm₁ + m₂ = {m_total:.4e} kg', color='#d4b896', fs=8.5)
label(ax, cx_sys + 1.4, cy_sys + 0.38,
      f"v' = {v_after*1e3:.4f} mm/s →", color='#ff9f60', fs=8.5, bold=True)
label(ax, cx_sys + 1.4, cy_sys - 0.08,
      f'({v_after:.4e} m/s)', color='#a0a0a0', fs=7.5)

# Impact flash
for r, alpha in [(0.15, 0.7), (0.3, 0.4), (0.5, 0.2)]:
    flash = plt.Circle((cx_sys - R_SYS * 0.7, cy_sys + R_SYS * 0.7),
                        r, color='#ffdd55', alpha=alpha, zorder=7)
    ax.add_patch(flash)

# ── Momentum equation at the bottom ──────────────────────────────────────────
eq_text = (
    r"Conservation of Momentum:  $m_1 v_1 + m_2 v_2 = (m_1 + m_2)\,v'$"
    "\n"
    rf"$570 \times 6600 + 4.3 \times 10^9 \times 0 = (570 + 4.3 \times 10^9)\,v'$"
    "          "
    rf"$\Rightarrow\; v' = {v_after:.4e}$ m/s"
)
fig.text(0.5, 0.025, eq_text, ha='center', va='bottom', fontsize=9.5,
         color='#e0e0e0', fontfamily=FONT,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e',
                   edgecolor='#444488', lw=1.2))

# ── Export ────────────────────────────────────────────────────────────────────
out_path = '/home/user/reimagined-eureka/dart_collision.png'
fig.savefig(out_path, dpi=300, bbox_inches='tight',
            facecolor=fig.get_facecolor())
print(f'Saved → {out_path}')
