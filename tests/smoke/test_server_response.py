import mylib.helpers as helper

def test_homepage_up():
    helper.check_status("https://randomuser.me/")

def test_api_response_contains_results():
    response = helper.check_status("https://randomuser.me/api/")
    data = response.json()
    assert data is not None, "Response JSON is empty"
    assert 'results' in data, "Response JSON does not contain 'results' key"