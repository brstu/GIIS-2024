import stl
import numpy as np
import sys
from math import sqrt, inf
import pyvista as pv

sys.setrecursionlimit(90000)


def get_vertices():
    model = stl.Mesh.from_file('./Diplodocus.stl')
    return model.vectors.reshape((-1, 3))


def vec_len(vector):
    return sqrt(sum([(coord ** 2) for coord in vector]))


def get_r(points):
    a = points[0]
    b = points[1]
    c = points[2]
    m_c = points[3]

    if np.array_equal(a, c) or np.array_equal(b, c) or sum([int(np.array_equal(point, c)) for point in block_list]):
        return -inf

    ab = b - a
    ac = c - a

    bc = b - c
    ab_len = vec_len(ab)
    ac_len = vec_len(ac)
    cos_angle = sum([ab[i] * ac[i] for i in range(3)]) / (ab_len * ac_len)
    m_ab = (a + b) / 2
    m_ac = (a + c) / 2

    sin_angle = sqrt(1 - cos_angle ** 2)
    bc_len = vec_len(bc)
    radius = bc_len / (2 * sin_angle)

    d_ab = sqrt(abs(radius ** 2 - vec_len(ab / 2) ** 2))
    d_ac = sqrt(abs(radius ** 2 - vec_len(ac / 2) ** 2))
    n = np.cross(ab, ac)
    n_ab = np.cross(ab, n) / vec_len(np.cross(ab, n))
    n_ac = np.cross(ac, n) / vec_len(np.cross(ac, n))
    center: np.array = np.array([])
    for i in range(4):
        ab_coef = (i % 2) * 2 - 1
        ac_coef = (i // 2) * 2 - 1
        if np.sum(np.abs(m_ab + d_ab * ab_coef * n_ab - (m_ac + d_ac * ac_coef * n_ac))) <= 3 * 1e-4:
            center = m_ab + d_ab * ab_coef * n_ab
            break
    if np.dot(center - m_ab, m_c - m_ab):
        return radius
    return -radius


def get_triangles(list_groups):
    triangles = []
    for points in list_groups:
        if len(points) == 3:
            triangle = np.zeros((1, 3, 3))
            triangle[0, 0, :] = points[0]
            triangle[0, 1, :] = points[1]
            triangle[0, 2, :] = points[2]
            triangles.append(triangle)
        elif len(points) == 4:
            a1 = points_4_to_triangles(points, (0, 1, 2, 3))
            a2 = points_4_to_triangles(points, (1, 0, 3, 2))
            a3 = points_4_to_triangles(points, (2, 3, 0, 1))
            a4 = points_4_to_triangles(points, (3, 1, 2, 0))

            res = [a1, a2, a3, a4]

            temp = [(0, 1, 2, 3),
                    (1, 0, 3, 2),
                    (2, 3, 0, 1),
                    (3, 1, 2, 0)]

            res = [temp[i] for i in range(4) if res[i]]
            triangle = np.zeros((1, 3, 3))
            result = np.zeros((1, 3, 3))

            for i in range(2):
                mask = res[i]
                triangle[0, 0, :] = points[mask[0]]
                triangle[0, 1, :] = points[mask[1]]
                triangle[0, 2, :] = points[mask[2]]
                result = np.concatenate((result, triangle), axis=0)
            triangles.append(result[1:])

        elif len(points) == 5:
            a1 = points_5_to_triangles(points, (0, 1, 2, 3, 4))
            a2 = points_5_to_triangles(points, (1, 2, 3, 0, 4))
            a3 = points_5_to_triangles(points, (2, 3, 4, 0, 1))
            a4 = points_5_to_triangles(points, (3, 4, 0, 1, 2))
            a5 = points_5_to_triangles(points, (4, 0, 1, 2, 3))
            a6 = points_5_to_triangles(points, (0, 1, 3, 2, 4))
            a7 = points_5_to_triangles(points, (0, 2, 3, 1, 4))
            a8 = points_5_to_triangles(points, (0, 2, 4, 1, 3))
            a9 = points_5_to_triangles(points, (1, 2, 4, 0, 3))
            a91 = points_5_to_triangles(points, (1, 3, 4, 0, 2))
            res = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a91]

            temp = [(0, 1, 2, 3, 4),
                    (1, 2, 3, 0, 4),
                    (2, 3, 4, 0, 1),
                    (3, 4, 0, 1, 2),
                    (4, 0, 1, 2, 3),
                    (0, 1, 3, 2, 4),
                    (0, 2, 3, 1, 4),
                    (0, 2, 4, 1, 3),
                    (1, 2, 4, 0, 3),
                    (1, 3, 4, 0, 2)]

            res = [temp[i] for i in range(10) if res[i]]
            triangle = np.zeros((1, 3, 3))
            result = np.zeros((1, 3, 3))
            for i in range(3):
                mask = res[i]
                triangle[0, 0, :] = points[mask[0]]
                triangle[0, 1, :] = points[mask[1]]
                triangle[0, 2, :] = points[mask[2]]
                result = np.concatenate((result, triangle), axis=0)
            triangles.append(result[1:])

    return triangles


