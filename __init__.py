"""
A configurable three-dimensional model renderer without OpenGL.

This uses raw math to project and texture your own models.
"""

import pygame
import math

from .loader import load

AIR_THICKNESS = 1.25

def rotate(vert, xyz) -> list:
    """
    Rotates given vertex on the X, Y, and Z dimensions.
    """
    """
    x, y, z = xyz
    x_matrix = np.array([[1, 0, 0], [0, cos(x), -sin(x)], [0, sin(x), cos(x)]])

    y_matrix = np.array([[cos(y), 0, sin(y)], [0, 1, 0], [-sin(y), 0, cos(y)]])

    z_matrix = np.array([[cos(z), -sin(z), 0], [sin(z), cos(z), 0], [0, 0, 1]])

    arr = np.array(vert)

    return [round(i) for i in arr @ x_matrix @ y_matrix @ z_matrix]
    """
    vert.rotate_x_ip(xyz[0])
    vert.rotate_y_ip(xyz[1])
    vert.rotate_z_ip(xyz[2])


class Model:
    def __init__(self, faces, scale) -> None:
        self.raw_faces = faces

        self.faces = [
            [[axis * scale for axis in vertex] for vertex in face]
            for face in self.raw_faces
        ]

        self.position = pygame.Vector3([0, 0, 0])
        self.rotation = pygame.Vector3([0, 0, 0])

        self.color = (54, 104, 143)


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

        self.position = pygame.Vector3([0, 0, 0])  # The physical position of the camera
        self.rotation = pygame.Vector3([0, 0, 0])  # The physical rotation of the camera
    
    # @profile
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
                    true_point = pygame.Vector3(point)
                    rotate(true_point, obj.rotation)
                    # Position
                    true_point = true_point + obj.position - self.position

                    # Camera transforms
                    rotate(true_point, self.rotation)
                    zs.append(true_point[2])


                    true_face.append([a+250 for a in self.project(true_point)])
                faces.append([true_face, min(zs)])
                # color = obj.color
                # pygame.draw.polygon(screen, color, true_face)
        faces = sorted(faces, key=lambda v: v[1], reverse=True)
        print(len(faces))
        for face, z in faces:
            if z != 1.1:
                color = obj.color

                light = [0, 0, 100]  # Light Source

                dist = abs(100-z)-50
                # print(dist)

                dist *= AIR_THICKNESS  # Light to shade factor

                color = [pygame.math.clamp(i + dist, 0, 250) for i in color]

                # print(color)
                        
                pygame.draw.polygon(screen, color, face)
                # highest_z = min(zs)

                # faces.append([true_face, highest_z])
        
        # Z-Sorting
        # faces = sorted(faces, key=lambda face: face[1], reverse=True)
    """
        for face, highest_z in faces:
            # Projection
            projected_points = [[i + 250 for i in self.project(p)] for p in face]

            # Shading
            color = obj.color

            light = [0, 0, 100]  # Light Source

            mpoint = [0, 0, 0]  # Average of all points
            for point in face:
                mpoint = [v + point[i] for i, v in enumerate(point)]
            mpoint = [i / len(face) for i in mpoint]

            dist = math.dist(mpoint, light) - 120

            dist *= AIR_THICKNESS  # Light to shade factor

            color = [pygame.math.clamp(i + dist, 0, 200) for i in color]

            # Drawing
            pygame.draw.polygon(screen, color, projected_points)
    """
    def project(self, point: list[int, int, int]) -> tuple:
        # TODO: Do not use try/except to sole ZeroDiv. It is slow. Implement culling
        x_projected: float = (point[0] * self.focal_length) // (self.focal_length + point[2])
        y_projected: float = -(point[1] * self.focal_length) // (self.focal_length + point[2])
        return x_projected, y_projected

