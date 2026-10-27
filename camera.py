
import math

import numpy as np
import pygame

import settings


class Camera:
    def __init__(self):
        self.position = settings.CAMERA_START_POSITION.copy()
        self.yaw = settings.CAMERA_START_YAW
        self.pitch = settings.CAMERA_START_PITCH
        self.speed = settings.CAMERA_START_SPEED
        self.mouse_sensitivity = settings.CAMERA_MOUSE_SENSITIVITY
        self.mouse_captured = False

        self.world_up = np.array(
            [0.0, 1.0, 0.0],
            dtype=np.float64,
        )

        self.forward = np.zeros(3, dtype=np.float64)
        self.right = np.zeros(3, dtype=np.float64)
        self.up = np.zeros(3, dtype=np.float64)

        self._update_vectors()

    def capture_mouse(self):
        self.mouse_captured = True
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        pygame.mouse.get_rel()

    def release_mouse(self):
        self.mouse_captured = False
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)

    def _update_vectors(self):
        yaw = math.radians(self.yaw)
        pitch = math.radians(self.pitch)

        self.forward = np.array(
            [
                math.cos(yaw) * math.cos(pitch),
                math.sin(pitch),
                math.sin(yaw) * math.cos(pitch),
            ],
            dtype=np.float64,
        )

        self.forward /= max(np.linalg.norm(self.forward), 1e-9)

        self.right = np.cross(self.forward, self.world_up)
        self.right /= max(np.linalg.norm(self.right), 1e-9)

        self.up = np.cross(self.right, self.forward)
        self.up /= max(np.linalg.norm(self.up), 1e-9)

    def rotate(self, dx, dy):
        self.yaw += dx * self.mouse_sensitivity
        self.pitch -= dy * self.mouse_sensitivity

        self.pitch = settings.clamp(
            self.pitch,
            -settings.CAMERA_PITCH_LIMIT,
            settings.CAMERA_PITCH_LIMIT,
        )

        self._update_vectors()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.speed = max(
                    settings.CAMERA_MIN_SPEED,
                    self.speed / settings.CAMERA_SPEED_FACTOR,
                )

            elif event.key == pygame.K_2:
                self.speed = min(
                    settings.CAMERA_MAX_SPEED,
                    self.speed * settings.CAMERA_SPEED_FACTOR,
                )

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.mouse_captured:
                self.capture_mouse()

        elif event.type == pygame.MOUSEWHEEL:
            self.position += (
                self.forward * self.speed * 0.1 * event.y
            )

        elif event.type == pygame.MOUSEMOTION:
            if self.mouse_captured:
                self.rotate(*event.rel)

        elif event.type == pygame.WINDOWFOCUSLOST:
            self.release_mouse()

    def update(self, dt):
        keys = pygame.key.get_pressed()
        movement = np.zeros(3, dtype=np.float64)

        if keys[pygame.K_w]:
            movement += self.forward
        if keys[pygame.K_s]:
            movement -= self.forward
        if keys[pygame.K_d]:
            movement += self.right
        if keys[pygame.K_a]:
            movement -= self.right
        if keys[pygame.K_SPACE]:
            movement += self.world_up
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            movement -= self.world_up

        length = np.linalg.norm(movement)

        if length > 1e-9:
            movement /= length
            self.position += movement * self.speed * dt

    def get_view_matrix(self):
        eye = self.position
        forward = self.forward

        side = np.cross(forward, self.world_up)
        side /= max(np.linalg.norm(side), 1e-9)

        corrected_up = np.cross(side, forward)
        corrected_up /= max(np.linalg.norm(corrected_up), 1e-9)

        view = np.eye(4, dtype=np.float32)

        view[0, :3] = side
        view[1, :3] = corrected_up
        view[2, :3] = -forward

        view[0, 3] = -np.dot(side, eye)
        view[1, 3] = -np.dot(corrected_up, eye)
        view[2, 3] = np.dot(forward, eye)

        return view