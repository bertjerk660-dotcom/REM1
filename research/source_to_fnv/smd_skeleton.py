"""SMD skeleton/bind-pose helpers (Source convention) shared by weapon conversion.

SMD bind pose lines are 'id px py pz rx ry rz' (radians), local to the parent.
Rotation matrix = Rz(rz) * Ry(ry) * Rx(rx) (Source AngleMatrix order for SMD).
Reference-mesh vertices are stored in model space.
"""
import math


def parse_skeleton(path):
    lines = open(path, encoding="utf-8", errors="ignore").read().splitlines()
    nodes, bind = {}, {}
    i = lines.index("nodes") + 1
    while lines[i].strip() != "end":
        t = lines[i].split('"')
        nodes[int(t[0])] = (t[1], int(t[2]))
        i += 1
    i = next(k for k, l in enumerate(lines) if l.strip() == "skeleton") + 2  # skip 'time 0'
    while lines[i].strip() != "end":
        v = lines[i].split()
        bind[int(v[0])] = tuple(float(x) for x in v[1:7])
        i += 1
    return nodes, bind


def rot(rx, ry, rz):
    cx, sx, cy, sy, cz, sz = math.cos(rx), math.sin(rx), math.cos(ry), math.sin(ry), math.cos(rz), math.sin(rz)
    Rx = [[1, 0, 0], [0, cx, -sx], [0, sx, cx]]
    Ry = [[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]
    Rz = [[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]
    return mm(Rz, mm(Ry, Rx))


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(3)) for i in range(3))


def tr(A):
    return [[A[j][i] for j in range(3)] for i in range(3)]


def world_transforms(nodes, bind):
    W = {}

    def get(b):
        if b in W:
            return W[b]
        px, py, pz, rx, ry, rz = bind[b]
        R, t = rot(rx, ry, rz), (px, py, pz)
        parent = nodes[b][1]
        if parent >= 0:
            PR, Pt = get(parent)
            R, t = mm(PR, R), tuple(Pt[i] + mv(PR, t)[i] for i in range(3))
        W[b] = (R, t)
        return W[b]
    for b in nodes:
        get(b)
    return {nodes[b][0]: W[b] for b in nodes}


def to_local(W_bone, v):
    R, t = W_bone
    return mv(tr(R), tuple(v[i] - t[i] for i in range(3)))
