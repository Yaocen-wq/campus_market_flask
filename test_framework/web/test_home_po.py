from pages.home_page import HomePage
from utils.data_loader import load_yaml

DATA = load_yaml("web/home.yaml")

def test_home_po(driver):
    page = HomePage(driver)
    page.open_page()
    assert DATA["expected_title"] in page.get_title()
