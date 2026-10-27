===
INARY STAR SYSTEM SIMULATION
===

A real-time 3D simulation of the Sirius binary star system, built with Python, ModernGL, NumPy, and Pygame.

This project combines astronomy, physics, mathematics, and real-time graphics to explore the behavior of a binary star system in a three-dimensional environment.


WHAT YOU CAN SEE
----------------

- Sirius A and Sirius B — a visualization of the two stars in a binary star system.
- Orbital motion — the stars' movement through space, represented using a physics-based approach.
- 3D space visualization — a real-time environment that allows you to explore the system from a three-dimensional perspective.
- Spacetime curvature — a visual representation of how mass can be associated with the curvature of spacetime.
- Real-time rendering — the scene is rendered using ModernGL and OpenGL, with Pygame handling the application window and user input.

The goal is to bring mathematical and physical concepts to life in an interactive environment rather than simply displaying a static model of a star system.


CONTROLS
--------

W             Move forward
A             Move left
S             Move backward
D             Move right

SPACE         Move upward
SHIFT         Move downward

MOUSE WHEEL   Zoom in and out

1             Decrease movement speed
2             Increase movement speed

3             Slow down simulation time
4             Speed up simulation time

Movement speed determines how quickly you can navigate through the 3D environment, while simulation speed controls how quickly the simulated system evolves over time.

This allows you to explore the star system at different scales and observe its motion at a slower or faster pace.


CUSTOMIZATION AND EXPERIMENTATION
---------------------------------

The settings.py file contains many configuration options that allow you to customize different aspects of the simulation.

Depending on the available settings, you can experiment with parameters related to the simulation, rendering, camera, movement, and other aspects of the environment without having to rewrite the entire application.

Feel free to explore the settings and adjust values to see how they affect the simulation. Experimenting with different configurations is a great way to learn more about the code and how the individual components work together.

IMPORTANT: Before making changes, create a backup of the original settings.py file or, preferably, a complete copy of the entire project.

You can use the copied project as a separate experimental version. This way, you can try new values, test ideas, and make changes without risking your original working version.

If something breaks or the simulation stops working, you can return to the untouched original or restore your backup.

Keep the original project safe and use the copy for experimentation!


PHYSICS AND MATHEMATICS
-----------------------

Physics is an important part of this project. The simulation is designed around actual mathematical and physical equations rather than relying entirely on predefined animations.

Depending on the component, calculations can involve concepts such as gravitational interaction, orbital motion, vectors, coordinate transformations, and numerical integration.

The underlying idea is to calculate the behavior of the simulated objects using mathematical rules and then visualize the resulting motion in real time.

The spacetime visualization is intended to help illustrate the relationship between mass and spacetime curvature. It is a visual model, not a complete general-relativistic simulation.

The implementation uses Python and NumPy for numerical calculations, while ModernGL handles GPU-based rendering. This separation allows the physics and visualization components to work together without being the same thing.


TECHNOLOGIES
------------

Python 3.13.15
    The main programming language.

ModernGL 5.13.0
    GPU-accelerated rendering through OpenGL.

NumPy 2.5.3
    Numerical calculations and mathematical operations.

Pygame 2.6.1
    Application window, input handling, and the main application loop.


HOW TO START THE SIMULATION
----------------------------

There are two ways to start the simulation:

**Option 1: Run it using Python**

Open the project folder in VS Code or another code editor, open the integrated terminal, and run:

python main.py


Make sure Python and all required libraries are installed before starting the simulation.

**Option 2: Run the executable**

Navigate to the `dist` folder and double-click the `.exe` file to launch the simulation directly, without having to run the Python script manually.


REQUIREMENTS
------------

Python: 3.13.15 or newer
Tested version: 3.13.15

The required Python packages and their versions are listed in requirements.txt.


INSTALLATION
------------

1. Make sure Python 3.13.15 is installed.

2. Clone or download this repository.

3. Open a terminal in the project directory.

4. Install the required libraries by running:

   python -m pip install -r requirements.txt

5. Run the simulation using the project's main Python file.


DEVELOPMENT APPROACH
--------------------

Most of this project was developed through AI-assisted coding, often referred to as "vibe coding". However, it was not simply a matter of asking an AI to generate code and accepting whatever it produced.

I provided detailed instructions about how the simulation should work, how its different components should interact, and what I wanted to achieve visually and technically. I worked iteratively, refining ideas, addressing problems, and guiding the implementation toward the result I had in mind.

Throughout this process, I also learned a lot about the technologies involved, including Python, 3D rendering, numerical calculations, and the physical concepts behind the simulation. My goal was not just to get something running, but to understand how the different parts fit together and why they work the way they do.

AI was an important development tool, but the concept, direction, requirements, and decisions behind the project came from me. I see vibe coding as a way to build ambitious projects, explore unfamiliar concepts, and learn by experimenting — not as a replacement for understanding what you're building.


PROJECT STATUS
--------------

This project is an ongoing experiment and learning project. Features, calculations, and visualizations may change as I continue improving the simulation.


ACKNOWLEDGEMENTS
----------------

Built by me with AI-assisted development, curiosity, and a lot of experimentation.
