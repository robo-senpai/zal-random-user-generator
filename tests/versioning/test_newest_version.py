import mylib.helpers as helper
import pytest

# N.B. Run pytest -s to see print statements

def test_version_match(page):
    # check if the latest version of the live page is 1.4
    page.goto("https://randomuser.me/changelog")
    assert "Version 1.4" in page.content(), "Version 1.4 not found in changelog"

NATIONALITIES = [
    ("in", "India"),
    ("mx", "Mexico"),
    ("rs", "Serbia"),
    ("ua", "Ukraine"),
]

@pytest.mark.parametrize("nat, expected_country", NATIONALITIES)
def test_new_nationalities(request_context, nat, expected_country):
    
    # Check if the India data is available in the latest version 1.4
    url = f"https://randomuser.me/api/?nat={nat}"
    data = helper.fetch_json_data(request_context, url)
    country = data["results"][0]["location"]["country"]
    assert country == expected_country, f"Expected country '{expected_country}', got {country}"
    print("Country 1.4:", country)

    # Comparison with the previous version 1.3
    url = f"https://randomuser.me/api/1.3/?nat={nat}"
    data = helper.fetch_json_data(request_context, url)
    country = data["results"][0]["location"]["country"]
    assert country != expected_country, f"Expected country other than {expected_country}, got {country}"
    print("Country 1.3:", country)


SSNNAMES = [
    ("br", "CPF"),
    ("ca", "SIN"),
    ("de", "SVNR"),
    ("LEGO", "SN") # fixed from "serial#"
]

@pytest.mark.parametrize("nat, expected_ssn_name", SSNNAMES)
def test_foreign_ssns(request_context, nat, expected_ssn_name):
    
    # Check if the foreign social security numbers added in v.1.4 are correct
    if nat == "LEGO":
        url = "https://randomuser.me/api/?lego"
    else:
        url = f"https://randomuser.me/api/?nat={nat}"
    data = helper.fetch_json_data(request_context, url)
    socialnumber = helper.find_key_in_dict(data, "id") # "name" : "CPF", "value" : ...
    assert socialnumber["name"] == expected_ssn_name, f"Expected 'name' to be {expected_ssn_name}, got {socialnumber['name']}"
    print("Social Number 1.4:", socialnumber)

    # Comparison with the previous version 1.3
    if nat == "LEGO":
        url = "https://randomuser.me/api/1.3/?lego"
    else:
        url = f"https://randomuser.me/api/1.3/?nat={nat}"
    data = helper.fetch_json_data(request_context, url)
    socialnumber = helper.find_key_in_dict(data, "id")
    assert socialnumber != expected_ssn_name, "Social security number should not be correct in version 1.3"
    print("Social Number 1.3:", socialnumber)