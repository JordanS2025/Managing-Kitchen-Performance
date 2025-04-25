# Kitchen Performance Management System

A sophisticated system that combines Bayesian Networks, Hidden Markov Models, and Decision Theory to monitor and optimize kitchen performance in a restaurant setting.

## Overview

This system provides a comprehensive approach to managing kitchen performance by:

1. Predicting kitchen states based on various factors
2. Tracking performance over time
3. Making optimal operational decisions

## Components

### 1. Bayesian Network (`bayes_net.py`)

- Models the probability of kitchen states based on:
  - Staffing levels (low, medium, high)
  - Equipment status (working, faulty)
  - Order complexity (simple, complex)
  - Time of day (off-peak, peak)
- Outputs initial state probabilities for the HMM

### 2. Hidden Markov Model (`hmm.py`)

- Tracks kitchen state evolution over time
- States:
  - "On track"
  - "Slightly behind"
  - "Severely behind"
- Observations:
  - Delivery times (fast, average, slow)
  - Customer complaints (low, medium, high)
- Uses forward and Viterbi algorithms for state prediction

### 3. Decision Theory (`decision_theory.py`)

- Makes operational decisions based on current state
- Available actions:
  - "Do nothing"
  - "Call extra staff"
  - "Offer discounts"
- Considers costs and benefits for each action

## Features

- **Real-time Monitoring**: Track kitchen performance throughout the day
- **Predictive Analysis**: Forecast potential issues before they occur
- **Decision Support**: Get actionable recommendations based on current conditions
- **Weekly Simulation**: Simulate a week's worth of kitchen operations with realistic variations
- **Customizable Parameters**: Adjust probabilities and thresholds to match your restaurant's needs

## Usage

1. Run the main simulation:

```bash
python main.py
```

2. The system will simulate a week of operations, showing:
   - Daily conditions (staffing, equipment, etc.)
   - Initial state probabilities
   - Observations throughout the day
   - Final state and recommended actions
   - Weekly summary

## Example Output

```
Kitchen Performance Weekly Analysis
==================================================

Day 1: Monday
------------------------------
Daily Conditions:
  Staffing: medium
  Equipment: working
  OrderComplexity: simple
  TimeOfDay: peak

Performance Analysis:
Initial State: On track
Final State: On track
State Probabilities:
  On track: 0.750
  Slightly behind: 0.200
  Severely behind: 0.050
Recommended Action: Do nothing
==================================================
```

## Requirements

- Python 3.x
- NumPy
- Standard Python libraries

## Authors

- Jordan Scott
- Adonijah Farner
- Benjamin Croyle

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on principles of Bayesian Networks, Hidden Markov Models, and Decision Theory
- Designed for practical application in restaurant management
