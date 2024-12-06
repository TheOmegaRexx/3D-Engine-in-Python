import pygame as pg  # Pygame for rendering
from matrix_functions import *  # Custom matrix operations (translation, rotation, scaling)
from numba import njit  # Numba for performance optimization with JIT compilation

# Optimized function using Numba to check if any element in an array equals specific values
# arr: The array to check
# a, b: The values to compare with
@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))

# Class representing a 3D object
class Object3D:
    def __init__(self, render, vertices='', faces=''):
        self.render = render  # Reference to the rendering engine
        self.vertices = np.array(vertices)  # Object's vertices in 3D space
        self.faces = faces  # Faces (connections between vertices)
        self.translate([0.0001, 0.0001, 0.0001])  # Small translation to avoid division by zero

        self.font = pg.font.SysFont('Arial', 30, bold=True)  # Font for rendering labels
        self.color_faces = [(pg.Color('white'), face) for face in self.faces]  # Assign colors to faces
        self.movement_flag = True  # Flag to enable or disable object movement
        self.draw_vertices = False  # Whether to draw vertices
        self.label = ''  # Label for object faces

    # Method to draw the object on the screen
    def draw(self):
        self.screen_projection()  # Project the 3D object to 2D screen coordinates
        self.movement()  # Handle object movement

    # Method to handle object movement (rotating in this case)
    def movement(self):
        if self.movement_flag:
            self.rotate_y(-(pg.time.get_ticks() % 0.005))  # Continuous rotation around the Y-axis

    # Project 3D vertices onto the 2D screen and draw faces and vertices
    def screen_projection(self):
        vertices = self.vertices @ self.render.camera.camera_matrix()  # Transform vertices by camera matrix
        vertices = vertices @ self.render.projection.projection_matrix  # Apply projection matrix
        vertices /= vertices[:, -1].reshape(-1, 1)  # Normalize by the w component
        vertices[(vertices > 2) | (vertices < -2)] = 0  # Clip vertices outside the view frustum
        vertices = vertices @ self.render.projection.to_screen_matrix  # Convert to screen coordinates
        vertices = vertices[:, :2]  # Extract 2D coordinates (x, y)

        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            polygon = vertices[face]  # Get polygon for the face
            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):  # Check if polygon is within bounds
                pg.draw.polygon(self.render.screen, color, polygon, 1)  # Draw the face
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color('white'))  # Render face label
                    self.render.screen.blit(text, polygon[-1])  # Place the label on the face

        if self.draw_vertices:  # If vertex drawing is enabled
            for vertex in vertices:
                if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):  # Check vertex bounds
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 2)  # Draw the vertex

    # Translate the object by a given vector
    def translate(self, pos):
        self.vertices = self.vertices @ translate(pos)

    # Scale the object uniformly
    def scale(self, scale_to):
        self.vertices = self.vertices @ scale(scale_to)

    # Rotate the object around the X-axis
    def rotate_x(self, angle):
        self.vertices = self.vertices @ rotate_x(angle)

    # Rotate the object around the Y-axis
    def rotate_y(self, angle):
        self.vertices = self.vertices @ rotate_y(angle)

    # Rotate the object around the Z-axis
    def rotate_z(self, angle):
        self.vertices = self.vertices @ rotate_z(angle)

# Class for rendering the coordinate axes
class Axes(Object3D):
    def __init__(self, render):
        super().__init__(render)
        # Define vertices for axes: origin and unit points on X, Y, and Z axes
        self.vertices = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        # Define connections (lines) between the origin and unit points
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        # Assign colors to each axis: red for X, green for Y, blue for Z
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertices = False  # Don't draw vertices for the axes
        self.label = 'XYZ'  # Labels for the axes
