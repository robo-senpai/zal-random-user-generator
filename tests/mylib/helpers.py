import requests
from datetime import datetime, timezone

def check_status(url: str, expected_status: int = 200):
    response = requests.get(url)
    assert response.status_code == expected_status, (
        f"Expected status code {expected_status}, got {response.status_code}"
    )
    return response

def check_title_and_url(page, expected_title, expected_url):
    page.wait_for_load_state("load")
    assert expected_title in page.title(), "Page title does not match"
    assert page.url == expected_url, "URL does not match"
    print(page.title())
    print(page.url)

def wait_for_user_data_to_load(page, selector="#values_list li"):
    # Wait until the first li has a data-value that isn't '...'
    page.locator(selector).first.wait_for()
    
    # Wait a bit more to be sure all values are filled
    page.wait_for_timeout(1000)


def get_data_snapshot(page, selector):
    text_content = {}
    elements = page.locator(selector).element_handles()

    for item in elements:
        label = item.get_attribute("data-title")
        value = item.get_attribute("data-value")
        text_content[label] = value
    return text_content

def get_card_data(page):
    return get_data_snapshot(page, "#values_list li")

def fetch_json_data(_, url):
    response = requests.get(url)
    response.raise_for_status() # Ensure we raise an error for bad responses
    return response.json()

def find_key_in_dict(data, key):

    """Recursively search for a key in a nested dictionary or list."""

    if isinstance(data, dict):
        if key in data:
            return data[key]
        for k, v in data.items():
            result = find_key_in_dict(v, key)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_key_in_dict(item, key)
            if result is not None:
                return result
    return None

def calculate_years(date_input):
    
    print(f"[DEBUG] date_input: {date_input} ({type(date_input)})")

    """Calculate the number of years from a given date to today."""

    # first find the date in the json data (search by key 'dob' or 'registered'), result is a dictionary with 'date' key
    # convert date string to datetime object
    if isinstance(date_input, dict):
        date_str = date_input.get("date", "")
    else:
        date_str = date_input
    date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)

    # calculate the difference in years
    difference = now - date
    years = difference.days // 365.25
    return years