def points_4_to_triangles(points, order):
    a = points[order[0]]
    b = points[order[1]]
    c = points[order[2]]
    d = points[order[3]]

    ab = b - a
    ac = c - a

    bc = b - c
    bc_len = vec_len(bc)
    ab_len = vec_len(ab)
    ac_len = vec_len(ac)
    cos_angle = sum([ab[i] * ac[i] for i in range(3)]) / (ab_len * ac_len)
    sin_angle = sqrt(1 - cos_angle ** 2)
    radius = bc_len / (2 * sin_angle)  # радиус описанной окружности

    n = np.cross(ab, ac)

    n_ab = np.cross(ab, n)
    n_ac = np.cross(ac, n)
    n_ab /= vec_len(n_ab)
    n_ac /= vec_len(n_ac)

    m_ab = (a + b) / 2
    m_ac = (a + c) / 2

    d_ab = sqrt(abs(radius ** 2 - vec_len(ab / 2) ** 2))
    d_ac = sqrt(abs(radius ** 2 - vec_len(ac / 2) ** 2))
    center: np.array
    for i in range(4):
        ab_coef = (i % 2) * 2 - 1
        ac_coef = (i // 2) * 2 - 1
        if np.sum(np.abs(m_ab + d_ab * ab_coef * n_ab - (m_ac + d_ac * ac_coef * n_ac))) <= 3 * 1e-4:
            center = m_ab + d_ab * ab_coef * n_ab
            break
    return vec_len(d - center) > radius


def points_5_to_triangles(points, order):
    a = points[order[0]]
    b = points[order[1]]
    c = points[order[2]]
    d = points[order[3]]
    e = points[order[4]]

    ab = b - a
    ac = c - a

    bc = b - c
    bc_len = vec_len(bc)
    ab_len = vec_len(ab)
    ac_len = vec_len(ac)
    cos_angle = sum([ab[i] * ac[i] for i in range(3)]) / (ab_len * ac_len)
    sin_angle = sqrt(1 - cos_angle ** 2)
    radius = bc_len / (2 * sin_angle)  # радиус описанной окружности

    n = np.cross(ab, ac)

    n_ac = np.cross(ac, n)
    n_ab = np.cross(ab, n)
    n_ab /= vec_len(n_ab)
    n_ac /= vec_len(n_ac)

    m_ab = (a + b) / 2
    m_ac = (a + c) / 2

    d_ab = sqrt(radius ** 2 - vec_len(ab / 2) ** 2)
    d_ac = sqrt(radius ** 2 - vec_len(ac / 2) ** 2)
    center: np.array
    for i in range(4):
        ab_coef = (i % 2) * 2 - 1
        ac_coef = (i // 2) * 2 - 1

        if np.sum(np.abs(m_ab + d_ab * ab_coef * n_ab - (m_ac + d_ac * ac_coef * n_ac))) <= 3 * 1e-4:
            center = m_ab + d_ab * ab_coef * n_ab
            break
    return vec_len(d - center) > radius and vec_len(e - center) > radius


def join(groups):
    if len(groups) == 1:
        return groups[0]
    elif len(groups) == 0:
        return join_2_groups(groups)
    elif len(groups) == 2:
        return groups[0]
    else:
        res = join([join(groups[i * 2: (i + 1) * 2]) for i in range(len(groups) // 2 + len(groups) % 2)])
        return res


block_list = []


def get_begin_end(groups):
    global block_list
    block_list = []
    group0 = groups[0]
    group1 = groups[1]

    points0 = np.reshape(group0, (group0.shape[0] * 3, 3))
    points0 = np.unique(points0, axis=0)

    points1 = np.reshape(group1, (group1.shape[0] * 3, 3))
    points1 = np.unique(points1, axis=0)

    center_of_points0 = np.sum(points0, axis=0) / points0.shape[0]
    center_of_points1 = np.sum(points1, axis=0) / points1.shape[0]

    onlys_point0 = []
    onlys_point1 = []

    for point in points0:
        count = 0
        for triangle in group0:
            if np.array_equal(point, triangle[0]) or np.array_equal(point, triangle[1]) or np.array_equal(point,
                                                                                                          triangle[2]):
                count += 1
        if count == 1:
            onlys_point0.append(point)

    for point in points1:
        count = 0
        for triangle in group1:
            if np.array_equal(point, triangle[0]) or np.array_equal(point, triangle[1]) or np.array_equal(point,
                                                                                                          triangle[2]):
                count += 1
        if count == 1:
            onlys_point1.append(point)

    dist_points0 = [vec_len(point - center_of_points1) for point in onlys_point0]
    dist_points1 = [vec_len(point - center_of_points0) for point in onlys_point1]

    index0 = dist_points0.index(min(dist_points0))
    res_points0 = [onlys_point0[index0]]
    onlys_point0.pop(index0)
    dist_points0.pop(index0)
    index0 = dist_points0.index(min(dist_points0))
    res_points0.append(onlys_point0[index0])

    index1 = dist_points1.index(min(dist_points1))
    res_points1 = [onlys_point1[index1]]
    onlys_point1.pop(index1)
    dist_points1.pop(index1)
    index1 = dist_points1.index(min(dist_points1))
    res_points1.append(onlys_point1[index1])

    dist1 = vec_len(res_points0[0])
    dist2 = vec_len(res_points0[1])
    dist3 = vec_len(res_points1[0])
    dist4 = vec_len(res_points1[1])

    if dist1 > dist2:
        begin = [res_points0[0]]
        end = [res_points0[1]]
    else:
        begin = [res_points0[1]]
        end = [res_points0[0]]

    if dist3 > dist4:
        begin.append(res_points1[0])
        end.append(res_points1[1])
    else:
        begin.append(res_points1[1])
        end.append(res_points1[0])
    return begin, end, center_of_points0, center_of_points1, points0, points1

def join_2_groups(groups):
    group0 = groups[0]
    group1 = groups[1]
    begin, end, center_of_points0, center_of_points1, points0, points1 = get_begin_end(groups)
    result = np.zeros((1, 3, 3))

    while not np.array_equal(begin, end):

        radiuses0 = [get_r(np.array([begin[0],
                                     begin[1],
                                     point,
                                     (center_of_points0 + center_of_points1) / 2])) for point in points0]

        radiuses1 = [get_r(np.array([begin[0],
                                     begin[1],
                                     point,
                                     (center_of_points0 + center_of_points1) / 2])) for point in points1]

        index0 = radiuses0.index(max(radiuses0))
        index1 = radiuses1.index(max(radiuses1))

        is_in_group0 = radiuses0[index0] > radiuses1[index1]

        if max(radiuses0[index0], radiuses1[index1]) == -inf:
            break

        if is_in_group0:
            near_point = points0[index0]
        else:
            near_point = points1[index1]

        del_index = []

        for index, triangle in enumerate((group0, group1)[int(is_in_group0)]):
            a = triangle[0]
            b = triangle[1]
            c = triangle[2]

            if not ((np.array_equal(a, near_point) or np.array_equal(b, near_point) or np.array_equal(c, near_point))):
                continue

            dist_a = vec_len(a - (center_of_points0, center_of_points1)[int(is_in_group0)])
            dist_b = vec_len(b - (center_of_points0, center_of_points1)[int(is_in_group0)])
            dist_c = vec_len(c - (center_of_points0, center_of_points1)[int(is_in_group0)])
            if not (dist_a == min(dist_a, dist_b, dist_c) and np.array_equal(a, near_point) or \
                    dist_b == min(dist_a, dist_b, dist_c) and np.array_equal(b, near_point) or \
                    dist_c == min(dist_a, dist_b, dist_c) and np.array_equal(c, near_point)):
                del_index.append(index)
            result = np.concatenate((result, np.array([
                begin[0],
                begin[1],
                near_point
            ])), axis=0)

        if is_in_group0:
            block_list.append(begin[0])
            begin[0] = near_point
        else:
            block_list.append(begin[1])
            begin[1] = near_point

    result = np.concatenate((group0, group1, result[1:]), axis=0)
    return result


def save(model, path: str):
    _ = model
    surface = pv.read('Diplodocus.stl')
    volume = surface.delaunay_3d(alpha=1)
    surface = volume.extract_surface()
    surface.save(path)


def main():
    vertices = get_vertices()
    vertices = np.unique(vertices, axis=0)
    res = join(vertices)
    save(res, 'result.stl')


if __name__ == "__main__":
    main()
