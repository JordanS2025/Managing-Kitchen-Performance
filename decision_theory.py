"""
bayes_net.py

Bayesian Network for Kitchen Performance
Models the probability of kitchen state ("On track", "Slightly behind", "Severely behind")
based on factors: Staffing, Equipment, Order Complexity, Time of Day.
"""

import itertools

# Define variables
STAFFING_LEVELS = ['low', 'medium', 'high']
EQUIPMENT_STATUS = ['working', 'faulty']
ORDER_COMPLEXITY = ['simple', 'complex']
TIME_OF_DAY = ['off-peak', 'peak']

KITCHEN_STATES = ['On track', 'Slightly behind', 'Severely behind']

# Prior distributions for factors (adjust as needed)
PRIOR = {
    'Staffing': {'low': 0.2, 'medium': 0.5, 'high': 0.3},
    'Equipment': {'working': 0.9, 'faulty': 0.1},
    'OrderComplexity': {'simple': 0.6, 'complex': 0.4},
    'TimeOfDay': {'off-peak': 0.7, 'peak': 0.3}
}

def state_cpt(staffing, equipment, complexity, time_of_day):
    """
    Conditional probability P(KitchenState | factors) using a simple severity-based approach.
    severity score: low staffing=2, medium=1, high=0; faulty equipment=1; complex orders=1; peak=1
    P(On track) = max(0, 1 - severity/5)
    P(Severely behind) = severity/5
    P(Slightly behind) = 1 - P(On track) - P(Severely behind)
    """
    # map severity
    s_score = {'low':2, 'medium':1, 'high':0}[staffing]
    e_score = 1 if equipment == 'faulty' else 0
    o_score = 1 if complexity == 'complex' else 0
    t_score = 1 if time_of_day == 'peak' else 0
    severity = s_score + e_score + o_score + t_score
    max_sev = 5.0
    p_severe = severity / max_sev
    p_on_track = max(0.0, 1.0 - p_severe)
    p_slight = max(0.0, 1.0 - p_on_track - p_severe)
    return {
        'On track': p_on_track,
        'Slightly behind': p_slight,
        'Severely behind': p_severe
    }

def enumerate_all_states(evidence=None):
    """
    Enumerate joint distribution P(state, all factors) restricted by evidence.
    evidence: dict with some factor assignments.
    Returns dict mapping state to unnormalized probability.
    """
    if evidence is None:
        evidence = {}
    state_probs = {state: 0.0 for state in KITCHEN_STATES}
    # iterate over factor combinations consistent with evidence
    for staffing in STAFFING_LEVELS:
        if 'Staffing' in evidence and evidence['Staffing'] != staffing:
            continue
        p_staff = PRIOR['Staffing'][staffing]
        for equipment in EQUIPMENT_STATUS:
            if 'Equipment' in evidence and evidence['Equipment'] != equipment:
                continue
            p_equip = PRIOR['Equipment'][equipment]
            for complexity in ORDER_COMPLEXITY:
                if 'OrderComplexity' in evidence and evidence['OrderComplexity'] != complexity:
                    continue
                p_comp = PRIOR['OrderComplexity'][complexity]
                for t in TIME_OF_DAY:
                    if 'TimeOfDay' in evidence and evidence['TimeOfDay'] != t:
                        continue
                    p_time = PRIOR['TimeOfDay'][t]
                    # compute CPT
                    cpt = state_cpt(staffing, equipment, complexity, t)
                    for state, p_state_given in cpt.items():
                        state_probs[state] += p_state_given * p_staff * p_equip * p_comp * p_time
    return state_probs

def normalize(dist):
    """
    Normalize a distribution dict so that values sum to 1.
    """
    total = sum(dist.values())
    if total == 0:
        return dist
    return {k: v/total for k,v in dist.items()}

def initial_state_distribution():
    """
    Returns P(KitchenState) by marginalizing over all factors.
    """
    raw = enumerate_all_states()
    return normalize(raw)

def posterior_state_distribution(evidence):
    """
    Returns P(KitchenState | evidence) for given partial evidence on factors.
    evidence keys: 'Staffing', 'Equipment', 'OrderComplexity', 'TimeOfDay'
    """
    raw = enumerate_all_states(evidence)
    return normalize(raw)

if __name__ == '__main__':
    print("Initial Kitchen State Distribution:")
    for state, prob in initial_state_distribution().items():
        print(f"  {state}: {prob:.3f}")

    # example: given it's peak time and staffing is low
    evidence = {'TimeOfDay':'peak', 'Staffing':'low'}
    print("\nPosterior given evidence:", evidence)
    for state, prob in posterior_state_distribution(evidence).items():
        print(f"  {state}: {prob:.3f}")
