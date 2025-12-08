🧪 Testing the Book API — Documentation
Overview

This project includes a comprehensive suite of unit tests for the Book API built using Django REST Framework.
The purpose of the tests is to validate:

Correct behavior of all CRUD endpoints

Proper filtering, searching, and ordering

Authentication and permission enforcement

Integrity and correctness of API response data

All tests are located in:

api/test_views.py

⚙️ Testing Framework

The test suite uses Django’s built-in test framework, which is based on unittest.
Additional helpers from DRF are used:

APITestCase for mocking requests

Automatic setup & teardown of a temporary test database

No production data is affected.

🧪 Test Categories
1. CRUD Functionality

List Books – GET /api/books/

Retrieve Single Book – GET /api/books/<id>/

Create Book – POST /api/books/create/

Update Book – PUT /api/books/update/<id>/

Delete Book – DELETE /api/books/delete/<id>/

Tests verify:

HTTP status codes (200, 201, 204, 401)

Response structure & correctness

Database state before & after operations

2. Filtering

Filtering tests ensure query parameters work correctly, including:

?title=<value>

?author=<value> (mapped to author__name via BookFilter)

?min_year=<value>

?max_year=<value>

Tests validate:

Only expected books are returned

Filtering rules and lookup expressions work

Multiple filters can be combined

3. Searching

Tests ensure SearchFilter works correctly via ?search=:

Search by partial book title

Search by author name

Case-insensitive matching

4. Ordering

Tests confirm that results can be sorted:

?ordering=title

?ordering=publication_year

?ordering=-publication_year

Verifies ascending and descending behavior.

5. Permissions

Tests ensure endpoints requiring authentication behave correctly:

Anonymous users cannot create, update, or delete books

Authenticated users can perform modifications

Proper 401/403 responses are returned when needed

▶️ How to Run the Test Suite

From the project root, run:

python manage.py test api


Expected output:

Ran XX tests in X.XXXs

OK


If any test fails, Django prints detailed tracebacks.

✔️ What Passing Tests Guarantee

When all tests pass:

CRUD operations behave exactly as expected

Filter/search/order functions operate correctly

Validation and permissions work

API responses match expected schemas

Breaking changes will be caught immediately