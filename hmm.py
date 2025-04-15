# Name: Jordan Scott 
# Topic: Hidden Markov Model

# Purpose: Model the kitchen's state as it evolves, using:
# Hidden Markov Model (HMM): Tracking Kitchen State Over Time
# Purpose: Model the kitchen's state as it evolves, using:
# Hidden States: "On track," "Slightly behind," "Severely behind."
# Observations: Metrics like time to deliver orders (fast, average, slow) or number of complaints (low, medium, high).
# Integration: Use the Bayes' Net output as initial state probabilities, then update the state based on a sequence of observations

import numpy as np

class KitchenHMM:
    def __init__(self):
        # Define states
        self.states = ["On track", "Slightly behind", "Severely behind"]
        self.n_states = len(self.states)
        
        # Define possible observations
        self.observations = ["Fast delivery, low complaints", 
                            "Average delivery, medium complaints", 
                            "Slow delivery, high complaints"]
        self.n_observations = len(self.observations)
        
        # Initialize transition probability matrix (A)
        # A[i][j] = probability of transitioning from state i to state j
        self.A = np.array([
            [0.7, 0.2, 0.1],  # From "On track"
            [0.3, 0.5, 0.2],  # From "Slightly behind"
            [0.1, 0.3, 0.6]   # From "Severely behind"
        ])
        
        # Initialize emission probability matrix (B)
        # B[i][j] = probability of observing j when in state i
        self.B = np.array([
            [0.7, 0.2, 0.1],  # "On track" state
            [0.2, 0.6, 0.2],  # "Slightly behind" state
            [0.1, 0.3, 0.6]   # "Severely behind" state
        ])
        
        # Initial state probabilities (π)
        # Default values - can be updated with Bayes' Net output
        self.pi = np.array([0.6, 0.3, 0.1])
    
    def set_initial_probabilities(self, probabilities):
        """Update initial state probabilities based on Bayes' Net output"""
        if len(probabilities) != self.n_states:
            raise ValueError(f"Expected {self.n_states} probabilities, got {len(probabilities)}")
        if not np.isclose(sum(probabilities), 1.0):
            raise ValueError(f"Probabilities must sum to 1, got {sum(probabilities)}")
        self.pi = np.array(probabilities)
    
    def forward_algorithm(self, observations):
        """
        Implements the forward algorithm to compute the probability of an observation sequence
        and determine the most likely current state.
        
        Args:
            observations: List of observation indices (0, 1, 2 corresponding to the observation types)
            
        Returns:
            Probability distribution over states after the observation sequence
        """
        T = len(observations)
        alpha = np.zeros((T, self.n_states))
        
        # Initialize
        alpha[0] = self.pi * self.B[:, observations[0]]
        
        # Forward pass
        for t in range(1, T):
            for j in range(self.n_states):
                alpha[t, j] = np.sum(alpha[t-1] * self.A[:, j]) * self.B[j, observations[t]]
        
        # Normalize to get probabilities
        final_probs = alpha[-1] / np.sum(alpha[-1])
        return final_probs
    
    def viterbi_algorithm(self, observations):
        """
        Implements the Viterbi algorithm to find the most likely sequence of states
        given a sequence of observations.
        
        Args:
            observations: List of observation indices (0, 1, 2 corresponding to the observation types)
            
        Returns:
            Most likely sequence of states
        """
        T = len(observations)
        delta = np.zeros((T, self.n_states))
        psi = np.zeros((T, self.n_states), dtype=int)
        
        # Initialize
        delta[0] = self.pi * self.B[:, observations[0]]
        
        # Recursion
        for t in range(1, T):
            for j in range(self.n_states):
                delta[t, j] = np.max(delta[t-1] * self.A[:, j]) * self.B[j, observations[t]]
                psi[t, j] = np.argmax(delta[t-1] * self.A[:, j])
        
        # Backtracking
        q_star = np.zeros(T, dtype=int)
        q_star[T-1] = np.argmax(delta[T-1])
        
        for t in range(T-2, -1, -1):
            q_star[t] = psi[t+1, q_star[t+1]]
        
        # Convert indices to state names
        state_sequence = [self.states[int(q)] for q in q_star]
        return state_sequence
    
    def get_observation_index(self, delivery_time, complaint_level):
        """
        Maps delivery time and complaint level to an observation index.
        
        Args:
            delivery_time: "fast", "average", or "slow"
            complaint_level: "low", "medium", or "high"
            
        Returns:
            Observation index (0, 1, or 2)
        """
        if delivery_time == "fast" and complaint_level == "low":
            return 0
        elif delivery_time == "average" and complaint_level == "medium":
            return 1
        elif delivery_time == "slow" and complaint_level == "high":
            return 2
        else:
            # For simplicity, map other combinations to the closest category
            if delivery_time == "fast" or complaint_level == "low":
                return 0
            elif delivery_time == "average" or complaint_level == "medium":
                return 1
            else:
                return 2
    
    def predict_kitchen_state(self, observation_sequence):
        """
        Predicts the current kitchen state based on a sequence of observations.
        
        Args:
            observation_sequence: List of tuples (delivery_time, complaint_level)
            
        Returns:
            Current most likely state and probability distribution
        """
        # Convert observations to indices
        observation_indices = [self.get_observation_index(dt, cl) for dt, cl in observation_sequence]
        
        # Get state probabilities
        state_probs = self.forward_algorithm(observation_indices)
        most_likely_state = self.states[np.argmax(state_probs)]
        
        # Get most likely state sequence
        state_sequence = self.viterbi_algorithm(observation_indices)
        
        return {
            "current_state": most_likely_state,
            "state_probabilities": {state: prob for state, prob in zip(self.states, state_probs)},
            "state_sequence": state_sequence
        }


def hmm():
    """
    Main function to demonstrate the HMM for kitchen performance tracking.
    """
    # Initialize the HMM
    kitchen_hmm = KitchenHMM()
    
    # Example: Set initial probabilities from a Bayes' Net
    # kitchen_hmm.set_initial_probabilities([0.7, 0.2, 0.1])
    
    # Example observation sequence: [(delivery_time, complaint_level), ...]
    observation_sequence = [
        ("fast", "low"),       # Good performance
        ("average", "medium"), # Average performance
        ("average", "medium"), # Average performance
        ("slow", "high")       # Poor performance
    ]
    
    # Predict kitchen state
    result = kitchen_hmm.predict_kitchen_state(observation_sequence)
    
    print("Kitchen Performance HMM Analysis:")
    print(f"Current most likely state: {result['current_state']}")
    print("\nState probabilities:")
    for state, prob in result['state_probabilities'].items():
        print(f"  {state}: {prob:.2f}")
    
    print("\nMost likely state sequence:")
    for i, state in enumerate(result['state_sequence']):
        print(f"  Time {i+1}: {state}")
    
    return result


if __name__ == "__main__":
    hmm()
