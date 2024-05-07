import pyvista as pv

def convex_hull_merge(A, B):

    if not A:
        return B
    if not B:
        return A

    lower_A = lower_hull(A)
    upper_A = upper_hull(A)
    lower_B = lower_hull(B)
    upper_B = upper_hull(B)

    lower = merge_hulls(lower_A, lower_B)
    upper = merge_hulls(upper_A, upper_B)

    return lower + upper[1:-1]

def do_delaunay_3d(surface, alpha=1):
    return surface.delaunay_3d(alpha=1)

def lower_hull(points):
    hull = []
    for p in points:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)
    return hull

def upper_hull(points):
    hull = []
    for p in reversed(points):
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)
    return hull

def merge_hulls(A, B):

    max_A, min_A = max(A, key=lambda p: p[0]), min(A, key=lambda p: p[0])
    max_B, min_B = max(B, key=lambda p: p[0]), min(B, key=lambda p: p[0])

    idx_max_A, idx_min_A = A.index(max_A), A.index(min_A)
    idx_max_B, idx_min_B = B.index(max_B), B.index(min_B)

    merged = A[:idx_min_A] + B[idx_min_B:] + B[:idx_max_B] + A[idx_max_A:]
    return merged

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

surface = pv.read('./AHRI.stl')
volume = do_delaunay_3d(surface, alpha=1)
surface = volume.extract_surface()
surface.save("./res.stl")
