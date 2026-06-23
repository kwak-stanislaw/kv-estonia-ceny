# Class Attributes in Python

## What is a Class Attribute?

A **class attribute** is defined directly on the class body — outside any method.  
It is **shared by all instances** of that class.

```python
class Dog:
    species = "Canis familiaris"  # class attribute

    def __init__(self, name):
        self.name = name          # instance attribute
```

---

## Class vs Instance Attributes

| | Class Attribute | Instance Attribute |
|---|---|---|
| **Defined in** | Class body | `__init__` (via `self`) |
| **Shared?** | Yes — all instances | No — unique per object |
| **Access** | `ClassName.attr` or `self.attr` | `self.attr` only |
| **Mutate via** | `ClassName.attr = ...` | `self.attr = ...` |

---

## Lookup Order

Python resolves attributes in this order:

```
instance → class → parent classes (MRO)
```

If an instance sets its own attribute with the same name, it **shadows** the class attribute — only for that instance.

```python
fido = Dog("Fido")
fido.species = "mutant"   # creates instance attribute on fido

print(fido.species)   # "mutant"   ← instance attribute wins
print(Dog.species)    # "Canis familiaris"  ← class attribute unchanged
```

---

## Common Use Cases

### 1. Shared Constants
```python
class Circle:
    PI = 3.14159

    def area(self, r):
        return Circle.PI * r ** 2
```

### 2. Instance Counter
```python
class User:
    count = 0

    def __init__(self, name):
        self.name = name
        User.count += 1   #  use ClassName, not self
```
> Always increment via the **class name**, not `self`.  
> `self.count += 1` creates a *new instance attribute* instead of updating the shared one.

### 3. Default Values (overridable per instance)
```python
class Config:
    timeout = 30

cfg = Config()
cfg.timeout = 60    # overrides only for this object
print(Config.timeout)  # still 30
```

### 4. Shared Registry / Cache
```python
class Animal:
    registry = []

    def __init__(self, name):
        self.name = name
        Animal.registry.append(self)
```

---

## The Mutable Attribute Trap

Mutable class attributes (lists, dicts) are shared — **mutating** them affects all instances.

```python
class Team:
    members = []    # ← shared list, DANGER

t1 = Team()
t2 = Team()

t1.members.append("Alice")   # mutates the shared list!
print(t2.members)            # ["Alice"] — unexpected!
```

**Fix:** initialise mutable defaults in `__init__`:

```python
class Team:
    def __init__(self):
        self.members = []   #  each instance gets its own list
```

---


```python
class MyClass:
    value = 42
 
    def instance_method(self):      # receives instance
        return self.value
 
    @classmethod
    def class_method(cls):          # receives the class
        return cls.value
```
 
| | Receives | Can access class state? | Can access instance state? |
|---|---|---|---|
| Instance method | `self` | ✅ via `self.__class__` | ✅ |
| Class method | `cls` | ✅ | ❌ |

 

## Quick Rule of Thumb

- Same value for every instance → **class attribute**  
- Unique per object → **instance attribute**  
- Counter or shared state → **class attribute**, mutate via `ClassName.x`  
- Mutable default (list/dict) → **instance attribute** in `__init__`


