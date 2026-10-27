
from dataclasses import dataclass, field

import numpy as np

import settings


@dataclass
class Star:
    name: str
    mass: float
    radius: float
    color: tuple
    render_radius: float
    glow: float

    position: np.ndarray = field(
        default_factory=lambda: np.zeros(3, dtype=np.float64)
    )
    velocity: np.ndarray = field(
        default_factory=lambda: np.zeros(3, dtype=np.float64)
    )
    acceleration: np.ndarray = field(
        default_factory=lambda: np.zeros(3, dtype=np.float64)
    )

    def __post_init__(self):
        self.position = np.asarray(
            self.position, dtype=np.float64
        ).copy()
        self.velocity = np.asarray(
            self.velocity, dtype=np.float64
        ).copy()
        self.acceleration = np.asarray(
            self.acceleration, dtype=np.float64
        ).copy()

    @property
    def gravitational_parameter(self):
        return settings.G * self.mass

    def reset_acceleration(self):
        self.acceleration.fill(0.0)


def create_sirius_system():
    star_a = Star(
        name="Sirius A",
        mass=settings.STAR_A_MASS,
        radius=settings.STAR_A_RADIUS,
        color=settings.STAR_A_COLOR,
        render_radius=settings.STAR_A_RENDER_RADIUS,
        glow=settings.STAR_A_GLOW,
    )

    star_b = Star(
        name="Sirius B",
        mass=settings.STAR_B_MASS,
        radius=settings.STAR_B_RADIUS,
        color=settings.STAR_B_COLOR,
        render_radius=settings.STAR_B_RENDER_RADIUS,
        glow=settings.STAR_B_GLOW,
    )

    return star_a, star_b