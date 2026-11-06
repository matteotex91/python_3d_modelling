import matplotlib.pyplot as plt
import numpy as np

o1 = np.array([1, 0, 0])
A = np.array([0, 0, 0])
o2 = np.array([1, 1, 0])
B = np.array([0, 0, 1])

alpha = np.linspace(-5, 5, 100)
pq_len = np.array(
    [
        np.linalg.norm(A - B + a * (o1 - o2 * (np.dot(o1, o2)) / (np.dot(o2, o2))))
        for a in alpha
    ]
)


def skew(v):
    return np.cross(np.eye(3), v)


def rotmat(o, theta):
    u = o / np.linalg.norm(o)
    return (
        np.eye(3) * np.cos(theta)
        + np.tensordot(u, u, 0) * (1 - np.cos(theta))
        + skew(u) * np.sin(theta)
    )


gen1 = np.array([A + a * o1 for a in alpha])
gen2 = np.array([B + a * np.dot(o1, o2) * o2 / np.dot(o2, o2) for a in alpha])
mo1 = np.linalg.norm(o1)
mo2 = np.linalg.norm(o2)
conj = gen2 - gen1
norms = np.linalg.norm(conj, axis=1) * mo2 / (mo1 + mo2)
mid_vec = np.array([c * n / np.linalg.norm(c) for c, n in zip(conj, norms)])

conj_2 = -gen2 + gen1
norms_2 = np.linalg.norm(conj_2, axis=1) * mo1 / (mo1 + mo2)
mid_vec_2 = np.array([c * n / np.linalg.norm(c) for c, n in zip(conj_2, norms_2)])

mid = gen1 + mid_vec


print("stop here")

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.scatter(gen1[:, 0], gen1[:, 1], gen1[:, 2])
ax.scatter(gen2[:, 0], gen2[:, 1], gen2[:, 2])
ax.scatter(mid[:, 0], mid[:, 1], mid[:, 2])
plt.show()


fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.scatter(gen1[:, 0], gen1[:, 1], gen1[:, 2])
ax.scatter(gen2[:, 0], gen2[:, 1], gen2[:, 2])
iper1 = []
iper2 = []
for t in np.linspace(0, 2 * np.pi, 50):
    rot1 = rotmat(o1, t)
    rot2 = rotmat(o2, t)
    for v, c in zip(gen1, mid_vec):
        iper1.append(v + np.dot(rot1, c))
    for v, c in zip(gen2, mid_vec_2):
        iper2.append(v + np.dot(rot2, c))
iper1 = np.array(iper1)
iper2 = np.array(iper2)
ax.scatter(iper1[:, 0], iper1[:, 1], iper1[:, 2])
ax.scatter(iper2[:, 0], iper2[:, 1], iper2[:, 2])
plt.show()
