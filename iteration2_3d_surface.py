import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# Constants
m1 = 579.4          # kg
m2 = 4.3e9          # kg
u1 = 6144.9         # m/s
T  = 42900          # s
v_orb = 0.1767      # m/s

# Domain
theta_deg = np.linspace(0, 80, 300)
e_vals    = np.linspace(0, 1, 300)
THETA, E  = np.meshgrid(theta_deg, e_vals)

# ΔT equation (converted to minutes)
theta_rad = np.deg2rad(THETA)
dT = (3 * T * (1 + E) * m1 * u1 * np.cos(theta_rad)) / ((m1 + m2) * v_orb) / 60

# Figure
fig = plt.figure(figsize=(8, 6))
ax  = fig.add_subplot(111, projection='3d')

# --- 3D surface ---
surf = ax.plot_surface(THETA, E, dT, cmap='YlGnBu', linewidth=0, antialiased=True, zorder=1)

# --- Translucent horizontal plane at z = 33 min ---
theta_plane = np.linspace(0, 80, 2)
e_plane     = np.linspace(0, 1, 2)
TP, EP = np.meshgrid(theta_plane, e_plane)
ZP = np.full_like(TP, 33.0)
ax.plot_surface(TP, EP, ZP, color='red', alpha=0.2, zorder=2, label='NASA observed (33 min)')

# Proxy patch for legend (plot_surface doesn't auto-register)
from matplotlib.patches import Patch
red_proxy = Patch(facecolor='red', alpha=0.4, label='NASA observed (33 min)')

# --- DART parameters point: θ=17°, e=0 ---
theta_dart = 17.0
e_dart     = 0.0
dT_dart    = (3 * T * (1 + e_dart) * m1 * u1 * np.cos(np.deg2rad(theta_dart))) / ((m1 + m2) * v_orb) / 60

ax.scatter([theta_dart], [e_dart], [dT_dart],
           color='black', s=60, zorder=5, depthshade=False)
ax.text(theta_dart + 2, e_dart + 0.05, dT_dart + 1.5,
        'DART parameters', fontsize=8, fontweight='bold', color='black')

# --- Labels & formatting ---
ax.set_xlabel('Impact angle θ (°)', labelpad=8)
ax.set_ylabel('Coefficient of restitution e', labelpad=8)
ax.set_zlabel('ΔT (minutes)', labelpad=8)
ax.set_zlim(0, 40)
ax.set_title('Predicted ΔT as a function of impact angle and restitution', pad=12)

# Colourbar
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, pad=0.1)
cbar.set_label('ΔT (minutes)')

# Legend
ax.legend(handles=[red_proxy], loc='upper right', fontsize=8)

# Viewing angle
ax.view_init(elev=25, azim=225)

plt.tight_layout()
plt.savefig('iteration2_3d_surface.png', dpi=300, bbox_inches='tight')
plt.show()
print("Saved iteration2_3d_surface.png")
