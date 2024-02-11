import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.test_pages import TestPages

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="class")
def driver():
    try:
        logger.info("Initializing WebDriver...")
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.implicitly_wait(3)
        yield driver
    finally:
        logger.info("Closing WebDriver...")
        driver.quit()

class TestAddRemoveElements:
    def test_element_addition(self, driver):
        try:
            logger.info("Navigating to Add/Remove Elements page...")
            driver.get(TestPages.ADD_REMOVE_ELEMENTS_PAGE_URL)

            logger.info("Clicking 'Add Element' button...")
            add_button = driver.find_element(By.XPATH, "//button[text()='Add Element']")
            add_button.click()

            logger.info("Verifying element addition...")
            added_element = driver.find_element(By.CSS_SELECTOR, "#elements button")
            assert added_element.is_displayed(), "Element not added successfully"
        except Exception as e:
            logger.error("Error occurred during test execution: %s", str(e))
            raise

    def test_element_removal(self, driver):
        try:
            logger.info("Clicking 'Delete' button to remove the added element...")
            delete_button = driver.find_element(By.CSS_SELECTOR, "#elements button.added-manually")
            delete_button.click()

            logger.info("Verifying element removal...")
            added_element = driver.find_elements(By.CSS_SELECTOR, "#elements button.added-manually")
            assert len(added_element) == 0, "Element not removed successfully"
        except Exception as e:
            logger.error("Error occurred during test execution: %s", str(e))
            raise

if __name__ == "__main__":
    pytest.main()