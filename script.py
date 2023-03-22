import numpy as np
from scipy.stats import beta

# Define the prior distribution over toppings
# Here, we assume that every topping is equally likely
prior_alpha = np.ones(10)
prior_beta = np.ones(10)

# Define the likelihood function for each topping
# Here, we assume that the likelihood of a topping is proportional to its popularity
likelihoods = np.array([0.2, 0.1, 0.15, 0.05, 0.1, 0.05, 0.1, 0.1, 0.05, 0.1])

def update_posterior(prior_alpha, prior_beta, data):
    # Compute the posterior alpha and beta parameters using the prior and likelihood
    posterior_alpha = prior_alpha + data
    posterior_beta = prior_beta + (1 - data)
    return posterior_alpha, posterior_beta

# Ask the user for their pizza preferences
print("What are your favorite pizza toppings?")
preferences = input().split(',')

# Convert the user's preferences to a binary vector
# Here, we assume that the user likes a topping if it is in their list of preferences
user_vector = np.array([1 if i in preferences else 0 for i in range(10)])

# Update the posterior distribution using the user's preferences
posterior_alpha, posterior_beta = update_posterior(prior_alpha, prior_beta, user_vector * likelihoods)

# Compute the posterior mean for each topping
posterior_means = beta.mean(posterior_alpha, posterior_beta)

# Print the recommended toppings based on the posterior means
toppings = ['Pepperoni', 'Mushrooms', 'Onions', 'Sausage', 'Bacon', 'Extra cheese', 'Black olives', 'Green peppers', 'Pineapple', 'Spinach']
recommendations = sorted(zip(toppings, posterior_means), key=lambda x: x[1], reverse=True)[:3]
print("We recommend trying the following toppings: ")
for topping, probability in recommendations:
    print(f"{topping} ({probability*100:.2f}%)")
