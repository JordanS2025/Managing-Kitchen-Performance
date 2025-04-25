# Name: Ben Croyle
# Topic: Decision Theory
# Purpose: Output a message saying what to do based on how much on track the kitchen staff is.

from hmm import hmm

class DecisionTheory:
    def __init__(self):
        # Define possible actions
        self.actions = ["Do nothing", "Call extra staff", "Offer discounts"]
        
        # Define utility parameters
        self.utilities = {
            "On track": {
                "Do nothing": 1.0,
                "Call extra staff": -0.2,  # Unnecessary cost
                "Offer discounts": -0.3    # Unnecessary cost
            },
            "Slightly behind": {
                "Do nothing": -0.2,
                "Call extra staff": 0.5,   # Moderate cost, good benefit
                "Offer discounts": 0.3     # Low cost, moderate benefit
            },
            "Severely behind": {
                "Do nothing": -1.0,
                "Call extra staff": 0.8,   # High cost, but necessary
                "Offer discounts": 0.6     # Moderate cost, good benefit
            }
        }
        
        # Cost factors
        self.costs = {
            "Call extra staff": 0.3,  # Cost of additional labor
            "Offer discounts": 0.2,   # Cost of reduced revenue
            "Do nothing": 0.0         # No direct cost
        }
    
    def calculate_expected_utility(self, state_probabilities):
        """
        Calculate expected utility for each action based on state probabilities
        """
        expected_utilities = {}
        
        for action in self.actions:
            total_utility = 0.0
            for state, prob in state_probabilities.items():
                # Calculate net utility (utility - cost)
                net_utility = self.utilities[state][action] - self.costs[action]
                total_utility += prob * net_utility
            expected_utilities[action] = total_utility
        
        return expected_utilities
    
    def make_decision(self, state_probabilities):
        """
        Make the optimal decision based on current state probabilities
        """
        expected_utilities = self.calculate_expected_utility(state_probabilities)
        best_action = max(expected_utilities.items(), key=lambda x: x[1])[0]
        
        # Generate detailed explanation
        explanation = f"Decision Analysis:\n"
        for action, utility in expected_utilities.items():
            explanation += f"  {action}: {utility:.2f} expected utility\n"
        explanation += f"\nRecommended Action: {best_action}"
        
        return {
            "action": best_action,
            "expected_utilities": expected_utilities,
            "explanation": explanation
        }

def main():
    # Example usage
    from hmm import KitchenHMM
    
    # Initialize HMM and get state probabilities
    hmm = KitchenHMM()
    observation_sequence = [
        ("fast", "low"),
        ("average", "medium"),
        ("slow", "high")
    ]
    hmm_result = hmm.predict_kitchen_state(observation_sequence)
    
    # Make decision based on current state probabilities
    dt = DecisionTheory()
    decision = dt.make_decision(hmm_result["state_probabilities"])
    
    print("\nKitchen Performance Decision Analysis")
    print("=" * 40)
    print(decision["explanation"])

if __name__ == "__main__":
    main()