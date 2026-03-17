import matplotlib.pyplot as plt
import numpy as np

# --- 1. Line Plot ---
x = np.linspace(0, 2 * np.pi, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].plot(x, y_sin, label='sin(x)', color='blue')
axes[0].plot(x, y_cos, label='cos(x)', color='orange', linestyle='--')
axes[0].set_title('Line Plot')
axes[0].set_xlabel('x')
axes[0].set_ylabel('y')
axes[0].legend()
axes[0].grid(True)

# --- 2. Bar Chart ---
categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 12, 67, 34]

axes[1].bar(categories, values, color='steelblue', edgecolor='black')
axes[1].set_title('Bar Chart')
axes[1].set_xlabel('Category')
axes[1].set_ylabel('Value')

# --- 3. Scatter Plot ---
np.random.seed(42)
x_scatter = np.random.randn(100)
y_scatter = 2 * x_scatter + np.random.randn(100)

axes[2].scatter(x_scatter, y_scatter, alpha=0.6, color='green', edgecolors='black', linewidths=0.5)
axes[2].set_title('Scatter Plot')
axes[2].set_xlabel('x')
axes[2].set_ylabel('y')

plt.tight_layout()
plt.savefig('matplotlib_example.png', dpi=150)
plt.show()
print("Plot saved to matplotlib_example.png")
