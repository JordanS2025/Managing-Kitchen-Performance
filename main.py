# Jordan Scott, Adonijah Farner, and Benjamin Croyle

# Here is where we will put together the code from Bayes' Net, Hidden Markov Model, and Decision Theory.

# Import the necessary modules
from bayes_net import posterior_state_distribution
from hmm import KitchenHMM
from decision_theory import DecisionTheory
import random
from datetime import datetime, timedelta

def generate_daily_conditions(day_of_week):
    """
    Generate realistic kitchen conditions for a given day of the week
    """
    # Base probabilities for different conditions
    staffing_probs = {
        'Monday': {'low': 0.3, 'medium': 0.5, 'high': 0.2},
        'Tuesday': {'low': 0.2, 'medium': 0.6, 'high': 0.2},
        'Wednesday': {'low': 0.2, 'medium': 0.5, 'high': 0.3},
        'Thursday': {'low': 0.1, 'medium': 0.4, 'high': 0.5},
        'Friday': {'low': 0.1, 'medium': 0.3, 'high': 0.6},
        'Saturday': {'low': 0.2, 'medium': 0.4, 'high': 0.4},
        'Sunday': {'low': 0.4, 'medium': 0.4, 'high': 0.2}
    }
    
    # Generate conditions based on day
    staffing = random.choices(['low', 'medium', 'high'], 
                            weights=list(staffing_probs[day_of_week].values()))[0]
    
    # Equipment status (usually working, but small chance of issues)
    equipment = 'working' if random.random() > 0.1 else 'faulty'
    
    # Order complexity (varies by day)
    complexity_probs = {
        'Monday': {'simple': 0.7, 'complex': 0.3},
        'Tuesday': {'simple': 0.6, 'complex': 0.4},
        'Wednesday': {'simple': 0.5, 'complex': 0.5},
        'Thursday': {'simple': 0.4, 'complex': 0.6},
        'Friday': {'simple': 0.3, 'complex': 0.7},
        'Saturday': {'simple': 0.4, 'complex': 0.6},
        'Sunday': {'simple': 0.6, 'complex': 0.4}
    }
    complexity = random.choices(['simple', 'complex'], 
                              weights=list(complexity_probs[day_of_week].values()))[0]
    
    return {
        'Staffing': staffing,
        'Equipment': equipment,
        'OrderComplexity': complexity,
        'TimeOfDay': 'peak' if random.random() > 0.5 else 'off-peak'
    }

def generate_observations(state):
    """
    Generate realistic observations based on the current state
    """
    # Observation probabilities based on state
    observation_probs = {
        'On track': {
            ('fast', 'low'): 0.7,
            ('average', 'medium'): 0.2,
            ('slow', 'high'): 0.1
        },
        'Slightly behind': {
            ('fast', 'low'): 0.2,
            ('average', 'medium'): 0.6,
            ('slow', 'high'): 0.2
        },
        'Severely behind': {
            ('fast', 'low'): 0.1,
            ('average', 'medium'): 0.3,
            ('slow', 'high'): 0.6
        }
    }
    
    # Generate 3 observations for the day
    observations = []
    for _ in range(3):
        obs = random.choices(
            list(observation_probs[state].keys()),
            weights=list(observation_probs[state].values())
        )[0]
        observations.append(obs)
    
    return observations

def run_weekly_simulation():
    """
    Run a week-long simulation of kitchen performance
    """
    print("\nKitchen Performance Weekly Analysis")
    print("=" * 50)
    
    # Initialize the HMM
    kitchen_hmm = KitchenHMM()
    
    # Get current date and simulate a week
    current_date = datetime.now()
    weekly_summary = []
    
    for day in range(7):
        date = current_date + timedelta(days=day)
        day_name = date.strftime('%A')
        
        print(f"\nDay {day + 1}: {day_name}")
        print("-" * 30)
        
        # Generate conditions for the day
        evidence = generate_daily_conditions(day_name)
        print("\nDaily Conditions:")
        for factor, value in evidence.items():
            print(f"  {factor}: {value}")
        
        # Get initial state probabilities
        bayes_post = posterior_state_distribution(evidence)
        pi_vector = [bayes_post[s] for s in kitchen_hmm.states]
        kitchen_hmm.set_initial_probabilities(pi_vector)
        
        # Generate observations for the day
        current_state = max(bayes_post.items(), key=lambda x: x[1])[0]
        observations = generate_observations(current_state)
        
        # Update state based on observations
        hmm_result = kitchen_hmm.predict_kitchen_state(observations)
        
        # Make decisions
        dt = DecisionTheory()
        decision = dt.make_decision(hmm_result["state_probabilities"])
        
        # Store daily summary
        daily_summary = {
            'day': day_name,
            'conditions': evidence,
            'initial_state': current_state,
            'final_state': hmm_result['current_state'],
            'action': decision['action'],
            'state_probabilities': hmm_result['state_probabilities']
        }
        weekly_summary.append(daily_summary)
        
        # Print daily results
        print("\nPerformance Analysis:")
        print(f"Initial State: {current_state}")
        print(f"Final State: {hmm_result['current_state']}")
        print("\nState Probabilities:")
        for state, prob in hmm_result["state_probabilities"].items():
            print(f"  {state}: {prob:.3f}")
        print(f"\nRecommended Action: {decision['action']}")
        print("=" * 50)
    
    return weekly_summary

def main():
    # Run the weekly simulation
    weekly_summary = run_weekly_simulation()
    
    # Print weekly summary
    print("\nWeekly Performance Summary")
    print("=" * 50)
    for day in weekly_summary:
        print(f"\n{day['day']}:")
        print(f"Initial State: {day['initial_state']}")
        print(f"Final State: {day['final_state']}")
        print(f"Action Taken: {day['action']}")
        print("-" * 30)

if __name__ == "__main__":
    main()