import pygame as pg
from matrix_functions import *  # Import custom matrix operations

# Camera class to handle movement, rotation, and perspective calculations
class Camera:
    def __init__(self, render, position):
        # Initialize camera attributes
        self.render = render  # Reference to the rendering system
        self.position = np.array([*position, 1.0])  # Camera position as a 4D vector
        self.forward = np.array([0, 0, 1, 1])  # Forward direction vector
        self.up = np.array([0, 1, 0, 1])  # Up direction vector
        self.right = np.array([1, 0, 0, 1])  # Right direction vector

        # Field of view (FOV) and viewing frustum settings
        self.h_fov = math.pi / 3  # Horizontal FOV
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)  # Vertical FOV adjusted for aspect ratio
        self.near_plane = 0.1  # Distance to the near clipping plane
        self.far_plane = 100  # Distance to the far clipping plane

        # Movement and rotation speeds
        self.moving_speed = 0.3  # Speed of camera movement
        self.rotation_speed = 0.015  # Speed of camera rotation

        # Angles for pitch, yaw, and roll
        self.anglePitch = 0  # Rotation around the X-axis
        self.angleYaw = 0  # Rotation around the Y-axis
        self.angleRoll = 0  # Rotation around the Z-axis

    # Handle camera controls using keyboard input
    def control(self):
        key = pg.key.get_pressed()  # Get the current state of all keys
        # Movement controls
        if key[pg.K_a]:  # Move left
            self.position -= self.right * self.moving_speed
        if key[pg.K_d]:  # Move right
            self.position += self.right * self.moving_speed
        if key[pg.K_w]:  # Move forward
            self.position += self.forward * self.moving_speed
        if key[pg.K_s]:  # Move backward
            self.position -= self.forward * self.moving_speed
        if key[pg.K_q]:  # Move up
            self.position += self.up * self.moving_speed
        if key[pg.K_e]:  # Move down
            self.position -= self.up * self.moving_speed

        # Rotation controls
        if key[pg.K_LEFT]:  # Rotate left (yaw)
            self.camera_yaw(-self.rotation_speed)
        if key[pg.K_RIGHT]:  # Rotate right (yaw)
            self.camera_yaw(self.rotation_speed)
        if key[pg.K_UP]:  # Rotate up (pitch)
            self.camera_pitch(-self.rotation_speed)
        if key[pg.K_DOWN]:  # Rotate down (pitch)
            self.camera_pitch(self.rotation_speed)

    # Rotate the camera around the Y-axis (yaw)
    def camera_yaw(self, angle):
        self.angleYaw += angle

    # Rotate the camera around the X-axis (pitch)
    def camera_pitch(self, angle):
        self.anglePitch += angle

    # Reset the camera's direction vectors to their initial values
    def axiiIdentity(self):
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

    # Update the camera's direction vectors based on current rotation angles
    def camera_update_axii(self):
        rotate = rotate_x(self.anglePitch) @ rotate_y(self.angleYaw)  # Combined rotation matrix
        self.axiiIdentity()  # Reset direction vectors
        self.forward = self.forward @ rotate  # Apply rotation to forward vector
        self.right = self.right @ rotate  # Apply rotation to right vector
        self.up = self.up @ rotate  # Apply rotation to up vector

    # Create the camera matrix (translation and rotation combined)
    def camera_matrix(self):
        self.camera_update_axii()  # Update direction vectors
        return self.translate_matrix() @ self.rotate_matrix()  # Combine translation and rotation matrices

    # Create the translation matrix based on the camera's position
    def translate_matrix(self):
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    # Create the rotation matrix based on the camera's direction vectors
    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])