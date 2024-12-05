import math
import numpy as np  # Import NumPy for matrix operations

# Creates a translation matrix for moving an object in 3D space
# pos: A tuple (tx, ty, tz) representing translation along the X, Y, and Z axes
def translate(pos):
    tx, ty, tz = pos
    return np.array([
        [1, 0, 0, 0],  # No scaling or rotation in the X direction
        [0, 1, 0, 0],  # No scaling or rotation in the Y direction
        [0, 0, 1, 0],  # No scaling or rotation in the Z direction
        [tx, ty, tz, 1]  # Translate the object by (tx, ty, tz)
    ])

# Creates a rotation matrix around the X-axis
# a: The angle in radians to rotate
def rotate_x(a):
    return np.array([
        [1, 0, 0, 0],  # No change to the X-axis
        [0, math.cos(a), math.sin(a), 0],  # Rotation in the YZ plane
        [0, -math.sin(a), math.cos(a), 0],  # Rotation in the YZ plane
        [0, 0, 0, 1]  # No change to position
    ])

# Creates a rotation matrix around the Y-axis
# a: The angle in radians to rotate
def rotate_y(a):
    return np.array([
        [math.cos(a), 0, -math.sin(a), 0],  # Rotation in the XZ plane
        [0, 1, 0, 0],  # No change to the Y-axis
        [math.sin(a), 0, math.cos(a), 0],  # Rotation in the XZ plane
        [0, 0, 0, 1]  # No change to position
    ])

# Creates a rotation matrix around the Z-axis
# a: The angle in radians to rotate
def rotate_z(a):
    return np.array([
        [math.cos(a), math.sin(a), 0, 0],  # Rotation in the XY plane
        [-math.sin(a), math.cos(a), 0, 0],  # Rotation in the XY plane
        [0, 0, 1, 0],  # No change to the Z-axis
        [0, 0, 0, 1]  # No change to position
    ])

# Creates a scaling matrix to uniformly scale an object in 3D space
# n: The scaling factor (uniform for all axes)
def scale(n):
    return np.array([
        [n, 0, 0, 0],  # Scale in the X direction
        [0, n, 0, 0],  # Scale in the Y direction
        [0, 0, n, 0],  # Scale in the Z direction
        [0, 0, 0, 1]  # No change to position
    ])