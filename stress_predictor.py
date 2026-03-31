# STUDENT STRESS PREDICTION SYSTEM

import math
from collections import deque
from sklearn.tree import DecisionTreeClassifier
import numpy as np

def get_user_input():
    print("\n--- Student Lifestyle Input ---")
    try:
        sleep = float(input("Hours of sleep (0 to 12): "))
        study = float(input("Hours of study (0 to 12): "))
        assignments = int(input("Assignments pending (0 to 10): "))
        mood = int(input("Mood level (1 to 5, where 1 = very low): "))

        return {
            "sleep": sleep,
            "study": study,
            "assignments": assignments,
            "mood": mood
        }

    except:
        print("Invalid input! Please enter numbers only.")
        return get_user_input()
# Rules expressed using propositional logic conditions
logic_rules = [
    ("HIGH",  lambda d: d["sleep"] < 5 and d["study"] > 6),
    ("HIGH",  lambda d: d["assignments"] > 5),
    ("MEDIUM",lambda d: 5 <= d["sleep"] <= 7 and d["study"] >= 4),
    ("MEDIUM",lambda d: d["mood"] <= 2),
    ("LOW",   lambda d: d["sleep"] >= 7 and d["study"] <= 4),
    ("LOW",   lambda d: d["assignments"] <= 2),
]

def rule_based_prediction(data):
    # BFS through rules (uninformed search)
    q = deque(logic_rules)

    counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}

    while q:
        stress_label, rule = q.popleft()
        if rule(data):
            counts[stress_label] += 1

    # Final label = highest matched rule
    final_label = max(counts, key=counts.get)

    return final_label, counts
# PROBABILITY CALCULATION (Conditional Probability)
sample_data = [
    {"sleep": 4, "assign": 6, "stress": "HIGH"},
    {"sleep": 5, "assign": 5, "stress": "MEDIUM"},
    {"sleep": 8, "assign": 1, "stress": "LOW"},
    {"sleep": 6, "assign": 4, "stress": "MEDIUM"},
    {"sleep": 7, "assign": 2, "stress": "LOW"},
    {"sleep": 3, "assign": 7, "stress": "HIGH"},
]

def conditional_probability(stress_label, condition_fn):
    total = 0
    match = 0

    for entry in sample_data:
        if condition_fn(entry):
            total += 1
            if entry["stress"] == stress_label:
                match += 1

    if total == 0:
        return 0

    return match / total

X = np.array([
    [4, 7, 6, 2],
    [6, 4, 5, 2],
    [7, 3, 1, 4],
    [5, 5, 4, 3],
    [8, 2, 1, 5],
    [3, 8, 7, 1],
])

y = np.array(["HIGH", "MEDIUM", "LOW", "MEDIUM", "LOW", "HIGH"])

model = DecisionTreeClassifier()
model.fit(X, y)
def ml_prediction(data):
    arr = np.array([[data["sleep"], data["study"], data["assignments"], data["mood"]]])
    return model.predict(arr)[0]


# MAIN ENGINE

def main():
    print("\n========== Student Stress Prediction System ==========\n")
    user_data = get_user_input()

    # Rule-based
    rule_label, rule_counts = rule_based_prediction(user_data)

    # ML-based
    ml_label = ml_prediction(user_data)

    # Conditional probability example
    prob_high = conditional_probability("HIGH", lambda d: d["sleep"] < 5)

    print("\n======= RESULTS =======")
    print(f"Rule-Based Prediction: {rule_label}")
    print(f"Rule Matches Count: {rule_counts}")

    print(f"\nMachine Learning Prediction: {ml_label}")

    print("\nProbabilistic Insight:")
    print(f"P(Stress=HIGH | sleep<5) = {prob_high:.2f}")

    print("\nFinal Recommendation:")
    if rule_label == ml_label:
 print(f"Final Stress Level = {rule_label} (Both methods agree)")
    else:
        print(f"Mixed signals → Final Level = {ml_label} (ML preferred)")

    print("\n===============================================\n")


main()
