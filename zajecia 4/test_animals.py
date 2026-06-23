import pytest
from animals_skeleton import Animal, Dog, Cat, Bird, CannotFlyError


# Animal (base class)
class TestAnimal:
    def setup_method(self):
        self.animal = Animal("Generic", 5)

    def test_init_stores_name_and_age(self):
        assert self.animal.name == "Generic"
        assert self.animal.age == 5

    def test_speak_raises_not_implemented(self):
        with pytest.raises(NotImplementedError, match="Subclasses must implement speak()"):
            self.animal.speak()

    def test_describe_returns_correct_string(self):
        assert self.animal.describe() == "I am Generic, 5 years old."

    def test_repr_returns_correct_string(self):
        assert repr(self.animal) == "Animal(name=Generic, age=5)"


# Dog
class TestDog:
    def setup_method(self):
        self.dog = Dog("Rex", 3, "Labrador")

    def test_init_stores_all_attributes(self):
        assert self.dog.name == "Rex"
        assert self.dog.age == 3
        assert self.dog.breed == "Labrador"

    def test_speak_returns_woof(self):
        assert self.dog.speak() == "Rex says: Woof!"

    def test_fetch_returns_correct_string(self):
        assert self.dog.fetch("ball") == "Rex fetches the ball!"

    def test_fetch_works_with_any_item(self):
        assert self.dog.fetch("stick") == "Rex fetches the stick!"

    def test_repr_returns_correct_string(self):
        assert repr(self.dog) == "Dog(name=Rex, breed=Labrador)"

    def test_describe_inherited_unchanged(self):
        assert self.dog.describe() == "I am Rex, 3 years old."


# Cat
class TestCat:
    def setup_method(self):
        self.cat = Cat("Whiskers", 4)
        self.outdoor_cat = Cat("Tom", 2, indoor=False)

    def test_init_default_indoor_is_true(self):
        assert self.cat.indoor is True

    def test_init_outdoor_cat(self):
        assert self.outdoor_cat.indoor is False

    def test_speak_returns_meow(self):
        assert self.cat.speak() == "Whiskers says: Meow!"

    def test_purr_returns_correct_string(self):
        assert self.cat.purr() == "Whiskers purrs contentedly."

    def test_describe_inherited_unchanged(self):
        assert self.cat.describe() == "I am Whiskers, 4 years old."

    def test_repr_inherited_from_animal(self):
        # Cat does not override __repr__, falls back to Animal's
        assert repr(self.cat) == "Animal(name=Whiskers, age=4)"


# Bird
class TestBird:
    def setup_method(self):
        self.sparrow = Bird("Sparrow", 1, can_fly=True)
        self.penguin = Bird("Penguin", 6, can_fly=False)

    def test_init_stores_all_attributes(self):
        assert self.sparrow.name == "Sparrow"
        assert self.sparrow.age == 1
        assert self.sparrow.can_fly is True

    def test_speak_returns_tweet(self):
        assert self.sparrow.speak() == "Sparrow says: Tweet!"

    def test_fly_returns_correct_string_when_can_fly(self):
        assert self.sparrow.fly() == "Sparrow soars through the sky!"

    def test_fly_raises_cannot_fly_error_when_cannot_fly(self):
        with pytest.raises(CannotFlyError, match="Penguins can't fly!"):
            self.penguin.fly()

    def test_cannot_fly_error_is_exception_subclass(self):
        assert issubclass(CannotFlyError, Exception)

    def test_describe_inherited_unchanged(self):
        assert self.sparrow.describe() == "I am Sparrow, 1 years old."


# Polymorphism
class TestPolymorphism:
    def test_all_subclasses_implement_speak(self):
        animals = [
            Dog("Buddy", 2, "Poodle"),
            Cat("Luna", 3),
            Bird("Tweety", 1, can_fly=True),
        ]
        # None of these should raise NotImplementedError
        for animal in animals:
            result = animal.speak()
            assert isinstance(result, str)

    def test_describe_works_uniformly_across_subclasses(self):
        dog = Dog("Buddy", 2, "Poodle")
        cat = Cat("Luna", 3)
        bird = Bird("Tweety", 1, can_fly=True)
        assert dog.describe() == "I am Buddy, 2 years old."
        assert cat.describe() == "I am Luna, 3 years old."
        assert bird.describe() == "I am Tweety, 1 years old."