import mylib.helpers as helper

# Test to ensure that navigation through the site works correctly
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

    # 4. Navigate to change log
    page.click("text=Change Log")
    helper.check_title_and_url(page, "Random User Generator | Change Log", "https://randomuser.me/changelog")

    # 5. Navigate to stats
    page.click("text=Stats & Graphs")
    helper.check_title_and_url(page, "Random User Generator | Statistics", "https://randomuser.me/stats")

    # 6. Navigate to donate
    page.click("text=Donate")
    helper.check_title_and_url(page, "Random User Generator | Donate", "https://randomuser.me/donate")

    # 7. Navigate to copyright
    page.click("text=Copyright Notice")
    helper.check_title_and_url(page, "Random User Generator | Copyright", "https://randomuser.me/copyright")

    # 8. Navigate to PS extension
    page.click("text=Photoshop Extension")
    helper.check_title_and_url(page, "Random User Generator | Photoshop Extension", "https://randomuser.me/photoshop")

    # 9. Navigate to the homepage again
    page.click("text=Home")
    helper.check_title_and_url(page, "Random User Generator | Home", "https://randomuser.me/")


# Test to ensure that card data changes on page refresh
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
