# Jordan Scott, Adonijah Farner, and Benjamin Croyle

# Here is where we will put together the code from Bayes’ Net, Hiddden Markov Model, and Decision Theeory.

# Import the necessary modules
from bayes_net import posterior_state_distribution
from hmm import KitchenHMM
from decision_theory import DecisionTheory


# 1. Get your Bayes‐Net output
evidence = { 'Staffing':'low', 'TimeOfDay':'peak' }
bayes_post = posterior_state_distribution(evidence)

# 2. Pull out π in the HMM’s order
kitchen_hmm = KitchenHMM()
pi_vector = [ bayes_post[s] for s in kitchen_hmm.states ]

# 3. Inject into the HMM
kitchen_hmm.set_initial_probabilities(pi_vector)