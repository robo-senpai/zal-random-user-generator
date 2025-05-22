import mylib.helpers as helper

def test_version_match(page):
    # check if the latest version of the live page is 1.4
    page.goto("https://randomuser.me/changelog")
    assert "Version 1.4" in page.content(), "Version 1.4 not found in changelog"

def test_new_nationalities(request_context):
    # Check if the India data is available in the latest version 1.4
    url = "https://randomuser.me/api/?nat=in"
    data = helper.fetch_json_data(request_context, url)
    country = data["results"][0]["location"]["country"]
    assert country == "India", f"Expected country 'India', got {country}"
    print("Country 1.4:", country)

    # Comparison with the previous version 1.3
    url = "https://randomuser.me/api/1.3/?nat=in"
    data = helper.fetch_json_data(request_context, url)
    country = data["results"][0]["location"]["country"]
    assert country != "India", f"Expected country other than 'India', got {country}"
    print("Country 1.3:", country)

    # Pozostale narodowości - może zbudować klasę?

    # Validate the addition of foreign SSNs
    # Brazil: CPF
    url = "https://randomuser.me/api/?nat=br"
    data = helper.fetch_json_data(request_context, url)
    socialnumber = helper.find_key_in_dict(data, "id") # "name" : "CPF", "vale" : ...
    assert socialnumber["name"] == "CPF", f"Expected 'name' to be 'CPF', got {socialnumber['name']}"
    print("Social Number 1.4:", socialnumber)