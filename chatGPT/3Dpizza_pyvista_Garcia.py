'''
Fork developed by Andrew Garcia
'''
import pyvista as pv
import numpy as np

# Create a sphere to represent the pizza base
# pizza_base = pv.Sphere(radius=0.5)
pizza_radius = 1
pizza_base = pv.Cylinder(radius=pizza_radius, height=0.15)

# Create 6 smaller spheres to represent the toppings
toppings_data = { 0: "pv.Cylinder(center=[0.07, 0.7, 0], radius=0.1, height=0.1)"}

def make_topping(coords):
    toppings = [
        eval("pv.Cylinder(center=[0.07, {}, {}], radius=0.1, height=0.1)".format(*coords)),  # pepperoni
        eval("pv.Sphere(center=[0.07, {}, {}], radius=0.08)".format(*coords)),  # mushroom
        eval("pv.Cylinder(center=[0.07, {}, {}], radius=0.03, height=0.1)".format(*coords)),  # onion
        eval("pv.PlatonicSolid(center=[0.07, {}, {}], kind='dodecahedron', radius=0.1)".format(*coords)),  # sausage
        eval("pv.PlatonicSolid(center=[0.07, {}, {}], kind='octahedron', radius=0.1)".format(*coords)), # pineapple
        eval("pv.Disc(center=[0.08, {}, {}], inner=0.025, outer=0.05,normal=(1, 0, 0), c_res=30)".format(*coords)),  # olives
    ]
    return toppings
# Combine the pizza base and toppings into a single mesh
# mesh = pizza_base + toppings
texture_coords = np.array([[0., 0.],
                          [1., 0.],
                          [1., 1.],
                          [0., 1.]])

pizza_base.t_coords = texture_coords


# Add some texture to the pizza base
tex = pv.read_texture("pizza_texture.png")
tex.InterpolateOn()
tex.MipmapOn()

topping_textures = [pv.read_texture(i) for i in ["pepperoni.jpg","mushroom.jpeg","onion.jpg","sausage.jpg","pineapple.jpg","olives.jpg"]]
# for i in topping_textures:
#     i.InterpolateOn()
#     i.MipmapOn()

colors=["red","lightgray","purple","brown","yellow","black"]

# mesh.textures["pizza_texture"] = texture

# Render the mesh
pl = pv.Plotter()
pl.add_mesh(pizza_base,texture=tex)

topping_probs = np.array([60,5,20,25,10,30.0])
topping_probs /= topping_probs.sum()

for i in np.random.choice([i for i in range(6)],size=60,p=topping_probs):

    xycoords = np.random.uniform(-0.75, 0.8, 2)
    while np.sqrt(np.sum(xycoords**2)) > pizza_radius:
        xycoords = np.random.uniform(-0.75, 0.8, 2)

    topping = make_topping(xycoords)[i]
    topping.t_coords = texture_coords

    if i == 0:
        pl.add_mesh(topping,texture=topping_textures[i])
    else:
        pl.add_mesh(topping,color=colors[i])

background_color='#cccccc'
pl.background_color = background_color
pl.show()
