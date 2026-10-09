"""Similarity ICP (pure Python) to register a viewmodel mesh onto its world model.

icp(src, dst, init=(s,R,t)) -> (s, R, t, stats). Uses a voxel grid for nearest
neighbours and trims the worst 10% of pairs each iteration (robust to parts that
are posed differently, e.g. a spinning element).
"""
import math
from similarity_fit import fit, apply


class Grid:
    def __init__(self, pts, cell):
        self.cell, self.g = cell, {}
        for p in pts:
            self.g.setdefault(self.key(p), []).append(p)

    def key(self, p):
        return tuple(int(math.floor(x / self.cell)) for x in p)

    def nn(self, p, rings=2):
        k = self.key(p)
        best, bq = 9e9, None
        r = range(-rings, rings + 1)
        for dx in r:
            for dy in r:
                for dz in r:
                    for q in self.g.get((k[0] + dx, k[1] + dy, k[2] + dz), ()):
                        d = math.dist(p, q)
                        if d < best:
                            best, bq = d, q
        return best, bq


def icp(src, dst, init, iters=40, cell=0.5, trim=0.9, s_fixed=None):
    g = Grid(dst, cell)
    s, R, t = init
    hist = []
    for it in range(iters):
        pairs = []
        for p in src:
            q = apply(s, R, t, p)
            d, n = g.nn(q)
            if n is not None:
                pairs.append((d, p, n))
        pairs.sort(key=lambda x: x[0])
        if len(pairs) < 10:  # start too far off: nothing inside the search radius
            return s, R, t, {"iterations": it, "median": float("inf"), "p95": float("inf"), "matched": len(pairs),
                             "within_0.01": 0.0, "within_0.05": 0.0, "unmatched_beyond_search": len(src) - len(pairs),
                             "rms_trimmed": float("inf"), "failed": "too few correspondences"}
        keep = pairs[:max(10, int(len(pairs) * trim))]
        s, R, t, rms, mx = fit([p for _, p, _ in keep], [n for _, _, n in keep], s_fixed=s_fixed)
        hist.append(rms)
        if it > 3 and abs(hist[-2] - hist[-1]) < 1e-6:
            break
    final = sorted(g.nn(apply(s, R, t, p))[0] for p in src)
    stats = {"iterations": len(hist), "rms_trimmed": hist[-1], "matched": len(final),
             "median": final[len(final) // 2], "p95": final[int(len(final) * 0.95)],
             "within_0.01": sum(1 for d in final if d <= 0.01) / len(final),
             "within_0.05": sum(1 for d in final if d <= 0.05) / len(final),
             "unmatched_beyond_search": sum(1 for d in final if d >= 9e8)}
    return s, R, t, stats
