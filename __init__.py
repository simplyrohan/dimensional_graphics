"""
A configurable three-dimensional model renderer without OpenGL.

This uses raw math to project and texture your own models.
"""

import pygame
from .loader import load

FOCAL_LENGTH = 100

def bary_to_cart(bary, triangle):
    return (
        bary[0] * triangle[0][0] + bary[1] * triangle[1][0] + bary[2] * triangle[2][0],
        bary[0] * triangle[0][1] + bary[1] * triangle[1][1] + bary[2] * triangle[2][1],
    )


def cart_to_bary(cart: tuple[int, int], triangle: list[tuple, tuple, tuple]):
    # Bartriangle[2][1] = 1 - bartriangle[0][1] - bartriangle[1][1]
    # Bartriangle[1][1] = bary[3] - bartriangle[0][1] + 1
    # Bartriangle[0][1] = bartriangle[2][1] - bar[1] + 1
    y2y3 = triangle[1][1] - triangle[2][1]
    x3x2 = triangle[2][0] - triangle[1][0]
    xx2 = cart[0] - triangle[2][0]
    yy2 = cart[1] - triangle[2][1]
    x0x2 = triangle[0][0] - triangle[2][0]
    denominator = y2y3 * x0x2 + x3x2 * (triangle[0][1] - triangle[2][1])

    if denominator == 0:
        return (0, 0, 0)

    b1 = (y2y3 * xx2 + x3x2 * yy2) / denominator

    b2 = ((triangle[2][1] - triangle[0][1]) * xx2 + x0x2 * yy2) / denominator

    return (b1, b2, 1 - b1 - b2)


def get_pixel(point: tuple, triangle: list, uvs: list, texture: pygame.Surface):
    bbary = cart_to_bary(point, triangle)
    if bbary == (0, 0, 0):
        return (0, 0, 0, 0)
    if bbary[0] >= 0 and bbary[1] >= 0 and bbary[2] >= 0:
        v = bary_to_cart(bbary, uvs)
        return texture.get_at((int(v[0]), int(v[1])))
    else:
        return (0, 0, 0, 0)


def draw(screen: pygame.Surface, triangle: list, uvs: list, texture: pygame.Surface):
    x, y = zip(*triangle)
    size = max(x) - min(x), max(y) - min(y)
    x, y = min(x), min(y)
    texture_size = texture.get_size()
    uvs = [
        (
            pygame.math.clamp(i[0] * texture_size[0] - 1, 0, texture_size[0] - 1),
            pygame.math.clamp(i[1] * texture_size[1] - 1, 0, texture_size[1] - 1),
        )
        for i in uvs
    ]

    triangle = [(p[0] - x, p[1] - y) for p in triangle]
    if 0 in size:
        return

    tri = pygame.Surface(size).convert_alpha()  # Doesn't cause segfault
    pa = pygame.PixelArray(tri)  # Doesn't cause segfault
    for r, row in enumerate(pa):
        for c in range(len(row)):
            pa[r][c] = get_pixel((r, c), triangle, uvs, texture)
        # row[:] = [get_pixel((r, i), triangle, uvs, texture) for i in range(len(row))]
    pa.close()
    screen.blit(tri, (x, y))


def rotate(vert, xyz) -> list:
    """
    Rotates given vertex on the X, Y, and Z dimensions.
    """
    vert.rotate_x_ip(xyz[0])
    vert.rotate_y_ip(xyz[1])
    vert.rotate_z_ip(xyz[2])


class Model:
    def __init__(self, faces, scale) -> None:
        self.raw_faces = faces

        self.faces = [
            [([axis * scale for axis in vertex[:3]], vertex[-2:]) for vertex in face]
            for face in self.raw_faces
        ]
        self.position = pygame.Vector3([0, 0, 0])
        self.rotation = pygame.Vector3([0, 0, 0])

        self.color = (54, 104, 143)

        self.texture = pygame.Surface((1, 1))
        self.texture.fill((150, 150, 150))

    def copy(self):
        m = Model([], 0)
        m.__dict__ = self.__dict__
        return m



def render(objects: list[Model], screen: pygame.Surface) -> None:
    
    faces = []
    for obj in objects:
        for face in obj.faces:
            projected_face = []
            uvs = []
            culled = False
            for point, uv in face:
                # Culling
                
                projected_face.append(_project(point)+pygame.Vector2(screen.get_size())*0.5)
                uvs.append(uv)

            faces.append((projected_face, uvs, obj.texture))

    faces = sorted(faces, key=lambda v: v[1], reverse=True)
    for face, uvs, texture in faces:
        draw(screen, face, uvs, texture)
        # pygame.draw.polygon(screen, (0,0,0), face, 2)

def _project(point: list[int, int, int]) -> tuple:
    # TODO: Do not use try/except to sole ZeroDiv. It is slow. Implement culling
    z = FOCAL_LENGTH + point[2]
    x_projected: float = (point[0] * FOCAL_LENGTH) // z
    y_projected: float = -(point[1] * FOCAL_LENGTH) // z
    return x_projected, y_projected
