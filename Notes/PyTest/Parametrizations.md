
# **Pytest Parametrization – Detailed Notes**

**Purpose:**  
Pytest parametrization allows a single test function to run **multiple times with different input values**. This reduces code repetition, makes tests cleaner, and ensures comprehensive coverage including edge cases.

---

## **1. Basic Syntax**

`import pytest  @pytest.mark.parametrize("param1, param2, ..., paramN", [     (value1a, value2a, ..., valueNa),     (value1b, value2b, ..., valueNb),     ... ]) def test_function(param1, param2, ..., paramN):     assert <function_under_test>(param1, param2, ..., paramN) == expected_result`

**Explanation:**

1. `@pytest.mark.parametrize` → decorator that tells pytest to parametrize this test.
    
2. First argument → a **string of parameter names** separated by commas.
    
3. Second argument → a **list of tuples**, each tuple contains a set of values corresponding to the parameters.
    
4. Pytest will run `test_function` **once for each tuple** in the list.
    
5. You can assert the function’s output against an expected value or perform any other test logic.
    

---

## **2. Example: Binary Search Test**

`import pytest from search_algorithms import binary_search  @pytest.mark.parametrize(     "input_arr, target, expected",     [         ([10], 10, 0),                   # Single element array         ([1, 4, 5, 6, 8, 9], 9, 5),      # Last element         ([1, 2, 3], 2, 1),               # Middle element         ([243, 332, 554, 999], 999, 3)   # Large numbers     ] ) def test_binary_search(input_arr, target, expected):     assert binary_search(input_arr, target) == expected`

**What happens:**

- Test runs **four times**, each time using the values from one tuple.
    
- Pytest automatically passes `input_arr`, `target`, `expected` to the test function.
    
- No need to write four separate test functions.
    

---

## **3. Multiple Parameters**

You can parametrize more than one argument simultaneously. Pytest handles mapping tuples to parameters automatically.

`@pytest.mark.parametrize("a, b, expected_sum", [     (1, 2, 3),     (10, 20, 30),     (-1, 1, 0), ]) def test_addition(a, b, expected_sum):     assert a + b == expected_sum`

---

## **4. Using `ids` for Readable Test Names**

You can give custom IDs to each test case. This is useful when pytest output is large and you want to identify test cases easily.

`@pytest.mark.parametrize(     "a, b, expected_sum",     [         (1, 2, 3),         (10, 20, 30),         (-1, 1, 0),     ],     ids=["small numbers", "tens", "zero sum"] ) def test_addition(a, b, expected_sum):     assert a + b == expected_sum`

**Effect:**

- Test results in pytest will display the given IDs instead of generic indexes like `[0]`, `[1]`, `[2]`.
    

---

## **5. Parametrizing with `pytest.param`**

`pytest.param` allows you to add **metadata** to a test case, like skipping or expecting failure.

`@pytest.mark.parametrize(     "a, b, expected_sum",     [         pytest.param(1, 2, 3, id="small numbers"),         pytest.param(10, 20, 30, id="tens"),         pytest.param(-1, 1, 0, marks=pytest.mark.xfail, id="xfail case"),     ] ) def test_addition(a, b, expected_sum):     assert a + b == expected_sum`

- `marks=pytest.mark.xfail` → pytest will expect this test to fail.
    
- Useful for testing **known issues or future fixes**.
    

---

## **6. Common Mistakes**

1. **Typo in decorator**
    
    - ❌ `@pytest.mark.parametrization(...)` → Wrong
        
    - ✅ `@pytest.mark.parametrize(...)` → Correct
        
2. **Mismatch between parameter names and tuple values**
    
    - Number of names in the string must equal the number of values in each tuple.
        
3. **Using fixtures instead of parameters**
    
    - Pytest will throw `fixture not found` if the decorator is wrong or missing.
        

---

## **7. Benefits of Parametrization**

- Reduces repetitive code.
    
- Makes tests **more readable** and **maintainable**.
    
- Automatically covers **edge cases**.
    
- Integrates well with pytest markers (`xfail`, `skip`, custom marks).
    

---

This is everything you need to fully understand and use **pytest parametrization** in real projects.