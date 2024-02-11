import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.test_pages import TestPages

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestBasicAuth:
    @pytest.fixture(autouse=True)
    # Initialize WebDriver instance
    def setup(self):
        try:
            logger.info("Initializing WebDriver...")
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
            self.driver.implicitly_wait(3)
            yield self.driver
        except Exception as e:
            logger.error(
                "Error occurred during WebDriver initialization: %s", str(e))
            raise
        finally:
            logger.info("Closing WebDriver...")
            self.driver.quit()

    # Verify happy path for authentication
    def test_basic_auth_successful_login(self, setup):
        try:
            logger.info("Navigating to url with correct credentials...")
            setup.get(TestPages.BASIC_AUTH_HAPPY_URL)
            
            # Verify the successful login page
            main_content = self.driver.find_element(
                By.CSS_SELECTOR, ".example")
            assert main_content.is_displayed()
            logger.info("Main content visibility verification successful.")
           
            h3_element = main_content.find_element(By.TAG_NAME, "h3")
            assert h3_element.text == "Basic Auth"
            logger.info("Verified presence of 'Basic Auth' heading.")

            p_element = main_content.find_element(By.TAG_NAME, "p")
            expected_text = "Congratulations! You must have the proper credentials."
            assert p_element.text == expected_text
            logger.info("Verified presence of expected paragraph text.")
        except Exception as e:
            logger.error("Error occurred during test execution: %s", str(e))
            raise

if __name__ == "__main__":
    pytest.main()