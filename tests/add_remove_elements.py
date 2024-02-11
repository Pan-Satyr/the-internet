import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.test_pages import TestPages

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AddRemoveElements:
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
