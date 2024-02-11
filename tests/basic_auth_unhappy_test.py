import pytest
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from pages.test_pages import TestPages
from selenium.common.exceptions import TimeoutException

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


    # Verify unhappy path for authentication
    def test_basic_auth_unsuccessful_login(self, setup):
        try:
            logger.info("Navigating to URL with incorrect credentials...")
            setup.get(TestPages.BASIC_AUTH_UNHAPPY_URL)
            WebDriverWait(setup, 3).until(EC.url_contains("the-internet.herokuapp.com"))
            
            # Verify the user remains in homepage if the login is unsuccessful
            logger.info("User remains on the same page after unsuccessful login.")
        except TimeoutException:
            logger.error("Timeout occurred while waiting for the URL to contain the expected substring.")
            raise
        except Exception as e:
            logger.error("Error occurred during test execution: %s", str(e))
            raise

if __name__ == "__main__":
    pytest.main()