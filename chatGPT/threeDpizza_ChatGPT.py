'''
Prompt: Write a working, simple Python script that uses Pyvista to make a 3-D model of a pizza with the 6 most popular toppings in the world

ChatGPT: Sure, here's a simple Python script that uses Pyvista to create a 3D model of a pizza with 6 popular toppings:
'''

import pyvista as pv

# Create a sphere to represent the pizza base
pizza_base = pv.Sphere(radius=1)

# Create 6 smaller spheres to represent the toppings
toppings = [
    pv.Sphere(center=[0.7, 0.7, 0], radius=0.3),  # pepperoni
    pv.Sphere(center=[-0.7, -0.7, 0], radius=0.3),  # mushroom
    pv.Sphere(center=[-0.7, 0.7, 0], radius=0.3),  # onion
    pv.Sphere(center=[0.7, -0.7, 0], radius=0.3),  # sausage
    pv.Sphere(center=[0, 0, 0.7], radius=0.3),  # pineapple
    pv.Sphere(center=[0, 0, -0.7], radius=0.3),  # olives
]

# Combine the pizza base and toppings into a single mesh
mesh = pizza_base + toppings

# Add some texture to the pizza base
texture = pv.read_texture("pizza_texture.jpg")
mesh.textures["pizza_texture"] = texture

# Render the mesh
p = pv.Plotter()
p.add_mesh(mesh, texture="pizza_texture")
p.show()
