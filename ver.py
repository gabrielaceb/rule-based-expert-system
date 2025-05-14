import re
from typing import Dict, Set, List
from rules import rules_base, Rule

def ask_yes_no_question(question: str, known_facts: Dict[str, bool], disproven_facts: Set[str]) -> bool:
    while True:
        if question in known_facts:
            return known_facts[question]
        if question in disproven_facts:
            return False
        response = input(f"{question} (yes/no): ").strip().lower()
        if response in ['yes', 'no']:
            result = response == 'yes'
            known_facts[question] = result
            if not result:
                disproven_facts.add(question)
            return result
        print("Invalid input. Please answer 'yes' or 'no'.")

def ask_multiple_choice_question(question: str, choices: List[str], known_facts: Dict[str, str]) -> str:
    if question in known_facts:
        return known_facts[question]
    print(f"{question}:")
    for i, choice in enumerate(choices, 1):
        print(f"{i}. {choice}")
    while True:
        try:
            selected = int(input("Select one: ").strip()) - 1
            if 0 <= selected < len(choices):
                known_facts[question] = choices[selected]
                return choices[selected]
            else:
                print("Invalid selection. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def forward_chaining(rules: List[Rule], known_facts: Dict[str, bool]) -> Set[str]:
    facts = set(known_facts.keys())
    disproven_facts = set()
    new_facts_added = True

    while new_facts_added:
        new_facts_added = False
        for rule in rules:
            if rule_applicable(rule, facts, disproven_facts):
                new_facts, goal_proven = apply_rule(rule, known_facts, disproven_facts, facts)
                if new_facts:
                    new_facts_added = True
                if goal_proven:
                    return facts
    return facts

def rule_applicable(rule: Rule, facts: Set[str], disproven_facts: Set[str]) -> bool:
    if rule.logical_operator == "AND":
        return not any(premise in disproven_facts for premise in rule.premises)
    elif rule.logical_operator == "OR":
        return not any(premise in facts for premise in rule.premises)
    return False

def apply_rule(rule: Rule, known_facts: Dict[str, bool], disproven_facts: Set[str], facts: Set[str]) -> (bool, bool):
    goal_proven = False
    if rule.logical_operator == "AND":
        if all([ask_yes_no_question(premise, known_facts, disproven_facts) for premise in rule.premises]):
            facts.update(rule.conclusions)
            goal_proven = "X is a Local (Golden)" in rule.conclusions
    elif rule.logical_operator == "OR":
        chosen_fact = ask_multiple_choice_question("Select the option that applies to you", rule.premises, known_facts)
        facts.add(chosen_fact)
        disproven_facts.update(set(rule.premises) - {chosen_fact})
        facts.update(rule.conclusions)
        goal_proven = "X is a Local (Golden)" in rule.conclusions
    return len(rule.conclusions - facts) > 0, goal_proven

# Usage example if you wish to run the code from here
if __name__ == "__main__":
    goal = "X is a Red Alien"
    known_facts = {}
    initial_facts = forward_chaining(rules_base, known_facts)
    print("\nFinal conclusions based on your answers:")
    for fact in initial_facts:
        print(fact)


# import re
# from rules import rules_base, Rule
#
#
# def ask_yes_no_question(question, known_facts, disproven_facts):
#     if question in known_facts:
#         return known_facts[question]
#     if question in disproven_facts:
#         return False
#     response = input(f"{question} (yes/no): ").strip().lower()
#     known_facts[question] = (response == 'yes')
#     if not known_facts[question]:
#         disproven_facts.add(question)
#     return known_facts[question]
#
#
# def ask_multiple_choice_question(question, choices, known_facts):
#     if question in known_facts:
#         return known_facts[question]
#     print(f"{question}:")
#     for i, choice in enumerate(choices, 1):
#         print(f"{i}. {choice}")
#     selected = int(input("Select one: ").strip())
#     known_facts[question] = choices[selected - 1]
#     return choices[selected - 1]
#
#
# def forward_chaining(rules, known_facts):
#     facts = set(known_facts.keys())
#     disproven_facts = set()
#
#     goal_proven = False
#     while not goal_proven:
#         new_facts_added = False
#         for rule in rules:
#             if rule.logical_operator == "AND":
#                 if any(premise in disproven_facts for premise in rule.premises):
#                     continue  # Skip this rule if any premise has been disproven
#
#                 all_premises_true = True
#                 for premise in rule.premises:
#                     if premise not in facts and premise not in disproven_facts:
#                         if ask_yes_no_question(premise, known_facts, disproven_facts):
#                             facts.add(premise)
#                         else:
#                             disproven_facts.add(premise)
#                             all_premises_true = False
#                             break  # Stop asking further premises for this rule
#
#                 if all_premises_true and not all(conclusion in facts for conclusion in rule.conclusions):
#                     facts.update(rule.conclusions)
#                     new_facts_added = True
#                     if "X is a Local (Golden)" in facts:
#                         goal_proven = True
#                         break
#
#             elif rule.logical_operator == "OR":
#                 if not any(premise in facts for premise in rule.premises):
#                     # Ask multiple choice question if none of the premises are known
#                     answer = ask_multiple_choice_question("Select the option that applies to you", rule.premises,
#                                                           known_facts)
#                     facts.add(answer)
#                     disproven_facts.update(set(rule.premises) - {answer})
#                 if any(premise in facts for premise in rule.premises) and not all(
#                         conclusion in facts for conclusion in rule.conclusions):
#                     facts.update(rule.conclusions)
#                     new_facts_added = True
#                     if "X is a Local (Golden)" in facts:
#                         goal_proven = True
#                         break
#
#         if goal_proven:
#             break
#         if not new_facts_added:
#             break
#
#     return facts
#
#
# def backward_chaining(goal: str, known_facts: dict, rules_base: list[Rule]) -> bool:
#     """Performs backward chaining with backtracking to prove a goal."""
#     backward_chaining_path = []
#     disproven_facts = set()
#
#     print("\nBackward chaining with backtracking...")
#     result = backward_chaining_backtracking(goal, rules_base, backward_chaining_path, known_facts, disproven_facts)
#
#     print(f"\nBackward chaining path: {backward_chaining_path}")
#
#     return result
#
#
# def backward_chaining_backtracking(goal: str, rules_base: list[Rule], backward_chaining_path: list[str],
#                                    known_facts: dict, disproven_facts: set, depth: int = 0) -> bool:
#     """Recursive function for backward chaining with backtracking."""
#     indent = "  " * depth
#     print(f"{indent}Fact: {goal}")
#     backward_chaining_path.append(goal)
#
#     if goal in known_facts:
#         return known_facts[goal]
#     if goal in disproven_facts:
#         return False
#
#     for rule in rules_base:
#         if goal in rule.conclusions:
#             all_premises_true = True
#             for premise in rule.premises:
#                 if premise in disproven_facts:
#                     return False
#                 if premise not in known_facts:
#                     if not backward_chaining_backtracking(premise, rules_base, backward_chaining_path, known_facts,
#                                                           disproven_facts, depth + 1):
#                         disproven_facts.add(premise)
#                         all_premises_true = False
#                         break
#             if all_premises_true:
#                 known_facts[goal] = True
#                 return True
#
#     disproven_facts.add(goal)
#     return False
#
#
# def match(pattern: str, fact: str) -> bool:
#     """Matches a pattern (with variables) against a fact."""
#     pattern = pattern.replace("(?x)", r"\b\w+\b")  # Match word boundaries
#     return re.match(pattern, fact) is not None
#
#
# # Example Usage
# if __name__ == "__main__":
#     goal = "X is a Red Alien"
#     known_facts = {}
#
#     # Perform forward chaining to gather initial facts
#     initial_facts = forward_chaining(rules_base, known_facts)
#
#     # Check the goal using backward chaining
#     if backward_chaining(goal, known_facts, rules_base):
#         print("Goal proven!")
#     else:
#         print("Goal not proven.")
#
#     print("\nFinal conclusions based on your answers:")
#     for fact in known_facts:
#         if known_facts[fact]:
#             print(fact)
