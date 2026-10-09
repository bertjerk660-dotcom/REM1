"""Pure-Python similarity registration (Horn 1987 quaternion method + scale).

fit(A, B) finds s, R, t minimising |s*R*a + t - b| over corresponding points.
Used to place a viewmodel (c_) mesh exactly onto its world (w_) model.
"""
import math


def _centroid(P):
    n = len(P)
    return tuple(sum(p[i] for p in P) / n for i in range(3))


def _eig_max(N, iters=500):
    # power iteration on shifted symmetric matrix (largest eigenvalue)
    shift = sum(abs(N[i][j]) for i in range(4) for j in range(4))
    M = [[N[i][j] + (shift if i == j else 0) for j in range(4)] for i in range(4)]
    v = [1.0, 0.1, 0.1, 0.1]
    for _ in range(iters):
        w = [sum(M[i][j] * v[j] for j in range(4)) for i in range(4)]
        n = math.sqrt(sum(x * x for x in w))
        v = [x / n for x in w]
    return v


def quat_to_mat(q):
    w, x, y, z = q
    return [[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]]


def fit(A, B, s_fixed=None):
    ca, cb = _centroid(A), _centroid(B)
    a = [tuple(p[i] - ca[i] for i in range(3)) for p in A]
    b = [tuple(p[i] - cb[i] for i in range(3)) for p in B]
    S = [[sum(p[i] * q[j] for p, q in zip(a, b)) for j in range(3)] for i in range(3)]
    Sxx, Sxy, Sxz = S[0]; Syx, Syy, Syz = S[1]; Szx, Szy, Szz = S[2]
    N = [[Sxx + Syy + Szz, Syz - Szy, Szx - Sxz, Sxy - Syx],
         [Syz - Szy, Sxx - Syy - Szz, Sxy + Syx, Szx + Sxz],
         [Szx - Sxz, Sxy + Syx, -Sxx + Syy - Szz, Syz + Szy],
         [Sxy - Syx, Szx + Sxz, Syz + Szy, -Sxx - Syy + Szz]]
    R = quat_to_mat(_eig_max(N))
    Ra = [tuple(sum(R[i][k] * p[k] for k in range(3)) for i in range(3)) for p in a]
    s = s_fixed if s_fixed is not None else \
        sum(sum(x * y for x, y in zip(p, q)) for p, q in zip(Ra, b)) / sum(sum(x * x for x in p) for p in a)
    t = tuple(cb[i] - s * sum(R[i][k] * ca[k] for k in range(3)) for i in range(3))
    res = [math.dist(tuple(s * sum(R[i][k] * p[k] for k in range(3)) + t[i] for i in range(3)), q) for p, q in zip(A, B)]
    return s, R, t, math.sqrt(sum(r * r for r in res) / len(res)), max(res)


def apply(s, R, t, p):
    return tuple(s * sum(R[i][k] * p[k] for k in range(3)) + t[i] for i in range(3))
