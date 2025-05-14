# Alien Classifier Expert System

This is a Python-based rule-driven system that determines whether an entity is a human or one of several alien types. It uses a custom `Rule` class and logical inference through a series of IF-THEN conditions.

## Features

- Defines rules using premises and conclusions
- Supports logical operators (AND)
- Easily extendable knowledge base
- Console interface for testing conditions

## Files

- `main.py` – Main program loop
- `rules.py` – Rule definitions and inference engine
- `utils.py` – Utility functions for string processing
- `production.py` – Production rules application (optional)

## Example

```python
Rule(
  premises=["X is an Alien", "X performs manual labor", "X is considered lower class"],
  conclusions=["X is a Red Alien"]
)
