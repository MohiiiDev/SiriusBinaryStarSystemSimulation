
import numpy as np

import settings


class SpacetimeGrid:
    def __init__(self):
        self.size = settings.SPACETIME_GRID_SIZE
        self.step = settings.SPACETIME_GRID_STEP
        self.color = settings.SPACETIME_COLOR
        self.line_width = settings.SPACETIME_LINE_WIDTH

        coordinates = np.arange(
            -self.size / 2.0,
            self.size / 2.0 + self.step * 0.5,
            self.step,
            dtype=np.float32,
        )

        segments = []

        for fixed in coordinates:
            for i in range(len(coordinates) - 1):
                a = coordinates[i]
                b = coordinates[i + 1]

                segments.append([a, 0.0, fixed])
                segments.append([b, 0.0, fixed])

                segments.append([fixed, 0.0, a])
                segments.append([fixed, 0.0, b])

        self.base_vertices = np.asarray(segments, dtype=np.float32)
        self.vertices = self.base_vertices.copy()

    def update(self, star_a, star_b):
        self.vertices = self.base_vertices.copy()

        if not settings.SPACETIME_VISIBLE:
            return self.vertices

        x = self.base_vertices[:, 0].astype(np.float64)
        z = self.base_vertices[:, 2].astype(np.float64)

        height = np.full_like(
            x,
            settings.SPACETIME_BASE_HEIGHT,
        )

        for star in (star_a, star_b):
            star_x = star.position[0] / settings.AU
            star_z = star.position[2] / settings.AU

            dx = x - star_x
            dz = z - star_z

            distance = np.sqrt(
                dx * dx
                + dz * dz
                + settings.SPACETIME_SOFTENING ** 2
            )

            depth = (
                settings.SPACETIME_CURVATURE_STRENGTH
                * star.mass
                / settings.SOLAR_MASS
            )

            height -= depth / distance

        self.vertices[:, 1] = height.astype(np.float32)
        return self.vertices

    def get_vertices(self):
        return self.vertices

    def get_color(self):
        return self.color

    def get_line_width(self):
        return self.line_width