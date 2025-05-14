import re
from rules import rules_base, Rule

def ask_yes_no_question(question, known_facts, disproven_facts):
    if question in known_facts:
        return known_facts[question]
    if question in disproven_facts:
        return False
    response = input(f"{question} (yes/no): ").strip().lower()
    known_facts[question] = (response == 'yes')
    if not known_facts[question]:
        disproven_facts.add(question)
    return known_facts[question]

def ask_multiple_choice_question(question, choices, known_facts):
    if question in known_facts:
        return known_facts[question]
    print(f"{question}:")
    for i, choice in enumerate(choices, 1):
        print(f"{i}. {choice}")
    selected = int(input("Select one: ").strip())
    known_facts[question] = choices[selected - 1]
    return choices[selected - 1]

def forward_chaining(rules, known_facts):
    facts = set(known_facts.keys())
    disproven_facts = set()
    asked_premises = set()
    goal_proven = False

    while not goal_proven:
        new_facts_added = False
        for rule in rules:
            if rule.logical_operator == "AND":
                if any(premise in disproven_facts for premise in rule.premises):
                    continue  # Skip this rule if any premise has been disproven

                all_premises_true = True
                for premise in rule.premises:
                    if premise not in facts and premise not in disproven_facts:
                        if ask_yes_no_question(premise, known_facts, disproven_facts):
                            facts.add(premise)
                        else:
                            disproven_facts.add(premise)
                            all_premises_true = False
                            break  # Stop asking further premises for this rule

                if all_premises_true and not all(conclusion in facts for conclusion in rule.conclusions):
                    facts.update(rule.conclusions)
                    new_facts_added = True
                    if "X is a Local (Golden)" in facts:
                        goal_proven = True
                        break

            elif rule.logical_operator == "OR":
                if not any(premise in facts for premise in rule.premises):
                    # Ask multiple choice question if none of the premises are known
                    answer = ask_multiple_choice_question("Select the option that applies to you", rule.premises,
                                                          known_facts)
                    facts.add(answer)
                    disproven_facts.update(set(rule.premises) - {answer})
                if any(premise in facts for premise in rule.premises) and not all(
                        conclusion in facts for conclusion in rule.conclusions):
                    facts.update(rule.conclusions)
                    new_facts_added = True
                    if "X is a Local (Golden)" in facts:
                        goal_proven = True
                        break

        if goal_proven:
            break
        if not new_facts_added:
            break

    return facts


def backward_chaining(goal: str, known_facts: list[str], rules_base: list[Rule]) -> bool:
    #Performs backward chaining with backtracking to prove a goal.
    backward_chaining_path = []

    print("\nBackward chaining with backtracking...")
    backward_chaining_backtracking(goal, rules_base, backward_chaining_path)

    print(f"\nBackward chaining path : {backward_chaining_path}")

    return all(fact in backward_chaining_path for fact in known_facts)


def backward_chaining_backtracking(goal: str, rules_base: list[Rule], backward_chaining_path: list[str],
                                   depth: int = 0):
    # Recursive function for backward chaining with backtracking.
    indent = "  " * depth
    print(f"{indent}Fact: {goal}")
    backward_chaining_path.append(goal)

    for rule in rules_base:
        if goal in rule.conclusions:
            for premise in rule.premises:
                backward_chaining_backtracking(premise, rules_base, backward_chaining_path, depth + 1)


# Example Usage
if __name__ == "__main__":
    # goal = "X is a Local (Golden)"
    goal = "X is a Red Alien"
    known_facts = {}

    # Perform forward chaining to gather initial facts
    initial_facts = forward_chaining(rules_base, known_facts)

    # Check the goal using backward chaining
    if backward_chaining(goal, list(initial_facts), rules_base):
        print("Goal proven!")
    else:
        print("Goal not proven.")

    print("\nFinal conclusions based on your answers:")
    for fact in initial_facts:
        print(fact)
