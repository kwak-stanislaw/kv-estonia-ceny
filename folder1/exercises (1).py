"""
exercises for class attributes
"""
# Class Attributes — Exercises
# Fill in each class so that the tests in test_exercises.py pass.
# Do NOT change method signatures or attribute names.



# Exercise 1 — Shared Constant
#
# Create a class `Circle` with:
#   - A class attribute `PI = 3.14159`
#   - An instance attribute `radius` set in __init__
#   - A method `area()` that returns PI * radius ** 2
#   - A method `circumference()` that returns 2 * PI * radius
#
# Both methods must use the class attribute PI (not a hard-coded number).

class Circle:
    PI = 3.14159

    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return self.PI * self.radius ** 2

    def circumference(self):
        return 2 * self.PI * self.radius

# Exercise 2 — Instance Counter
#
# Create a class `User` with:
#   - A class attribute `count = 0` tracking total instances created
#   - An instance attribute `username` set in __init__
#   - count must increase by 1 each time a new User is created
#   - A class method `reset()` that clears the registry
#     (for test isolation)

class User:
    count = 0

    def __init__(self, username):
        self.username = username
        User.count += 1

    @classmethod
    def reset(cls):
        cls.count = 0


# Exercise 3 — Default Config (overridable per instance)
#
# Create a class `ServerConfig` with:
#   - Class attributes:  host = "localhost"
#                        port = 8080
#                        timeout = 30
#   - No custom __init__ needed (use the default)
#
# Individual instances can override any of these values
# without affecting the class defaults or other instances.

class ServerConfig:
    pass  # TODO



# Exercise 4 — Avoiding the Mutable Trap
#
# Create TWO classes:
#
# `BrokenTeam`  — has a class-level `members = []`
#                 __init__ accepts `name` (the team's name)
#                 has `add_member(member)` appending to self.members
#                 (this implementation is intentionally broken — let it be)
#
# `FixedTeam`   — same interface but stores members as an
#                 instance attribute so each team has its own list


class BrokenTeam:
    pass  # TODO (keep the broken shared-list behaviour)


class FixedTeam:
    pass  # TODO (fix it — each instance gets its own list)


# Exercise 5 — Registry Pattern
#
# Create a class `Plugin` with:
#   - A class attribute `registry = {}` mapping name → instance
#   - An instance attribute `name` set in __init__
#   - __init__ must automatically register the new instance:
#       Plugin.registry[self.name] = self
#   - A class method `get(name)` that returns the plugin by name
#     or None if not found
#   - A class method `reset()` that clears the registry
#     (for test isolation)

class Plugin:
    pass  # TODO
