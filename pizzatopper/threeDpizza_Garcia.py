'''
Fork developed by Andrew Garcia
'''
import pyvista as pv
import numpy as np

class Chef:
    def __init__(self):
        
        self.pizza_radius = 1
        self.pizza_base = pv.Cylinder(radius=self.pizza_radius, height=0.15)
        self.texture_coords = np.array([[0., 0.],
                                [1., 0.],
                                [1., 1.],
                                [0., 1.]])

        self.toppings_chosen = ['Pepperoni', 'Mushrooms', 'Onions']
        self.toppings = ['Pepperoni', 'Mushrooms', 'Onions', 'Sausage', 'Bacon', 'Extra cheese', 'Black olives', 'Green peppers', 'Pineapple', 'Spinach']
        self.toppings_dict = {top: idx for idx, top in enumerate(self.toppings) }            
        # self.topping_preferences = [60,5,20,25,50,30.0,5,5,5,5]
        self.topping_preferences = np.ones(10)
        

    def make_topping(self,coords):
        toppings = [
            eval("pv.Cylinder(center=[0.07, {}, {}], radius=0.1, height=0.1)".format(*coords)),  # pepperoni
            eval("pv.Sphere(center=[0.07, {}, {}], radius=0.08)".format(*coords)),  # mushrooms
            eval("pv.Cylinder(center=[0.07, {}, {}], radius=0.015, height=0.1, direction=(0.0, 0.0, 1.0))".format(*coords)),  # onions
            eval("pv.PlatonicSolid(center=[0.07, {}, {}], kind='dodecahedron', radius=0.07)".format(*coords)),  # sausage
            eval("pv.Plane(center=[0.09, {}, {}], i_size=0.09, j_size=0.27, i_resolution=1, j_resolution=1,direction=(1, 0, 0))".format(*coords)),  # bacon
            eval("pv.PlatonicSolid(center=[0.07, {}, {}], kind='dodecahedron', radius=0.05)".format(*coords)),  # extra cheese
            eval("pv.Disc(center=[0.08, {}, {}], inner=0.025, outer=0.05,normal=(1, 0, 0), c_res=30)".format(*coords)),  # black olives 
            eval("pv.Cylinder(center=[0.07, {}, {}], radius=0.03, height=0.1, direction=(0.0, 1.0, 1.0))".format(*coords)),  # green peppers 
            eval("pv.PlatonicSolid(center=[0.07, {}, {}], kind='octahedron', radius=0.1)".format(*coords)), # pineapple
            eval("pv.Cylinder(center=[0.07, {}, {}], radius=0.02, height=0.2, direction=(0.0, 1.0, 1.0))".format(*coords)),   # spinach 
        ]
        return toppings

    def model(self):

        self.pizza_base.t_coords = self.texture_coords

        # Add some texture to the pizza base
        tex = pv.read_texture("pizzatopper/textures/pizza_texture.png")
        tex.InterpolateOn()
        tex.MipmapOn()

        topping_textures = [pv.read_texture("pizzatopper/textures/"+i) for i in ["pepperoni.jpg","mushroom.jpeg","onion.jpg","sausage.jpg","pineapple.jpg","olives.jpg"]]
        for i in topping_textures:
            i.InterpolateOn()
            i.MipmapOn()

        colors=["red","lightgray","purple","brown","darkred","lightyellow","black","green","yellow","darkgreen"]

        # mesh.textures["pizza_texture"] = texture

        # Render the mesh
        pl = pv.Plotter()
        pl.add_mesh(self.pizza_base,texture=tex)

        topping_probs = np.array(self.topping_preferences)
        topping_probs /= topping_probs.sum()

        def throw_topping():
            xycoords = np.random.uniform(-0.75, 0.8, 2)
            while np.sqrt(np.sum(xycoords**2)) > 0.9*self.pizza_radius:
                xycoords = np.random.uniform(-0.75, 0.8, 2)

            topping = self.make_topping(xycoords)[i]
            topping.t_coords = self.texture_coords

            return topping
        
        topping_idcs = [self.toppings_dict[i] for i in self.toppings_chosen]

        for i in np.random.choice(topping_idcs,size=100):

            if i != 5:
                #if topping is not extra cheese
                topping = throw_topping()

                if i == 0:
                    pl.add_mesh(topping,texture=topping_textures[i])
                else:
                    pl.add_mesh(topping,color=colors[i])
                

            else:
                #if topping is cheese, add 20 cheese morsels per sampling of this topping
                for j in range(20):
                    topping = throw_topping()

                    pl.add_mesh(topping,color=colors[i])        

        background_color='#cccccc'
        pl.background_color = background_color
        pl.show()

