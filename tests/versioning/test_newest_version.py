import mylib.helpers as helper
import pytest
import requests
import json
import time


# 1/4
# Test to ensure that the latest version of the live page is 1.4

def test_version_match(page):
    
    page.goto("https://randomuser.me/changelog")
    assert "Version 1.4" in page.content(), "Version 1.4 not found in changelog"


# 2/4
# Verify that newly added nationalities are correct

NATIONALITIES = [
    ("in", "India"),
    ("mx", "Mexico"),
    ("rs", "Serbia"),
    ("ua", "Ukraine"),
]

@pytest.mark.parametrize("nat, expected_country", NATIONALITIES)
def test_new_nationalities(request_context, nat, expected_country):
    
    url = f"https://randomuser.me/api/?nat={nat}"
    data = helper.fetch_json_data(request_context, url)
    country = data["results"][0]["location"]["country"]
    assert country == expected_country, f"Expected country '{expected_country}', got {country}"
    print("Country 1.4:", country)

    # Comparison with the previous version 1.3 where these nationalities were not available
    url = f"https://randomuser.me/api/1.3/?nat={nat}"
    data = helper.fetch_json_data(request_context, url)
    country = data["results"][0]["location"]["country"]
    assert country != expected_country, f"Expected country other than {expected_country}, got {country}"
    print("Country 1.3:", country)


# 3/4
# Verify added social security numbers for foreign countries

SSNNAMES = [
    ("br", "CPF"),
    ("ca", "SIN"),
    ("de", "SVNR"),
    ("LEGO", "SN") # fixed from "serial#"
]

@pytest.mark.parametrize("nat, expected_ssn_name", SSNNAMES)
def test_foreign_ssns(request_context, nat, expected_ssn_name):

    """Test to ensure that foreign social security numbers are correct in the latest version 1.4."""
    
    # Check if the foreign social security numbers added in v.1.4 are correct
    if nat == "LEGO":
        url = "https://randomuser.me/api/?lego"
    else:
        url = f"https://randomuser.me/api/?nat={nat}"
    data = helper.fetch_json_data(request_context, url)
    socialnumber = helper.find_key_in_dict(data, "id") # "name" : "CPF", "value" : ...
    assert socialnumber["name"] == expected_ssn_name, f"Expected 'name' to be {expected_ssn_name}, got {socialnumber['name']}"
    print("Social Number 1.4:", socialnumber)

    # Comparison with the previous version 1.3 where these social security numbers were not available
    if nat == "LEGO":
        url = "https://randomuser.me/api/1.3/?lego"
    else:
        url = f"https://randomuser.me/api/1.3/?nat={nat}"
    data = helper.fetch_json_data(request_context, url)
    socialnumber = helper.find_key_in_dict(data, "id")
    assert socialnumber != expected_ssn_name, "Social security number should not be correct in version 1.3"
    print("Social Number 1.3:", socialnumber)


# 4/4
# Test date calculations for dob and registered fields

# N.B. The first 4 tests are run with the seed "testing123" to verify that the date calculations are correct for known values
# and to verify the logic.
# These tests are skipped during normal runs.

# Version 1.4 introduced a fix for the date calculations, so we need to ensure that the calculations are correct
@pytest.mark.test123seed
def test_dob_calculation_known():
    url = "https://randomuser.me/api/1.4/?seed=testing123" # dob is "1993-01-14T06:19:58.502Z", age should be 32 as of 2025-06-02
    response = requests.get(url)
    data = response.json()
    print(f"[DEBUG] Fetching: {url}")
    print(json.dumps(data, indent=2))
    dob = helper.find_key_in_dict(data, "dob")
    print(f"DOB ver 1.4: {dob}", type(dob))
    years = helper.calculate_years(dob)
    print(f"Calculated years since birth: {years}")
    print(f"Generated age: {dob['age']}")
    assert years == dob["age"], f"Expected age to be 32, got {years}"

