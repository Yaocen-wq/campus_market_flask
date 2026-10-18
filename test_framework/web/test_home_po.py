from pages.home_page import HomePage
def test_home_po(driver):
    page = HomePage(driver)
    page.open_page()
    assert "首页" in page.get_title()