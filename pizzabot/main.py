import numpy as np
from scipy.stats import beta
import json

class Bot:
    def __init__(self):
        pass

        # Define the prior distribution over toppings
        # Here, we assume that every topping is equally likely
        self.prior_alpha = np.ones(10)
        self.prior_beta = np.ones(10)

        # Define the likelihood function for each topping
        # Here, we assume that the likelihood of a topping is proportional to its popularity
        self.likelihoods = np.array([0.2, 0.1, 0.15, 0.05, 0.1, 0.05, 0.1, 0.1, 0.05, 0.1])

        self.toppings = ['Pepperoni', 'Mushrooms', 'Onions', 'Sausage', 'Bacon', 'Extra cheese', 'Black olives', 'Green peppers', 'Pineapple', 'Spinach']

        dtoppings = dict(enumerate(self.toppings))
        pretty_json = json.dumps(dtoppings, indent=4)
        print('TOPPINGS\n----------------------------\n',pretty_json)


    def update_posterior(self, data):
        # Compute the posterior alpha and beta parameters using the prior and likelihood
        posterior_alpha = self.prior_alpha + data
        posterior_beta = self.prior_beta + (1 - data)
        return posterior_alpha, posterior_beta


    def make_choices(self):
        # Ask the user for their pizza preferences
        print("What are your favorite pizza toppings?")
        print('Choose indices separated by commas (e.g. 0,5,3,4)')
        preferences = [self.toppings[int(i)] for i in input().split(',')  ]
        # print(preferences)

        # Convert the user's preferences to a binary vector
        # Here, we assume that the user likes a topping if it is in their list of preferences
        user_vector = np.array([1 if i in preferences else 0 for i in self.toppings])

        # Update the posterior distribution using the user's preferences
        posterior_alpha, posterior_beta = self.update_posterior(user_vector * self.likelihoods)

        
        # Compute the posterior mean for each topping
        posterior_means = beta.mean(posterior_alpha, posterior_beta)

        # Print the recommended toppings based on the posterior means
        recommendations = sorted(zip(self.toppings, posterior_means/posterior_means.sum() ), key=lambda x: x[1], reverse=True)[:10]
        print("\nWe think you'd like these toppings the most:\nRANKING (by preference %)\n-------------------------")

        k=1
        # recommendations[1] = np.cumsum(recommendations[1])

        for topping, probability in recommendations:
            print(f"#{k} || {self.toppings.index(topping)} : {topping} ({probability*100:.2f}%)")
            k+=1

        # Update priors for next iteration (if desired)
        self.prior_alpha, self.prior_beta = posterior_alpha, posterior_beta

    def run(self):
        #init 
        self.make_choices()

        print("Would you like to make other choices based on our recommendations [(y)/n]?")
        answer = input()
        while answer != 'n':
            self.run()