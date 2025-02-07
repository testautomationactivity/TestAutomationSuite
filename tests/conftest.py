import pytest
from selenium import webdriver
from utils.configs import Configs
from utils.log import logger

@pytest.fixture(scope="function")
def setup(request):
    # Initialize the WebDriver (Chrome) instance
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--use_subprocess")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(Configs.REG_VALUATION_URL)

    driver.maximize_window()

    # Yield the driver instance
    yield driver

    # Quit the driver after tests are done
    driver.delete_all_cookies()
    driver.quit()

@pytest.fixture(scope="session", autouse=True)
def logger_config():
    logger.info("Automation test suite started")
    yield

def pytest_html_report_title(report):
    report.title = "Car Valuation Automation Test Report"