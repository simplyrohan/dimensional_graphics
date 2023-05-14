"""
A configurable three-dimensional model renderer without OpenGL.

This uses raw math to project and texture your own models.
"""

import pygame

import numpy as np

from math import cos, sin

import math

# from numba import jit

import time

from . import loader

# from scipy.interpolate import interp1d

AIR_THICKNESS = 2


def rotate(vert, xyz) -> list:
    """
    Rotates given vertex on the X, Y, and Z dimensions.
    """
    x, y, z = xyz
    x_matrix = np.array([[1, 0, 0], [0, cos(x), -sin(x)], [0, sin(x), cos(x)]])

    y_matrix = np.array([[cos(y), 0, sin(y)], [0, 1, 0], [-sin(y), 0, cos(y)]])

    z_matrix = np.array([[cos(z), -sin(z), 0], [sin(z), cos(z), 0], [0, 0, 1]])

    arr = np.array(vert)

    return [
        round(i) for i in arr@x_matrix@y_matrix@z_matrix
    ]


class Model:
    def __init__(self, faces, scale) -> None:
        self.raw_faces = faces

        self.faces = [
            [[axis * scale for axis in vertex] for vertex in face]
            for face in self.raw_faces
        ]

        self.position = [0, 0, 0]
        self.rotation = [0, 0, 0]

        self.color = (200, 125, 130)


class Camera:
    """
    Projects three-dimensional `Models` onto pygame surfaces.

    Uses [weak perspective](https://en.wikipedia.org/wiki/3D_projection#Weak_perspective_projection) projection on all vertices of a model. These are then wireframed and sorted, and finally textured. Note that this is not a ray-caster.
    To use this, simply call `render()` to draw all the models to the screen.
    """

    focal_length = 100

    def __init__(self, objs) -> None:
        """
        Initializes a physical and virtual camera instance, and specifies all camera information.

        Args:
            objs: A pointer to a list of `Models` to be drawn.
        """
        self.objs = objs  # A pointer to a list of `Models`

        self.position = [0, 0, 0]  # The physical position of the camera
        self.rotation = [0, 0, 0]  # The physical rotation of the camera

    def render(self, screen) -> None:
        # Transformations
        faces = []
        for obj in self.objs:
            for face in obj.faces:
                true_face = []
                zs = []
                for point in face:
                    # Local transforms
                    # Rotation
                    true_point = rotate(point, obj.rotation)
                    # Position

                    true_point = [a+obj.position[ai]
                                  for ai, a in enumerate(true_point)]

                    # Camera transforms

                    true_point = [a+self.position[ai]
                                  for ai, a in enumerate(true_point)]

                    true_point = rotate(true_point, self.rotation)

                    zs.append(true_point[2])
                    true_face.append(true_point)

                highest_z = min(zs)

                faces.append([true_face, highest_z])

        # Z-Sorting
        faces = sorted(faces, key=lambda face: face[1], reverse=True)

        # NOTE: very fast; 3/4 microseconds per iteration
        for face, highest_z in faces:
            # Projection
            start = time.time()

            projected_points = [
                [i + 250 for i in self.project(p)] for p in face]

            # Shading
            start = time.time()

            color = obj.color

            # Light Source
            light = [0, 0, 100]

            mpoint = [0, 0, 0]
            for point in face:
                mpoint = [v+point[i] for i, v in enumerate(point)]
            mpoint = [i/len(face) for i in mpoint]

            dist = math.dist(mpoint, light) - 120

            dist *= AIR_THICKNESS  # Light to shade factor

            color = [pygame.math.clamp(i+dist, 0, 200) for i in color]
            """
            x, y = zip(projected_points)

            surface = pygame.Surface((max(x)-min(x), max(y)-min(y)))
            """

            # Drawing
            start = time.time()
            pygame.draw.polygon(screen, color, projected_points)

    def project(self, point) -> tuple:
        x, y, z = point
        y -= 70
        try:
            x_projected = (x * self.focal_length) / (self.focal_length + z)
        except ZeroDivisionError:
            x_projected = x

        try:
            y_projected = (-y * self.focal_length) / (self.focal_length + z)
        except ZeroDivisionError:
            y_projected = -y

        return x_projected, y_projected


CUBE_MODEL = [
    [[-0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5]],
    [[-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5]],
]
