
pytest is a software test framework, which means pytest is a command-line tool that automatically finds tests you’ve written, runs the tests, and reports the results. You can use pytest to run tests written for unittest or nose.

Here are the different tests we can conduct in pytests. These are labels given to different types of tests conducted : 

**Unit test**: A test that checks a small bit of code, like a function or a class, in isolation of the rest of the system. I consider the tests in Chapter 1, Getting Started with pytest, to be unit tests run against the Tasks data structure.

**Integration test**: A test that checks a larger bit of the code, maybe several classes, or a subsystem. Mostly it’s a label used for some test larger than a unit test, but smaller than a system test.

**System test (end-to-end)**: A test that checks all of the system under test in an environment as close to the end-user environment as possible. Functional test: A test that checks a single bit of functionality of a system. A test that checks how well we add or delete or update a task item in Tasks is a functional test. 

**Subcutaneous test**: A test that doesn’t run against the final end-user interface, but against an interface just below the surface. Since most of the tests in this book test against the API layer—not the CLI—they qualify as subcutaneous tests.


*Note : We use pytest for reasons listed below:
- *In pytest, you can just name a file test_thenameofthefileyouaretesting or just the-name-of-the-file-you-are-testing_test and pytest will auto detect these tests and give us results. You donot need to tell the pytest library which one is a test and which isn't.*
- *In pytest, you will get a detailed reason on why your test failed rather than some random text where you have to debug what went wrong. This makes life a hell of a lot simpler. *
- *We can run a test function multiple times with different parameters to really get the coverage required of the testing service. You give the system a set or a list of parameters to test against and it will check for each parameter.*
- *Pytest has a lot of extensibility. That means, we can add certain add-ons and be able to test literally anything from django to graphana.*