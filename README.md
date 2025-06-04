# Random User Generator

A Python project that is aimed at testing the [Random User API](https://randomuser.me/) and specifically: verifying whether or not the newest version (1.4 as of June 2025) has been deployed correctly.

## Details

Test suite has been divided into three sections:
- Smoke
- Regression
- Versioning

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/robo-senpai/zal-random-user-generator.git
   cd zal-random-user-generator

2. (Optional) Create and activate virtual environment.:

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate

3. Install dependencies:

   ```bash
   pip install -r requirements.txt

## Running the tests (Windows)

Some tests are marked with a custom marker (test123seed) - these have been created in order to test the calculation logic on existing seeded users, ensuring the data is constant and does not depend on the number of fetches as opposed to unseeded results.

When run as part of the entire test suite, these tests affect the results of the randomized (unseeded) fetches, specifically causing the JSON data to be cut or not loading properly and the seed changing to a different, albeit constant string.

In order to ensure the tests' independency it is highly recommended tests with these markers are either skipped (when running the remaining tests) or run independently if needed (without the remaining tests).

The default 'pytest' command will run all tests except those marked as "test123seed" (see pytest.ini).

To run all tests, use command:
   pytest -c nul

To only run tests marked with the test123seed marker, use command:
   pytest -m test123seed