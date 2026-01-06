
## 1. What does `import` actually mean in Python?

When Python sees an import statement like:

`from Source.Binary_search import binary_search`

Python does **not**:

- search your whole project
    
- guess folder relationships
    
- recursively scan directories
    

Instead, Python follows a **strict, deterministic algorithm**.

---

## 2. `sys.path` — the real import mechanism

Python maintains a list called:

`sys.path`

This is **the only place Python looks** when resolving imports.

`sys.path` is a list of directories, searched **in order**.

### Where does `sys.path` come from?

At runtime, Python builds it from:

1. **The directory of the executed command**
    
    - For `pytest`, this is the directory where you ran `pytest`
        
2. The `PYTHONPATH` environment variable (if set)
    
3. Python standard library directories
    
4. Installed packages (`site-packages`)
    

👉 **If a directory is not in `sys.path`, Python pretends it does not exist.**

There is no exception to this.

---

## 3. Modules vs Packages (critical distinction)

### Module

A **module** is a single file:

`binary_search.py`

Imported as:

`import binary_search`

---

### Package

A **package** is a directory that Python recognizes as a module namespace.

Traditionally, a directory becomes a package **only if it contains**:

`__init__.py`

Example:

`Source/ ├── __init__.py └── Binary_search.py`

Now Python treats `Source` as a package, and this becomes valid:

`from Source.Binary_search import binary_search`

---

## 4. What does `__init__.py` actually do?

`__init__.py` does **one thing**:

> It tells Python:  
> “This directory is a package and can be imported.”

That’s it.

Important points:

- It can be empty
    
- It can contain code
    
- Its mere presence changes import behavior
    

Without `__init__.py`, the directory is just a folder — **not importable**.

---

## 5. Why `__init__.py` still matters today

Python 3.3+ introduced _namespace packages_ (folders without `__init__.py`).

However:

- Tooling (pytest, linters, IDEs, CI) still expect `__init__.py`
    
- Namespace packages are for advanced, multi-distribution setups
    
- Accidental namespace packages cause subtle bugs
    

**Rule you should follow:**

> If you control the code, add `__init__.py`.

---

## 6. Why running pytest from the project root matters

Suppose your project looks like this:

`code/ ├── Source/ │   ├── __init__.py │   └── Binary_search.py └── test/     └── test_Binary_search.py`

If you run:

`cd code pytest`

Then:

- `code/` becomes part of `sys.path`
    
- Python can see **both** `Source/` and `test/`
    

If instead you run pytest from inside `test/`:

`cd test pytest`

Then:

- only `test/` is visible
    
- `Source/` does not exist from Python’s perspective
    
- imports fail
    

This is about **`sys.path`**, not pytest preference.

---

## 7. pytest’s role (what it does and does NOT do)

pytest:

- discovers test files (`test_*.py`, `*_test.py`)
    
- imports test modules like normal Python modules
    
- executes test functions
    
- reports results
    

pytest **does NOT**:

- fix broken imports
    
- guess your project structure
    
- magically expose folders
    

Older pytest versions _hid_ import problems.  
pytest 8 **does not**.

This is intentional and correct.

---

## 8. Why pytest 8 broke “working” imports

pytest 8 uses:

`--import-mode=importlib`

This means:

- pytest no longer auto-adds the project root to `sys.path`
    
- imports behave closer to real Python execution
    
- broken project layouts are exposed early
    

This is why your setup **looked correct** but still failed.

---

## 9. Why `pyproject.toml` is added

### What is TOML?

TOML = _Tom’s Obvious, Minimal Language_

It’s a configuration format:

- human-readable
    
- strict
    
- predictable
    

Python standardized on it for tooling configuration.

---

### What is `pyproject.toml`?

It is the **single source of truth** for project configuration:

- pytest
    
- packaging
    
- build systems
    
- linters
    
- formatters
    

Modern Python projects are expected to have one.

---

## 10. The pytest configuration you added — explained word by word

### File:

`[tool.pytest.ini_options] pythonpath = ["."]`

---

### `[tool.pytest.ini_options]`

Breakdown:

- `tool` → configuration for developer tools
    
- `pytest` → specifically pytest
    
- `ini_options` → pytest accepts INI-style options even inside TOML
    

Meaning:

> “Everything under this section configures pytest.”

---

### `pythonpath = ["." ]`

Breakdown:

- `pythonpath` → directories pytest should add to `sys.path`
    
- `"."` → the current directory (project root)
    
- `["."]` → a list (multiple paths are allowed)
    

Effectively does:

`sys.path.insert(0, PROJECT_ROOT)`

Explicit. Reproducible. CI-safe.

---

## 11. Full import + pytest flow (end-to-end)

1. You design your project structure
    
2. You mark source directories as packages using `__init__.py`
    
3. You run pytest from the project root
    
4. pytest reads `pyproject.toml`
    
5. pytest adds configured paths to `sys.path`
    
6. Python resolves imports normally
    
7. pytest discovers test files
    
8. pytest imports test modules
    
9. tests import source code
    
10. tests execute and report results
    

No magic. No hacks.

---

## 12. Modern best-practice layout (why `src/` exists)

Preferred structure:

`project/ ├── pyproject.toml ├── src/ │   └── myapp/ │       ├── __init__.py │       └── binary_search.py └── tests/     └── test_binary_search.py`

Why this is used:

- prevents accidental imports
    
- forces tests to behave like external consumers
    
- matches production and CI environments
    
- exposes bugs early
    

---

## 13. Rules you can rely on (memorize these)

1. Python only imports what’s in `sys.path`
    
2. A folder is importable only if it is a package
    
3. `__init__.py` makes a folder a package
    
4. pytest does not fix broken imports
    
5. Always run pytest from project root
    
6. Never modify `sys.path` inside test files
    
7. If imports fail in pytest, they would fail in production too
    

---

## 14. Corrected high-level summary

> Python resolves imports by searching `sys.path`.  
> A directory becomes importable when it is a package, usually marked by `__init__.py`.  
> pytest runs tests by importing them as normal Python modules and does not guess import paths.  
> Modern pytest requires explicit configuration via `pyproject.toml` to control the Python path.  
> When imports are correct, pytest discovery and execution are straightforward and reliable.

---

## 15. Status check

If you understand:

- why `sys.path` matters
    
- why `__init__.py` matters
    
- why pytest needed `pyproject.toml`
    

Then you now understand **more than most developers using pytest**


## Note: Why I Don’t Need to Import Every Function Explicitly

In Python, when I import a function from a module, **Python first loads and executes the entire module file**. This means all functions, variables, and helpers defined in that file are placed into the module’s namespace.

A function does **not** execute in the namespace of the file that imports it.  
It executes in the namespace of the **module where it was defined**.

Therefore, if a function depends on other helper functions that are defined in the **same file**, I do **not** need to import those helpers separately. Python resolves those names internally through the module’s global scope.

Example:

`# merge_sort.py
```
def merge(left, right):
     ...
     def merge_sort(arr):
          return merge(left, right)`

`# test file from Source.merge_sort import merge_sort`

```
This works because:

- importing `merge_sort` loads `merge_sort.py`
    
- `merge` exists in the same module namespace
    
- `merge_sort` resolves `merge` internally
    

However, Python does **not** automatically resolve functions across different files.  
If a function depends on helpers located in **another module**, those helpers must be explicitly imported in the file where the function is defined.

Key rule:

> Import the **entry point**.  
> Internal helpers in the same module are resolved automatically.  
> Helpers in other modules must be imported explicitly.

This design allows clean APIs, internal implementation details, and safe refactoring without changing import statements in test or caller code.