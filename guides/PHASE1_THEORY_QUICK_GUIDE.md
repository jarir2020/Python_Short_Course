# ⚡ Phase 1: Python Core Theory Quick Guide

A concise cheat sheet for web developers learning Python. Each concept includes a 1-2 sentence summary and a 1-2 line code snippet.

---

## 0. Absolute Basics: Arithmetic, Logic, Control Flow & Loops
* **Arithmetic**: `+`, `-`, `*`, `/` (float divide), `//` (integer divide), `%` (remainder), `**` (power).
* **Control Flow**: Conditional branching using `if`, `elif`, `else`, and ternary operator `a if cond else b`.
* **Loops & Slicing**: Repeat code using `for` and `while` loops; extract sub-lists with slicing `lst[start:stop]`.

```python
val = 10 // 3                     # Integer division -> 3
status = "OK" if val > 0 else "Err" # Ternary operator
for i in range(3): print(i)       # Prints 0, 1, 2
sub_list = [10, 20, 30, 40][1:3]  # Returns [20, 30]
```

---

## 1. Variables & References
Variables in Python are **labels (names) bound to memory objects**, not boxes holding values. Multiple names can point to the same object.

```python
a = [1, 2]
b = a          # b points to the SAME list in memory as a
```

---

## 2. Identity (`is`) vs Equality (`==`)
* `==` checks if two objects have **equal values**.
* `is` checks if two variables point to the **exact same memory location**.

```python
x = [1, 2]; y = [1, 2]
print(x == y)  # True (same content)
print(x is y)  # False (different memory locations)
```

---

## 3. Shallow Copy vs Deep Copy
* **Shallow Copy**: Copies the outer container; inner nested objects remain shared references.
* **Deep Copy**: Recursively copies outer and inner objects independently.

```python
import copy
shallow = original.copy()        # Inner items shared
deep = copy.deepcopy(original)   # Completely independent copy
```

---

## 4. Truthiness & `None`
Empty structures (`[]`, `{}`, `""`, `0`, `False`, `None`) evaluate to `False` in boolean contexts. Always check `None` using `is None`.

```python
if val is None:                  # Best practice for None check
    print("Value is missing")
```

---

## 5. Scope & the LEGB Rule
Python searches for variable names in order: **L**ocal $\rightarrow$ **E**nclosing $\rightarrow$ **G**lobal $\rightarrow$ **B**uilt-in.

```python
x = "global"
def outer():
    x = "enclosing"
    def inner():
        x = "local"              # Python looks here first
```

---

## 6. Core Data Structures
* **List**: Ordered, mutable `[1, 2, 3]`
* **Tuple**: Ordered, immutable `(10.0, 20.0)`
* **Dict**: Key-value mapping `{"name": "Alice"}`
* **Set**: Unordered, unique elements `{1, 2, 3}`

```python
user = {"name": "Alice"}         # Dict lookup: user["name"]
unique_ids = {101, 102, 101}     # Result: {101, 102} (duplicates auto-removed)
```

---

## 7. Functions: `*args` and `**kwargs`
* `*args`: Collects extra positional arguments into a **tuple**.
* `**kwargs`: Collects extra keyword arguments into a **dictionary**.

```python
def add_item(*args, **kwargs):
    print(args)                  # Tuple of extra positional arguments
    print(kwargs)                # Dict of extra keyword arguments
```

---

## 8. OOP Basics (`class`, `self`, `__init__`)
Classes blueprint objects. `self` refers to the active instance. `__init__` is the constructor.

```python
class User:
    def __init__(self, name: str):
        self.name = name         # Instance variable
```

---

## 9. Exception Handling (`try / except / else / finally`)
Prevents application crashes. `else` runs if no error occurs; `finally` ALWAYS runs for cleanup.

```python
try:
    res = 10 / 0
except ZeroDivisionError:
    res = None                   # Gracefully handle error
finally:
    db.close()                   # Always clean up resources
```

---

## 10. Custom Exceptions
Inherit from Python's base `Exception` class to create custom domain/application errors.

```python
class UserNotFoundError(Exception): pass

raise UserNotFoundError("User ID 42 not found")
```

---

## 11. Context Managers (`with` statement)
Ensures resource setup (`__enter__`) and teardown (`__exit__`) happen automatically, even during crashes.

```python
with open("file.txt", "w") as f:
    f.write("Hello Backend")      # Auto-closed when exiting block
```

---

## 12. First-Class Functions & Decorators
Functions can be passed as arguments. A **decorator** wraps a function to modify its behavior without changing its code.

```python
def my_decorator(func):
    def wrapper():
        print("Before function execution")
        return func()
    return wrapper
```

---

## 13. Preserving Metadata with `@wraps`
Decorating functions hides their original `__name__` and `__doc__`. `@wraps` preserves them.

```python
from functools import wraps
def my_dec(func):
    @wraps(func)                  # Preserves func.__name__
    def wrapper(*args, **kwargs): return func(*args, **kwargs)
    return wrapper
```

---

## 14. Type Hints & Dataclasses
Type hints enforce readability and enable API frameworks (like FastAPI) to validate data. `@dataclass` generates `__init__` automatically.

```python
from dataclasses import dataclass

@dataclass
class Item:
    id: int
    name: str
    price: float = 0.0
```

---

## 15. Modules, Packages & Virtual Envs
* **Module**: A single `.py` file.
* **Package**: A directory with an `__init__.py` file.
* **`if __name__ == "__main__":`**: Runs code ONLY when the script is executed directly.
* **`venv`**: Isolated folder for project-specific pip dependencies.

```bash
python3 -m venv .venv            # Create virtual environment
source .venv/bin/activate        # Activate virtual environment (Linux/macOS)
pip install -r requirements.txt  # Install project dependencies
```

---

## 16. Dynamic Typing, Comprehensions & Generators
* **Dynamic typing**: A name can be rebound to objects of different types; a
  type annotation documents intent but does not enforce it at runtime by
  itself.
* **Comprehensions**: Compact syntax for building lists, dictionaries, and
  sets from an iterable.
* **Iterator**: An object that returns one item at a time through `next()`.
* **Generator**: A function containing `yield`; it pauses and resumes lazily,
  which is useful for large data streams.

```python
even_squares = [n * n for n in numbers if n % 2 == 0]

def count_up_to(limit):
    for number in range(1, limit + 1):
        yield number
```
