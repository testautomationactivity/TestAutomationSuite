from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.configs import Configs

from utils.log import logger

@dataclass
class LandingPage:
    """

    """
    driver: webdriver.Chrome

    def enter_registration_number(self, reg_number):
        """

        :return:
        """
        input_field = (By.ID, "vrm-input")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(input_field)
            ).clear()
            logger.debug("Registration number cleared")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(input_field)
            ).send_keys(reg_number)
            logger.debug(f"Registration number entered: {reg_number}")
        except TimeoutException:
            logger.error("Registration number input field not found")
            raise

    def click_value_your_car(self):
        x_path = '//*[@id="main"]/div[1]/div[3]/div/div[2]/div/div/div/section/form/button'
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, x_path))
            ).click()
            logger.debug("Clicked submit button")
        except TimeoutException:
            logger.error("submit button not responding")
            raise

    def get_valuation_data(self):
        results = {}
        reg_path = '/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div/div/div/div[1]/div/div[2]'
        make_path = '/html/body/div[2]/div[2]/div[2]/div[1]/div[3]/div/div[2]/div/div/div/div[1]/h1'

        reg = self.get_element_text((By.XPATH, reg_path))
        make = self.get_element_text((By.XPATH, make_path))
        # year = get_element_text((By.CLASS_NAME, ""))
        # reg_ = get_element_text((By.CLASS_NAME, ""))
        # transmission = get_element_text((By.CLASS_NAME, ""))
        # fuel = get_element_text((By.CLASS_NAME, ""))

        results["VARIANT_REG"] = reg
        results["MAKE_MODEL"] = make
        print(f"{self.driver.current_url=}")
        logger.info(f"result found: {results}")
        return results

    def get_error_message(self):
        try:
            # wait the ready state to be complete
            WebDriverWait(driver=self.driver, timeout=20).until(
                lambda x: x.execute_script("return document.readyState === 'complete'")

            )
            error_message_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '#app > div.Toast-shared-module__toasterContainer-muon > ol')
                )
            )
            error_message = error_message_element.text
            logger.debug(f"Error message found: {error_message}")

            return error_message
        except TimeoutException:
            logger.error("Error message not found")
            return ""

    def shutdown_driver(self):
        self.driver.delete_all_cookies()
        self.driver.quit()

    def get_element_text(self, locator):
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((locator))
            ).text
        except TimeoutException:
            logger.error("result label not found")
            return ""
