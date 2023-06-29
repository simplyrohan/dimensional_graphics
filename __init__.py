"""
A configurable three-dimensional model renderer without OpenGL.

This uses raw math to project and texture your own models.
"""

import pygame
from math import asin, atan2, degrees
from .loader import load

def bary_to_cart(bary, triangle):
    return (
        bary[0] * triangle[0][0] + bary[1] * triangle[1][0] + bary[2] * triangle[2][0],
        bary[0] * triangle[0][1] + bary[1] * triangle[1][1] + bary[2] * triangle[2][1],
    )


def cart_to_bary(cart: tuple[int, int], triangle: list[tuple, tuple, tuple]):
    # Bary[2] = 1 - bary[0] - bary[1]
    # Bary[1] = bary[3] - bary[0] + 1
    # Bary[0] = bary[2] - bar[1] + 1
    x, y = zip(*triangle)
    y2y3 = y[1] - y[2]
    x3x2 = x[2] - x[1]
    xx2 = cart[0] - x[2]
    yy2 = cart[1] - y[2]
    x0x2 = x[0] - x[2]
    y0y2 = y[0] - y[2]
    try:
        b1 = (y2y3 * xx2 + x3x2 * yy2) / (y2y3 * x0x2 + x3x2 * y0y2)

        b2 = ((y[2] - y[0]) * xx2 + x0x2 * yy2) / (y2y3 * x0x2 + x3x2 * y0y2)
    except ZeroDivisionError:
        return 0

    return b1, b2, 1 - b1 - b2


def get_pixel(point: tuple, triangle: list, uvs: list, texture: pygame.Surface):
    size = texture.get_size()
    uvs = [(max(0, i[0] * size[0] - 1), max(0, i[1] * size[1] - 1)) for i in uvs]

    bbary = cart_to_bary(point, triangle)
    if bbary == 0:
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
    triangle = [(p[0] - x, p[1] - y) for p in triangle]
    if 0 in size:
        return

    tri = pygame.Surface(size).convert_alpha()  # Doesn't cause segfault
    pa = pygame.PixelArray(tri)  # Doesn't cause segfault
    for r, row in enumerate(pa):
        row[:] = [get_pixel((r, i), triangle, uvs, texture) for i in range(len(row))]
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
            [[axis * scale for axis in vertex[:3]] + vertex[-2:] for vertex in face]
            for face in self.raw_faces
        ]
        self.position = pygame.Vector3([0, 0, 0])
        self.rotation = pygame.Vector3([0, 0, 0])

        self.color = (54, 104, 143)

        self.texture = pygame.Surface((1, 1))
        self.texture.fill((150, 150, 150))


class Camera:
    """
    Projects three-dimensional `Models` onto pygame surfaces.

    Uses [weak perspective](https://en.wikipedia.org/wiki/3D_projection#Weak_perspective_projection) projection on all vertices of a model. These are then wireframed and sorted, and finally textured. Note that this is not a ray-caster.
    To use this, simply call `render()` to draw all the models to the screen.
    """

    focal_length = 100

    def __init__(self) -> None:
        """
        Initializes a physical and virtual camera instance, and specifies all camera information.

        Args:
            objs: A pointer to a list of `Models` to be drawn.
        """
        self.position = pygame.Vector3([0, 0, 0])  # The physical position of the camera
        self.rotation = pygame.Vector3([0, 0, 0])  # The physical rotation of the camera
        self.forward = pygame.Vector3([0, 0, 1])

    def render(self, objects: list, screen: pygame.Surface) -> None:
        # Transformations
        self.forward.normalize_ip()
        pitch, yaw = degrees(asin(self.forward.y)), degrees(
            atan2(self.forward.x, self.forward.z)
        )
        faces = []
        for obj in objects:
            for face in obj.faces:
                true_face = []
                zs = []
                uvs = []
                for point in face:
                    # Local transforms
                    # Rotation
                    uvs.append(point[-2:])

                    point = point[:3]
                    true_point = pygame.Vector3(point)
                    rotate(true_point, obj.rotation)
                    # Position
                    true_point: pygame.Vector3 = (
                        true_point + obj.position - self.position
                    )

                    # Camera transforms
                    # rotate(true_point, self.rotation)
                    true_point.rotate_y_ip(yaw)
                    true_point.rotate_x_ip(pitch)
                    zs.append(true_point[2])
                    
                    projected = self.project(true_point)

                    true_face.append([projected[0]+screen.get_width(), projected[1]+screen.get_height()])
                faces.append([true_face, min(zs), uvs, obj.texture])

        faces = sorted(faces, key=lambda v: v[1], reverse=True)
        for face, z, uvs, texture in faces:
            if z > -self.focal_length:
                # print(uvs)
                draw(screen, face, uvs, texture)
                
    def project(self, point: list[int, int, int]) -> tuple:
        # TODO: Do not use try/except to sole ZeroDiv. It is slow. Implement culling
        x_projected: float = (point[0] * self.focal_length) // (
            self.focal_length + point[2]
        )
        y_projected: float = -(point[1] * self.focal_length) // (
            self.focal_length + point[2]
        )
        return x_projected, y_projected
