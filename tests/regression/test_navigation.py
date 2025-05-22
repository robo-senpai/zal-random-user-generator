import mylib.helpers as helper

def test_navigation_and_content(page):
        
        # 1. Navigate to the homepage and check title and URL
        page.goto("https://randomuser.me/")
        helper.check_title_and_url(page, "Random User Generator | Home", "https://randomuser.me/")

        # 2. Navigate to user photos
        page.click("text=Photos")
        helper.check_title_and_url(page, "Random User Generator | Photos", "https://randomuser.me/photos")

        # 3. Navigate to documentation
        page.click("text=Documentation")
        helper.check_title_and_url(page, "Random User Generator | Documentation", "https://randomuser.me/documentation")

        # Można w ten sposób sprawdzić pozostałe zakładki


def test_card_data_changes_on_refresh(page):
    page.goto("https://randomuser.me/")
    helper.wait_for_user_data_to_load(page)
    data_before = helper.get_card_data(page)

    page.reload()
    helper.wait_for_user_data_to_load(page)
    data_after = helper.get_card_data(page)
    
    print("Before:", data_before)
    print("After:", data_after)

    assert data_before != data_after, "Card data did not change after refresh"
