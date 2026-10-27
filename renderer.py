
import math

import moderngl
import numpy as np
import pygame

import settings
import shaders


class Renderer:
    def __init__(self, ctx):
        self.ctx = ctx

        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.enable(moderngl.BLEND)
        self.ctx.enable(moderngl.PROGRAM_POINT_SIZE)

        self.ctx.blend_func = (
            moderngl.SRC_ALPHA,
            moderngl.ONE_MINUS_SRC_ALPHA,
        )

        self.star_program = ctx.program(
            vertex_shader=shaders.STAR_VERTEX_SHADER,
            fragment_shader=shaders.STAR_FRAGMENT_SHADER,
        )

        self.line_program = ctx.program(
            vertex_shader=shaders.LINE_VERTEX_SHADER,
            fragment_shader=shaders.LINE_FRAGMENT_SHADER,
        )

        self.star_buffer = ctx.buffer(reserve=12)
        self.star_vao = ctx.vertex_array(
            self.star_program,
            [(self.star_buffer, "3f", "in_position")],
        )

        self.grid_buffer = None
        self.grid_vao = None
        self.grid_size_bytes = 0

        self.orbit_buffers = []
        self.orbit_vaos = []

        self.projection = np.eye(4, dtype=np.float32)

    @staticmethod
    def _matrix_bytes(matrix):
        return np.asarray(
            matrix,
            dtype=np.float32,
        ).T.copy().tobytes()

    def _create_projection(self):
        width, height = pygame.display.get_window_size()
        width = max(width, 1)
        height = max(height, 1)

        aspect = width / height
        f = 1.0 / math.tan(math.radians(settings.FOV) / 2.0)

        near = settings.NEAR_PLANE
        far = settings.FAR_PLANE

        matrix = np.zeros((4, 4), dtype=np.float32)
        matrix[0, 0] = f / aspect
        matrix[1, 1] = f
        matrix[2, 2] = (far + near) / (near - far)
        matrix[2, 3] = (2.0 * far * near) / (near - far)
        matrix[3, 2] = -1.0

        return matrix

    def _set_matrices(self, program, camera):
        program["view"].write(
            self._matrix_bytes(camera.get_view_matrix())
        )
        program["projection"].write(
            self._matrix_bytes(self.projection)
        )

    def _update_grid_buffer(self, vertices):
        data = np.ascontiguousarray(
            vertices,
            dtype=np.float32,
        )

        if data.nbytes == 0:
            return

        if (
            self.grid_buffer is None
            or self.grid_size_bytes != data.nbytes
        ):
            if self.grid_vao is not None:
                self.grid_vao.release()

            if self.grid_buffer is not None:
                self.grid_buffer.release()

            self.grid_buffer = self.ctx.buffer(data.tobytes())
            self.grid_vao = self.ctx.vertex_array(
                self.line_program,
                [(self.grid_buffer, "3f", "in_position")],
            )

            self.grid_size_bytes = data.nbytes
        else:
            self.grid_buffer.write(data.tobytes())

    def _prepare_orbits(self, orbit_points):
        for points in orbit_points:
            data = np.ascontiguousarray(
                points,
                dtype=np.float32,
            )

            buffer = self.ctx.buffer(data.tobytes())
            vao = self.ctx.vertex_array(
                self.line_program,
                [(buffer, "3f", "in_position")],
            )

            self.orbit_buffers.append(buffer)
            self.orbit_vaos.append(vao)

    def _draw_star(self, star, camera):
        position = np.asarray(
            star.position / settings.AU,
            dtype=np.float32,
        ).copy()

        position[1] += settings.ORBIT_HEIGHT

        self.star_buffer.write(position.tobytes())

        self._set_matrices(self.star_program, camera)

        self.star_program["star_radius"].value = star.render_radius
        self.star_program["star_screen_size_multiplier"].value = (
            settings.STAR_SCREEN_SIZE_MULTIPLIER
        )
        self.star_program["star_screen_size_min"].value = (
            settings.STAR_SCREEN_SIZE_MIN
        )
        self.star_program["star_screen_size_max"].value = (
            settings.STAR_SCREEN_SIZE_MAX
        )

        self.star_program["star_color"].value = tuple(
            channel / 255.0
            for channel in star.color[:3]
        )

        self.star_program["glow_intensity"].value = (
            star.glow * settings.STAR_GLOW_INTENSITY
        )

        self.ctx.disable(moderngl.DEPTH_TEST)

        self.ctx.blend_func = (
            moderngl.SRC_ALPHA,
            moderngl.ONE,
        )

        self.star_vao.render(
            mode=moderngl.POINTS,
            vertices=1,
        )

        self.ctx.blend_func = (
            moderngl.SRC_ALPHA,
            moderngl.ONE_MINUS_SRC_ALPHA,
        )

        self.ctx.enable(moderngl.DEPTH_TEST)

    def render(self, camera, stars, grid_vertices, orbit_points):
        width, height = pygame.display.get_window_size()
        self.ctx.viewport = (0, 0, width, height)

        self.ctx.clear(
            settings.BACKGROUND_COLOR[0] / 255.0,
            settings.BACKGROUND_COLOR[1] / 255.0,
            settings.BACKGROUND_COLOR[2] / 255.0,
            1.0,
            depth=1.0,
        )

        self.projection = self._create_projection()

        if settings.SPACETIME_VISIBLE:
            self._update_grid_buffer(grid_vertices)

            if self.grid_vao is not None:
                self._set_matrices(self.line_program, camera)

                self.line_program["line_color"].value = tuple(
                    channel / 255.0
                    for channel in settings.SPACETIME_COLOR[:3]
                )

                self.line_program["opacity"].value = 0.8
                self.ctx.line_width = settings.SPACETIME_LINE_WIDTH

                self.grid_vao.render(mode=moderngl.LINES)

        if settings.ORBIT_VISIBLE:
            if not self.orbit_vaos:
                self._prepare_orbits(orbit_points)

            self._set_matrices(self.line_program, camera)

            self.line_program["line_color"].value = tuple(
                channel / 255.0
                for channel in settings.ORBIT_COLOR[:3]
            )

            self.line_program["opacity"].value = (
                settings.ORBIT_ALPHA / 255.0
            )

            self.ctx.line_width = settings.ORBIT_LINE_WIDTH

            for vao in self.orbit_vaos:
                vao.render(mode=moderngl.LINE_STRIP)

        for star in stars:
            self._draw_star(star, camera)

    def release(self):
        self.star_vao.release()
        self.star_buffer.release()
        self.star_program.release()
        self.line_program.release()

        if self.grid_vao is not None:
            self.grid_vao.release()

        if self.grid_buffer is not None:
            self.grid_buffer.release()

        for vao in self.orbit_vaos:
            vao.release()

        for buffer in self.orbit_buffers:
            buffer.release()