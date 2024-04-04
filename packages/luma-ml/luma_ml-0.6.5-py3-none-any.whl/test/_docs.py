import __local__
from luma.reduction.manifold import SammonMapping

from sklearn.datasets import make_swiss_roll
import matplotlib.pyplot as plt


X, y = make_swiss_roll(n_samples=500, noise=0.3)

model = SammonMapping(
    n_components=2, max_iter=100, max_halves=35, initialize="pca", verbose=True
)
Z = model.fit_transform(X)

fig = plt.figure(figsize=(10, 5))
ax1 = fig.add_subplot(1, 2, 1, projection="3d")
ax2 = fig.add_subplot(1, 2, 2)

ax1.scatter(X[:, 0], X[:, 1], X[:, 2], c=y, cmap="rainbow")
ax1.set_xlabel(r"$x$")
ax1.set_ylabel(r"$y$")
ax1.set_zlabel(r"$z$")
ax1.set_title("Original S-Curve")

ax2.scatter(Z[:, 0], Z[:, 1], c=y, cmap="rainbow")
ax2.set_xlabel(r"$z_1$")
ax2.set_ylabel(r"$z_2$")
ax2.set_title(f"After {type(model).__name__}")
ax2.grid(alpha=0.2)

plt.tight_layout()
plt.show()