@pytest.mark.test123seed
def test_registered_calculation_known():
    url = "https://randomuser.me/api/1.4/?seed=testing123" # registered date is "2004-01-09T22:06:00.202Z", age should be 21 as of 2025-06-02
    response = requests.get(url)
    data = response.json()
    print(f"[DEBUG] Fetching: {url}")
    print(json.dumps(data, indent=2))
    reg = helper.find_key_in_dict(data, "registered")
    years = helper.calculate_years(reg)
    print(f"REG ver 1.4: {reg}", type(reg))
    print(f"Calculated years since registration: {years}")
    print(f"Registered age: {reg['age']}")
    assert years == reg["age"], f"Expected age to be 21, got {years}"

# Version 1.3 had a bug in the date calculations, so we need to ensure that the calculations are incorrect
@pytest.mark.test123seed
def test_dob_calculation_known_1_3():
    url = "https://randomuser.me/api/1.3/?seed=testing123" # dob is "1990-10-09T10:25:31.134Z", age should be 34 as of 2025-06-02
    response = requests.get(url)
    data = response.json()
    print(f"[DEBUG] Fetching: {url}")
    print(json.dumps(data, indent=2))
    dob = helper.find_key_in_dict(data, "dob")
    print(dob)
    years = helper.calculate_years(dob)
    print(f"DOB ver 1.3: {dob}", type(dob))
    print(f"Calculated years since birth: {years}")
    print(f"Generated age: {dob['age']}")
    # calculation was incorrect in version 1.3, so we expect the age to be 35
    assert years != dob["age"], f"Expected age not to be 34, got {years}"

@pytest.mark.test123seed
def test_registered_calculation_known_1_3():
    url = "https://randomuser.me/api/1.3/?seed=testing123" # registered date is "2003-10-14T23:46:05.735Z", age should be 21 as of 2025-06-02
    response = requests.get(url)
    data = response.json()
    print(f"[DEBUG] Fetching: {url}")
    print(json.dumps(data, indent=2))
    reg = helper.find_key_in_dict(data, "registered")
    years = helper.calculate_years(reg)
    print(f"REG ver 1.3: {reg}", type(reg))
    print(f"Calculated years since registration: {years}")
    print(f"Registered age: {reg['age']}")
    # calculation was incorrect in version 1.3, so we expect the age to be 22
    assert years != reg["age"], f"Expected age not to be 5, got {reg['age']}"


# Actual tests for random data, these will be run multiple times with different random data
# TODO: Consider generating a number of random users at once to minimize the known seed error and adjust the key/value search logic accordingly

@pytest.mark.parametrize("i", range(10)) # run the test "i" times with different random data
def test_dob_calculation_random(request_context, i):

    """Test to ensure that the age calculation from birth is correct for random data."""
    
    url = "https://randomuser.me/api"
    data = helper.fetch_json_data(request_context, url)

    seed = helper.find_key_in_dict(data, "seed")
    if seed == "d3adb33f":
        pytest.skip("Skipping test for seed 'd3adb33f' as it is known to cause issues.")

    print(f"[DEBUG] Fetching: {url}")
    print(json.dumps(data, indent=2))
    dob = helper.find_key_in_dict(data, "dob")
    years = helper.calculate_years(dob)
    print(f"Random DOB ver 1.4: {dob}", type(dob))
    print(f"Calculated years since registration: {years}")
    print(f"Generated age: {dob['age']}")
    assert years == dob["age"], f"Expected age to be {dob['age']}, got {years}"

    time.sleep(0.4)  # Sleep to avoid hitting the API too fast, can be adjusted as needed

@pytest.mark.parametrize("j", range(10)) # run the test "j" times with different random data
def test_registered_calculation_random(request_context, j):

    """Test to ensure that the years calculation since registration is correct for random data."""
    
    url = "https://randomuser.me/api"
    data = helper.fetch_json_data(request_context, url)

    seed = helper.find_key_in_dict(data, "seed")
    if seed == "d3adb33f":
        pytest.skip("Skipping test for seed 'd3adb33f' as it is known to cause issues.")

    print(f"[DEBUG] Fetching: {url}")
    print(json.dumps(data, indent=2))
    reg = helper.find_key_in_dict(data, "registered")
    years = helper.calculate_years(reg)
    print(f"Random DOB ver 1.4: {reg}", type(reg))
    print(f"Calculated years since registration: {years}")
    print(f"Generated age: {reg['age']}")
    assert years == reg["age"], f"Expected age to be {reg['age']}, got {years}"

    time.sleep(0.4)