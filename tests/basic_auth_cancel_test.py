import pytest
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.test_pages import TestPages
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

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
            

    # Verify redirection on clicking 'Cancel' from the login modal
    def test_basic_auth_cancel_redirect(self, setup):
        try:
            logger.info("Navigating to URL and clicking 'Cancel'...")
            setup.get(TestPages.BASIC_AUTH_URL)
        
            # Simulate pressing the ESC key to dismiss the authentication dialog
            actions = ActionChains(setup)
            actions.send_keys(Keys.ESCAPE).perform()
            logger.info("Pressed ESC key to dismiss authentication dialog.")
        
            # Wait for the redirect
            WebDriverWait(setup, 10).until(EC.url_to_be("https://the-internet.herokuapp.com/basic_auth"))
            logger.info("Redirected to the expected URL after clicking 'Cancel'.")

            # Wait for the body content to be loaded
            logger.info("Waiting for the body content to be loaded...")
            WebDriverWait(setup, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
            logger.info("Body content loaded.")
        
            # Get the body text
            logger.info("Getting body text...")
            body_text = setup.find_element(By.TAG_NAME, 'body').text
            logger.info(f"Body text: {body_text}")
        
            # Verify the page content
            assert "Not authorized" in body_text
            logger.info("User redirected to 'Not authorized' page after clicking 'Cancel'.")
        except TimeoutException:
            logger.error("Timeout occurred while waiting for the redirect.")
            raise
        except Exception as e:
            logger.error("Error occurred during test execution: %s", str(e))
            raise
        input("Press any key to close the browser...")

if __name__ == "__main__":
    pytest.main()