"""
DART spacecraft collision with asteroid Dimorphos — academic figure.
Perfectly inelastic collision shown in before/after panels.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.font_manager as fm
import numpy as np

# Use Liberation Sans (Arial metric-compatible) if available, else fall back gracefully.
_ls = [f for f in fm.fontManager.ttflist if 'Liberation Sans' in f.name]
FONT = 'Liberation Sans' if _ls else 'DejaVu Sans'
matplotlib.rcParams['font.family'] = FONT

# ── Physics ───────────────────────────────────────────────────────────────────
m_dart = 570        # kg
v_dart = 6600       # m/s
m_dim  = 4.3e9      # kg  (stationary)
v_after = (m_dart * v_dart) / (m_dart + m_dim)   # ≈ 8.74e-4 m/s

# ── Style constants ────────────────────────────────────────────────────────────
C_DART  = '#4878CF'   # muted blue  — DART
C_DIM   = '#6E6E6E'   # mid grey    — Dimorphos
C_EDGE  = '#2a2a2a'   # near-black edge
C_ARR   = '#222222'   # arrow colour
C_TEXT  = '#1a1a1a'   # body text
C_SUB   = '#555555'   # secondary annotation text
FS_BODY = 8           # pt — annotation text
FS_LBL  = 8.5         # pt — object labels
FS_HDR  = 10          # pt — panel header

# ── Helpers ───────────────────────────────────────────────────────────────────
def draw_sphere(ax, cx, cy, r, fc, zorder=3):
    """Filled circle with a subtle specular highlight for a sphere look."""
    ax.add_patch(plt.Circle((cx, cy), r, color=fc, ec=C_EDGE, lw=1.2, zorder=zorder))
    ax.add_patch(plt.Circle((cx - r*0.28, cy + r*0.28), r*0.22,
                             color='white', alpha=0.30, zorder=zorder+1))

def varrow(ax, x0, y, dx, zorder=5):
    """Horizontal velocity arrow."""
    ax.annotate('', xy=(x0 + dx, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle='->, head_width=0.13, head_length=0.1',
                                color=C_ARR, lw=1.5),
                zorder=zorder)

def tlabel(ax, x, y, text, fs=FS_BODY, bold=False, ha='center', va='center', color=C_TEXT):
    ax.text(x, y, text, ha=ha, va=va, fontsize=fs, color=color,
            fontfamily=FONT, fontweight='bold' if bold else 'normal', zorder=10)

# ── Figure ─────────────────────────────────────────────────────────────────────
fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(10, 4.2),
                                  facecolor='white',
                                  gridspec_kw={'wspace': 0.08})

for ax in (ax_l, ax_r):
    ax.set_facecolor('white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')
    ax.axis('off')

# thin dividing line between panels
fig.add_artist(plt.Line2D([0.5, 0.5], [0.05, 0.95],
                           transform=fig.transFigure,
                           color='#cccccc', lw=0.8, zorder=0))

# ── Object sizes (not to scale — schematic) ───────────────────────────────────
R_DART = 0.22
R_DIM  = 1.05

# ── BEFORE panel ──────────────────────────────────────────────────────────────
ax = ax_l
ax.set_title('(a)  Before impact', fontsize=FS_HDR, fontfamily=FONT,
             fontweight='normal', color=C_TEXT, loc='left', pad=6)

# Dimorphos
cx_dim, cy_dim = 7.4, 3.0
draw_sphere(ax, cx_dim, cy_dim, R_DIM, fc=C_DIM)

# DART
cx_dart, cy_dart = 2.0, 3.0
draw_sphere(ax, cx_dart, cy_dart, R_DART, fc=C_DART)

# Approach trajectory — light dashed line
ax.plot([cx_dart + R_DART, cx_dim - R_DIM], [cy_dart, cy_dim],
        '--', color='#aaaaaa', lw=0.8, zorder=1)

# Velocity arrow — DART
varrow(ax, cx_dart + R_DART + 0.08, cy_dart, 1.55)

# Object name labels (inside/near spheres)
tlabel(ax, cx_dart, cy_dart + 0.58, 'DART', fs=FS_LBL, bold=True, color='white',
       va='bottom')
tlabel(ax, cx_dart, cy_dart + 0.58, 'DART', fs=FS_LBL, bold=True,
       va='bottom', color=C_DART)
tlabel(ax, cx_dim,  cy_dim,         'Dimorphos', fs=FS_LBL, bold=True, color='white')

# Mass annotations — below objects
tlabel(ax, cx_dart, cy_dart - 0.52,
       f'$m_1$ = {m_dart:,} kg', fs=FS_BODY, color=C_SUB)
tlabel(ax, cx_dim, cy_dim - 1.45,
       f'$m_2$ = {m_dim:.2e} kg', fs=FS_BODY, color=C_SUB)

# Velocity annotations — above arrows
tlabel(ax, cx_dart + 1.05, cy_dart + 0.28,
       f'$v_1$ = {v_dart:,} m s$^{{-1}}$', fs=FS_BODY, color=C_TEXT)
tlabel(ax, cx_dim, cy_dim - 1.82,
       '$v_2$ = 0 m s$^{-1}$', fs=FS_BODY, color=C_SUB)

# ── AFTER panel ───────────────────────────────────────────────────────────────
ax = ax_r
ax.set_title('(b)  After impact', fontsize=FS_HDR, fontfamily=FONT,
             fontweight='normal', color=C_TEXT, loc='left', pad=6)

# Combined body — centred
cx_sys, cy_sys = 4.6, 3.0
R_SYS = R_DIM
draw_sphere(ax, cx_sys, cy_sys, R_SYS, fc=C_DIM)

# DART embedded as a small contrasting circle
draw_sphere(ax, cx_sys - 0.48, cy_sys + 0.48, R_DART * 0.75, fc=C_DART, zorder=8)

# Post-impact velocity arrow (very slow — scaled visually)
varrow(ax, cx_sys + R_SYS + 0.1, cy_sys, 1.4)

# Labels
tlabel(ax, cx_sys, cy_sys, 'Dimorphos + DART', fs=FS_LBL, bold=True, color='white')

m_total = m_dart + m_dim
tlabel(ax, cx_sys, cy_sys - 1.45,
       f'$m_1 + m_2$ = {m_total:.4e} kg', fs=FS_BODY, color=C_SUB)
tlabel(ax, cx_sys + 1.35, cy_sys + 0.28,
       f"$v'$ = {v_after:.3e} m s$^{{-1}}$", fs=FS_BODY, color=C_TEXT)

# ── Caption-quality figure note ────────────────────────────────────────────────
fig.text(0.5, 0.01,
         'Schematic diagram — object sizes not to scale. '
         'Collision treated as perfectly inelastic; momentum conserved.',
         ha='center', va='bottom', fontsize=6.5, color='#888888', fontfamily=FONT,
         style='italic')

# ── Export ─────────────────────────────────────────────────────────────────────
out_path = '/home/user/reimagined-eureka/dart_collision.png'
fig.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f'Saved → {out_path}')
