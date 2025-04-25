# Name: Ben Croyle
# Topic: Decision Theory

from hmm import KitchenHMM
from hmm import hmm

def DecisionTheory():
    result = hmm()['current_state']
    if result == "On track":
        print("Business is going well as usual")
    elif result == "Slightly behind":
        print("We may need some help")
    elif result == "Severely behind":
        print("Please send help ASAP")

DecisionTheory()