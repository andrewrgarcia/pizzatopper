import pizzatopper as pizza

X = pizza.Bot()
X.run()

C = pizza.Chef()
C.toppings_chosen = X.recommended_toppings
C.model()