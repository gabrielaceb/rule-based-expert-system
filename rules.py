from dataclasses import dataclass

@dataclass
class Rule:
    premises: list[str]
    conclusions: list[str]
    logical_operator: str = "AND"

    def __str__(self):
        operator = f" {self.logical_operator} "  # Create a string with the logical operator padded with spaces for formatting in the output.
        return f"IF {operator.join(self.premises)} THEN {' AND '.join(self.conclusions)}" # Construct and return the string in the form: IF (conditions) ELSE (conclusions).

# Alien Classification Rules
rules_base = [
    Rule(
        premises=["X does have golden eyes", "X does have human characteristics"],
        conclusions=["X is a Local (Golden)"]
    ),
    Rule(
        premises=["X has red skin", "X has blue skin", "X has grey skin", "X has green skin", "X has violet skin"],
        conclusions=["X is an Alien"],
        logical_operator="OR"
    ),
    Rule(
        premises=["X is an Alien", "X performs manual labor", "X is considered lower class"],
        conclusions=["X is a Red Alien"]
    ),
    Rule(
        premises=["X is an Alien", "X works in a scientific field", "X has high intelligence"],
        conclusions=["X is a Blue Alien"]
    ),
    Rule(
        premises=["X is an Alien", "X is skilled in technology", "X works in engineering"],
        conclusions=["X is a Grey Alien"]
    ),
    Rule(
        premises=["X is an Alien", "X is involved in agriculture", "X grows and harvests crops"],
        conclusions=["X is a Green Alien"]
    ),
    Rule(
        premises=["X is an Alien", "X is involved in medical professions",
                  "X cares for the sick and injured"],
        conclusions=["X is a Violet Alien"]
    ),

]



