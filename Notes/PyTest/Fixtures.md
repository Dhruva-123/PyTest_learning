
# **Pytest Fixtures – Deep Dive**

**What are fixtures?**  
Fixtures are reusable components that **prepare the environment, data, or dependencies** your tests need. They are **the backbone of clean, maintainable, and isolated testing** in pytest. Think of them as “test helpers” that **set up before a test runs and clean up after it finishes**.

Fixtures let you avoid repetitive boilerplate while giving your tests a **clear separation of setup and logic**.

---

## **1. Basic Fixture**

`import pytest  @pytest.fixture def sample_list():     """Returns a list for tests to use."""     return [1, 2, 3, 4, 5]  def test_sum(sample_list):     assert sum(sample_list) == 15`

**How it works:**

1. `@pytest.fixture` declares a fixture.
    
2. Test functions **request the fixture** by having a parameter with the same name (`sample_list`).
    
3. Pytest automatically calls the fixture function and injects its return value into the test.
    
4. No setup repetition in multiple tests.
    

---

## **2. Fixture Scope**

Fixtures can live longer than a single test using **scopes**:

|Scope|Description|Example Use Case|
|---|---|---|
|`function`|Default. Runs once per test function|A list or dict used only in one test|
|`class`|Runs once per test class|Shared object for all tests in a class|
|`module`|Runs once per file/module|DB connection reused across tests in the file|
|`package`|Runs once per package|Large setup shared across files in a package|
|`session`|Runs once per pytest session (entire test run)|Global environment setup or test server|

`@pytest.fixture(scope="module") def db_connection():     print("Connecting to DB")     yield "DB connection object"     print("Closing DB connection")`

- `yield` separates **setup** (before yield) and **teardown** (after yield).
    
- Setup runs **once per scope**, teardown runs after the last dependent test.
    

---

## **3. Parametrized Fixtures**

Fixtures can be parametrized to **run the same test with multiple setups**:

`@pytest.fixture(params=[1, 2, 3]) def number(request):     """Provides numbers 1, 2, 3 one by one to tests."""     return request.param  def test_number_square(number):     assert number ** 2 >= 0`

- `request.param` → provides the current parameter value.
    
- Test runs once **for each value** in `params`.
    

---

## **4. Fixture Dependencies**

Fixtures can **depend on other fixtures**, letting you compose setup logic neatly:

`@pytest.fixture def db_connection():     return "DB Connected"  @pytest.fixture def user(db_connection):     return {"name": "Bob", "status": db_connection}  def test_user_status(user):     assert user["status"] == "DB Connected"`

- `user` automatically gets the value from `db_connection`.
    
- Pytest resolves dependencies **topologically**—runs fixtures in the correct order.
    

---

## **5. Autouse Fixtures**

Autouse fixtures **run automatically** without being explicitly requested:

`@pytest.fixture(autouse=True) def setup_environment():     print("Setting up environment")     yield     print("Cleaning up environment")`

- Runs **before and after every test** in scope.
    
- Perfect for **global setup/teardown** like environment variables, logging, or mocks.
    

---

## **6. Fixtures in Multiple Modules (`conftest.py`)**

- Put fixtures in `conftest.py` for **automatic global availability** in the same directory tree.
    
- No imports required in test files.
    

`# conftest.py import pytest  @pytest.fixture def user_data():     return {"name": "Alice", "age": 25}  # test_module1.py def test_name(user_data):     assert user_data["name"] == "Alice"  # test_module2.py def test_age(user_data):     assert user_data["age"] == 25`

---

## **7. Setup and Teardown**

Fixtures handle **setup before tests** and **cleanup after tests** elegantly:

`@pytest.fixture def temporary_file(tmp_path):     file = tmp_path / "data.txt"     file.write_text("Hello World")  # setup     yield file     file.unlink()  # teardown`

- Setup → everything before `yield`
    
- Teardown → everything after `yield`
    

**This avoids manual cleanup inside tests**, which is error-prone.

---

## **8. Combining Fixtures with Parametrization**

You can **use fixtures inside parametrized tests** and vice versa:

`@pytest.fixture def sample_list():     return [1, 2, 3, 4, 5]  @pytest.mark.parametrize("multiplier, expected", [(1, 15), (2, 30)]) def test_sum_times(sample_list, multiplier, expected):     assert sum(sample_list) * multiplier == expected`

- Test runs **once per parameter tuple**.
    
- Fixture is injected automatically each time.
    

---

## **9. Benefits of Fixtures**

1. **Reusability:** Write setup logic once, reuse everywhere.
    
2. **Separation of concerns:** Tests focus only on assertions.
    
3. **Isolation:** Each test gets a fresh, controlled environment.
    
4. **Scalability:** Parametrized and autouse fixtures handle multiple tests and scenarios.
    
5. **Composition:** Fixtures can depend on other fixtures naturally.
    
6. **Setup/Teardown:** Built-in mechanism prevents resource leaks.
    

---

## **10. Common Pitfalls**

- Misspelling fixture names → `fixture not found`.
    
- Forgetting `@pytest.fixture` → pytest ignores the function.
    
- Overusing `autouse` → can make tests confusing if too much runs behind the scenes.
    
- Global state modification → break test isolation. Always return fresh objects or use `scope` wisely.