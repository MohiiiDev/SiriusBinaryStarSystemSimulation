
import math

import numpy as np

import settings


class BinaryStarPhysics:
    def __init__(self, star_a, star_b):
        self.stars = [star_a, star_b]
        self.elapsed_time = 0.0

        self._initialize_orbit()
        self._update_accelerations()

    def _initialize_orbit(self):
        star_a, star_b = self.stars

        total_mass = star_a.mass + star_b.mass
        semi_major_axis = settings.SEMI_MAJOR_AXIS_AU * settings.AU
        eccentricity = settings.ORBIT_ECCENTRICITY

        separation = semi_major_axis * (1.0 - eccentricity)

        relative_speed = math.sqrt(
            settings.G
            * total_mass
            * (1.0 + eccentricity)
            / (semi_major_axis * (1.0 - eccentricity))
        )

        star_a.position = np.array(
            [-separation * star_b.mass / total_mass, 0.0, 0.0],
            dtype=np.float64,
        )

        star_b.position = np.array(
            [separation * star_a.mass / total_mass, 0.0, 0.0],
            dtype=np.float64,
        )

        star_a.velocity = np.array(
            [0.0, 0.0, -relative_speed * star_b.mass / total_mass],
            dtype=np.float64,
        )

        star_b.velocity = np.array(
            [0.0, 0.0, relative_speed * star_a.mass / total_mass],
            dtype=np.float64,
        )

    def _update_accelerations(self):
        star_a, star_b = self.stars

        displacement = star_b.position - star_a.position
        distance_squared = float(np.dot(displacement, displacement))
        distance = math.sqrt(max(distance_squared, 1.0))

        direction = displacement / distance

        star_a.acceleration = (
            settings.G * star_b.mass / distance_squared
        ) * direction

        star_b.acceleration = (
            -settings.G * star_a.mass / distance_squared
        ) * direction

    def step(self, dt):
        half_dt = 0.5 * dt

        for star in self.stars:
            star.velocity += star.acceleration * half_dt
            star.position += star.velocity * dt

        self._update_accelerations()

        for star in self.stars:
            star.velocity += star.acceleration * half_dt

        self.elapsed_time += dt

    def advance(self, dt, substeps=None):
        if dt <= 0.0:
            return

        requested_steps = (
            settings.PHYSICS_SUBSTEPS
            if substeps is None
            else substeps
        )

        adaptive_steps = math.ceil(
            dt / settings.PHYSICS_TIME_STEP
        )

        count = max(1, requested_steps, adaptive_steps)
        step_dt = dt / count

        for _ in range(count):
            self.step(step_dt)

    def get_barycenter(self):
        star_a, star_b = self.stars
        total_mass = star_a.mass + star_b.mass

        return (
            star_a.position * star_a.mass
            + star_b.position * star_b.mass
        ) / total_mass

    def get_relative_separation(self):
        star_a, star_b = self.stars
        return float(np.linalg.norm(star_b.position - star_a.position))