"""
===========================================================
  OOP Animal Hierarchy – Exercise
===========================================================

-------------------
HOW TO WORK THROUGH THIS FILE
------------------------------
  • Search for every TODO comment — that is where you (usually) write code.
  • Read the docstrings carefully, they describes exactly what the method must do and what it must return.
  • Run test_animals.py for checks
"""


# ===========================================================
# PART 0  –  Custom Exception (SOLVED)
# ===========================================================

# TODO: Define a custom exception class called CannotFlyError.
#       It should inherit from the built-in Exception class.
#       No body is needed beyond `pass`.
#
# Example usage once implemented:
#   raise CannotFlyError("Penguins can't fly!")

class CannotFlyError(Exception):
    pass


# ===========================================================
# PART 1  –  Base Class
# ===========================================================

class Animal:
    """
    Base class for all animals.

    Attributes
    ----------
    name : str
        The animal's name.
    age  : int
        The animal's age in years.
    """

    def __init__(self, name: str, age: int):
        """
        Store name and age as instance attributes.

        Parameters
        ----------
        name : str   e.g. "Rex"
        age  : int   e.g. 3

        """
        # TODO: assign both parameters to instance attributes

        self.name = name
        self.age = age

    # ----------------------------------------------------------

    def speak(self):
        """
        Every real animal can speak, but Animal itself is too
        generic to know how. This method acts as a placeholder
        that child classes MUST override.

        [RAISE] NotImplementedError with the message:
                "Subclasses must implement speak()"

        """
        # TODO: raise NotImplementedError with the required message

        raise NotImplementedError("Subclasses must implement speak()")


    # ----------------------------------------------------------

    def describe(self) -> str:
        """
        Return a human-readable description of this animal.

        [RETURN] "I am {name}, {age} years old."

        Example:
          animal = Animal("Buddy", 4)
          animal.describe()  →  "I am Buddy, 4 years old."

        !! Do NOT override this method in any child class !!
           Inheritance means children get it for free.
        """
        # TODO: return the formatted string (use an f-string)

        return f"I am {self.name}, {self.age} years old."

    # ----------------------------------------------------------

    def __repr__(self) -> str:
        """
        Return string representation of this object.

        [RETURN] "Animal(name={name}, age={age})"

        Example:
          repr(Animal("Buddy", 4))  →  "Animal(name=Buddy, age=4)"
        """
        # TODO: return the formatted string

        return f"Animal(name={self.name}, age={self.age})"



# ===========================================================
# PART 2  –  Dog
# ===========================================================

class Dog(Animal):
    """
    A Dog is an Animal that barks and fetches things.

    Extra attribute
    ---------------
    breed : str   e.g. "Labrador"
    """

    def __init__(self, name: str, age: int, breed: str):
        """
        Initialise Dog with name, age (via parent) and breed.
        """
        # TODO: call super().__init__() then store breed

        super().__init__(name, age)
        self.breed = breed

    # ----------------------------------------------------------

    def speak(self) -> str:
        """
        Dogs say Woof!

        Example:
          Dog("Rex", 3, "Lab").speak()  →  "Rex says: Woof!"
        """
        # TODO: return the formatted string

        return f"{self.name} says: Woof!"

    # ----------------------------------------------------------

    def fetch(self, item: str) -> str:
        """
        Dogs love to fetch things.

        Parameters
        ----------
        item : str   e.g. "ball"



        Example:
          Dog("Rex", 3, "Lab").fetch("stick")  →  "Rex fetches the stick!"
        """
        # TODO: return the formatted string

        self.item = item
        return f"{self.name} fetches the {self.item}!"

    # ----------------------------------------------------------

    def __repr__(self) -> str:
        """
        Dog's __repr__ shows breed instead of age.

        Example:
          repr(Dog("Rex", 3, "Lab"))  →  "Dog(name=Rex, breed=Lab)"
        """
        # TODO: return the formatted string

        return f"Dog(name={self.name}, breed={self.breed})"


# ===========================================================
# PART 3  –  Cat
# ===========================================================

class Cat():
    """
    A Cat is an Animal that meows and purrs.
    TODO Add inheritance from Animal
    Extra attribute:
    indoor : bool   whether the cat lives indoors (default True)
    """

    def __init__(self, name: str, age: int, indoor: bool = True):
        """
        Initialise Cat with name, age (via parent) and indoor.
        """
        # TODO: call super().__init__() then store indoor

        super().__init__(name, age)
        self.indoor = indoor

    # ----------------------------------------------------------

    def speak(self) -> str:
        """
        Cats say Meow!

        Example:
          Cat("Kicia", 3).speak()  →  "Kicia says: Meow!"
        """
        # TODO: return the formatted string

        return f"{self.name} says: Meow!"
    # ----------------------------------------------------------

    def purr(self) -> str:
        """
        A contented cat purrs.

        Example:
          Cat("Kicia", 3).purr()  →  "Kicia purrs contentedly."
        """
        # TODO: return the formatted string

        return f"{self.name} purrs contentedly."


# ===========================================================
# PART 4  –  Bird
# ===========================================================

class Bird():
    """
    A Bird is an Animal that tweets — and may or may not fly.
    TODO Add inheritance
    Extra attribute:
    can_fly : bool   True for most birds, False for e.g. penguins
    """

    def __init__(self, name: str, age: int, can_fly: bool):
        """
        Initialise Bird with name, age (via parent) and add can_fly.
        """
        # TODO: call parent class init then store can_fly

        pass

    # ----------------------------------------------------------

    def speak(self) -> str:
        """
        Birds say Tweet!

        Example:
            Bird("Dodo", 3, False).speak() -> "Dodo says: Tweet!"
        """
        # TODO: return the formatted string

        pass

    # ----------------------------------------------------------

    def fly(self) -> str:
        """
        Attempt to fly.

        if self.can_fly is True:
             [RETURN] "{name} soars through the sky!"
         else:
             [RAISE]  CannotFlyError("Penguins can't fly!")
        """
        # TODO: branch on self.can_fly

        pass


