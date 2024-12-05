import math  # For mathematical operations (e.g., tangent)
import numpy as np  # For handling matrices and numerical computations


# The Projection class handles the creation of projection matrices for transforming 3D points to 2D screen coordinates.
class Projection:
    def __init__(self, render):
        # Extracting values from the camera object in the render engine
        NEAR = render.camera.near_plane  # Distance to the near clipping plane
        FAR = render.camera.far_plane  # Distance to the far clipping plane
        RIGHT = math.tan(render.camera.h_fov / 2)  # Right boundary of the frustum in view space
        LEFT = -RIGHT  # Left boundary (symmetric to the right)
        TOP = math.tan(render.camera.v_fov / 2)  # Top boundary of the frustum
        BOTTOM = -TOP  # Bottom boundary (symmetric to the top)

        # Calculating elements for the projection matrix
        # This matrix transforms 3D coordinates into normalized device coordinates (NDC)
        m00 = 2 / (RIGHT - LEFT)  # Scale factor for the X-axis
        m11 = 2 / (TOP - BOTTOM)  # Scale factor for the Y-axis
        m22 = (FAR + NEAR) / (FAR - NEAR)  # Perspective depth scaling
        m32 = -2 * NEAR * FAR / (FAR - NEAR)  # Depth translation for clipping

        # Constructing the projection matrix
        # Rows:
        # - Row 0: X-axis transformation
        # - Row 1: Y-axis transformation
        # - Row 2: Z-axis transformation for depth
        # - Row 3: Handles perspective divide
        self.projection_matrix = np.array([
            [m00, 0, 0, 0],
            [0, m11, 0, 0],
            [0, 0, m22, 1],
            [0, 0, m32, 0]
        ])

        # Screen dimensions (half-width and half-height)
        HW, HH = render.H_WIDTH, render.H_HEIGHT

        # Matrix for converting NDC coordinates to screen coordinates
        # Rows:
        # - Row 0: X-axis scaling and translation to the screen width
        # - Row 1: Y-axis scaling and flipping (to match screen space where Y increases downward)
        # - Row 2: Z-axis remains unchanged
        # - Row 3: Translation to the center of the screen
        self.to_screen_matrix = np.array([
            [HW, 0, 0, 0],
            [0, -HH, 0, 0],
            [0, 0, 1, 0],
            [HW, HH, 0, 1]
        ])