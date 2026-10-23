facts = {
    "temperature": 32,      # Category 1: Temperature
    "humidity": 85,         # Category 1: Temperature/Environment
    "is_raining": True,     # Category 2: Status
    "is_cloudy": True,      # Category 2: Status
    "user_present": True    # Category 3: Presence
}

def rule_hot(facts):
    if facts.get("temperature", 0) > 30 and facts.get("user_present", False):
        return "Turn on the aircon"
    return None

def rule_rain(facts):
    if facts.get("is_raining", False):
        return "Bring umbrella"
    return None

def rule_dehumidifier(facts):
    if facts.get("humidity", 0) > 80:
        return "Turn on dehumidifier"
    return None


def run_rbr_inference_engine(facts_db, rules_list):
    inferred_actions = []
    for rule in rules_list:
        action = rule(facts_db)
        if action:
            inferred_actions.append(action)
    
    print("Rule-Based Reasoning Actions:")
    for action in inferred_actions:
        print(f"- {action}")
    return inferred_actions

# Execute Demonstration
rules = [rule_hot, rule_rain, rule_dehumidifier]
run_rbr_inference_engine(facts, rules)
print("\n" + "="*40 + "\n")


case_base = [
    {
        "problem": {"won't turn on": True, "noise": False},
        "solution": "Check power cable."
    },
    {
        "problem": {"won't turn on": True, "noise": True},
        "solution": "Inspect fan motor for blockage."
    },
    {
        "problem": {"won't turn on": False, "noise": True},
        "solution": "Clean or replace fan bearings."
    }
]


def calculate_similarity(new_problem, case_problem):
    score = 0
    total_keys = set(new_problem.keys()).union(set(case_problem.keys()))
    for key in total_keys:
        if new_problem.get(key) == case_problem.get(key):
            score += 1
    return score / len(total_keys) if total_keys else 0.0


def retrieve_and_reuse(new_problem, case_base):
    best_match = None
    highest_score = -1.0
    
    for case in case_base:
        sim = calculate_similarity(new_problem, case["problem"])
        if sim > highest_score:
            highest_score = sim
            best_match = case
            
    print(f"[Retrieve & Reuse] Most similar case score: {highest_score * 100:.1f}%")
    return best_match["solution"] if best_match else "No solution found."


def revise_solution(proposed_solution, manual_adjustment=None):
    if manual_adjustment:
        print(f"[Revise] Solution manually updated from '{proposed_solution}' to '{manual_adjustment}'")
        return manual_adjustment
    print(f"[Revise] Proposed solution accepted without changes: '{proposed_solution}'")
    return proposed_solution


def retain_case(case_base, new_problem, final_solution):
    new_case = {
        "problem": new_problem,
        "solution": final_solution
    }
    case_base.append(new_case)
    print(f"[Retain] New case successfully learned and stored into Case Base.")


new_user_problem = {"won't turn on": True, "noise": False}
print(f"New Problem Input: {new_user_problem}")

# 1. Retrieve & Reuse
retrieved_sol = retrieve_and_reuse(new_user_problem, case_base)

# 2. Revise (Optionally pass custom string to revise)
final_sol = revise_solution(retrieved_sol, manual_adjustment="Check power cable and fuse box.")

# 3. Retain
retain_case(case_base, new_user_problem, final_sol)
