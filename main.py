from object_3d import *
from camera import *
from projection import *
import pygame as pg

# Main class for software rendering
class SoftwareRender:
    def __init__(self):
        # Initialize Pygame and basic settings
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900  # Screen resolution
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2  # Half width and height for centered rendering
        self.FPS = 60  # Frames per second
        self.screen = pg.display.set_mode(self.RES)  # Create the Pygame window
        self.clock = pg.time.Clock()  # Pygame clock for controlling FPS
        self.create_objects()  # Create and initialize objects

    # Creates and initializes the camera, projection, and 3D objects
    def create_objects(self):
        self.camera = Camera(self, [-5, 6, -55])  # Initialize camera with position
        self.projection = Projection(self)  # Create projection object
        self.object = self.get_object_from_file('resources/object.obj')  # Load 3D object from file
        self.object.rotate_y(-math.pi / 4)  # Rotate object around the Y-axis

    # Loads a 3D object from a file in .obj format
    def get_object_from_file(self, filename):
        vertex, faces = [], []  # Lists for vertices and faces
        with open(filename) as f:  # Open the file in read mode
            for line in f:  # Iterate through each line of the file
                if line.startswith('v '):  # If the line describes a vertex
                    vertex.append([float(i) for i in line.split()[1:]] + [1])  # Add vertex data
                elif line.startswith('f'):  # If the line describes a face
                    faces_ = line.split()[1:]  # Extract face definitions
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])  # Add face indices
        return Object3D(self, vertex, faces)  # Create and return the 3D object

    # Draws the current frame
    def draw(self):
        self.screen.fill(pg.Color('black'))  # Set screen background color
        self.object.draw()  # Draw the 3D object

    # Main program loop
    def run(self):
        while True:
            self.draw()  # Draw the current frame
            self.camera.control()  # Execute camera controls
            [exit() for i in pg.event.get() if i.type == pg.QUIT]  # Exit the program if the window is closed
            pg.display.set_caption(str(self.clock.get_fps()))  # Display FPS in the window title
            pg.display.flip()  # Update the screen
            self.clock.tick(self.FPS)  # Wait to maintain the desired FPS

# Entry point if the script is executed directly
if __name__ == '__main__':
    app = SoftwareRender()  # Create an instance of the SoftwareRender class
    app.run()  # Run the main program
