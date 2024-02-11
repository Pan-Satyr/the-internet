import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.test_pages import TestPages

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestABTestPage:
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

    # Test to verify page title, main content, and specific text
    def test_page_rendering(self, setup):
        try:
            logger.info("Navigating to AB Test page...")
            setup.get(TestPages.ABTEST)
            assert "The Internet" in self.driver.title
            logger.info("Page title verification successful.")

            main_content = self.driver.find_element(
                By.CSS_SELECTOR, ".example")
            assert main_content.is_displayed()
            logger.info("Main content visibility verification successful.")

            # Check specific text within elements
            h3_element = main_content.find_element(By.TAG_NAME, "h3")
            assert h3_element.text == "A/B Test Control"
            logger.info("Verified presence of 'A/B Test Control' heading.")

            p_element = main_content.find_element(By.TAG_NAME, "p")
            expected_text = "Also known as split testing. This is a way in which businesses are able to simultaneously test and learn different versions of a page to see which text and/or functionality works best towards a desired outcome (e.g. a user action such as a click-through)."
            assert p_element.text == expected_text
            logger.info("Verified presence of expected paragraph text.")
        except Exception as e:
            logger.error("Error occurred during test execution: %s", str(e))
            raise


if __name__ == "__main__":
    pytest.main()
