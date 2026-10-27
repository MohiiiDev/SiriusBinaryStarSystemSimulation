
import math

import moderngl
import numpy as np
import pygame

import settings
from camera import Camera
from physics import BinaryStarPhysics
from renderer import Renderer
from spacetime import SpacetimeGrid
from stars import create_sirius_system


def calculate_orbit_points(star_index, star_a, star_b):
    total_mass = star_a.mass + star_b.mass
    eccentricity = settings.ORBIT_ECCENTRICITY

    if star_index == 0:
        axis = (
            settings.SEMI_MAJOR_AXIS_AU
            * star_b.mass / total_mass
        )
        direction = -1.0
    else:
        axis = (
            settings.SEMI_MAJOR_AXIS_AU
            * star_a.mass / total_mass
        )
        direction = 1.0

    angles = np.linspace(
        0.0,
        2.0 * math.pi,
        settings.ORBIT_POINT_COUNT,
        endpoint=True,
    )

    radius = axis * (1.0 - eccentricity**2) / (
        1.0 + eccentricity * np.cos(angles)
    )

    points = np.zeros((len(angles), 3), dtype=np.float32)

    points[:, 0] = direction * radius * np.cos(angles)
    points[:, 1] = settings.ORBIT_HEIGHT
    points[:, 2] = direction * radius * np.sin(angles)

    return points


def main():
    pygame.init()

    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_MAJOR_VERSION, 3
    )
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_MINOR_VERSION, 3
    )
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK,
        pygame.GL_CONTEXT_PROFILE_CORE,
    )
    pygame.display.gl_set_attribute(
        pygame.GL_DEPTH_SIZE, 24
    )
    pygame.display.gl_set_attribute(
        pygame.GL_DOUBLEBUFFER, 1
    )

    pygame.display.set_mode(
        (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT),
        pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE,
        vsync=1 if settings.VSYNC else 0,
    )

    pygame.display.set_caption(settings.WINDOW_TITLE)

    ctx = moderngl.create_context()

    star_a, star_b = create_sirius_system()
    stars = [star_a, star_b]

    physics = BinaryStarPhysics(star_a, star_b)
    camera = Camera()
    spacetime = SpacetimeGrid()
    renderer = Renderer(ctx)

    orbit_points = [
        calculate_orbit_points(0, star_a, star_b),
        calculate_orbit_points(1, star_a, star_b),
    ]

    time_scale = settings.INITIAL_TIME_SCALE
    clock = pygame.time.Clock()
    running = True

    camera.capture_mouse()

    try:
        while running:
            frame_dt = min(
                clock.tick(settings.FPS) / 1000.0,
                0.05,
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if camera.mouse_captured:
                            camera.release_mouse()
                        else:
                            running = False

                    elif event.key == pygame.K_3:
                        time_scale = max(
                            settings.MIN_TIME_SCALE,
                            time_scale / settings.TIME_SCALE_FACTOR,
                        )

                    elif event.key == pygame.K_4:
                        time_scale = min(
                            settings.MAX_TIME_SCALE,
                            time_scale * settings.TIME_SCALE_FACTOR,
                        )

                camera.handle_event(event)

            if not running:
                break

            camera.update(frame_dt)

            physics.advance(
                frame_dt * time_scale,
                settings.PHYSICS_SUBSTEPS,
            )

            grid_vertices = spacetime.update(star_a, star_b)

            renderer.render(
                camera,
                stars,
                grid_vertices,
                orbit_points,
            )

            pygame.display.flip()

            elapsed_years = physics.elapsed_time / settings.YEAR
            speed_years = time_scale / settings.YEAR

            pygame.display.set_caption(
                f"{settings.WINDOW_TITLE} | "
                f"Simulation: {elapsed_years:.2f} years | "
                f"Speed: {speed_years:.3f} years/s"
            )

    finally:
        camera.release_mouse()
        renderer.release()
        ctx.release()
        pygame.quit()


if __name__ == "__main__":
    main()