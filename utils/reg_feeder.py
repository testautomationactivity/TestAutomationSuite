import logging
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils.log import logger

@dataclass
class RegFeeder:
    """

    """
    url: str

    def __post_init__(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--use_subprocess")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)

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

        reg = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, reg_path))
        ).text
        make = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, make_path))
        ).text
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
            logger.debug("Error message not found")
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


if __name__ == "__main__":
    from utils.configs import Configs
    from utils.file_data_reader import Reader

    import os

    patterns = Configs.REGEX_PATTERNS
    input_path = Configs.INPUT_FILE
    output_path = Configs.OUTPUT_FILE
    print(f"******************{Configs.ROOT_DIR}")
    rd = Reader(input_path)
    rd_x = Reader(output_path)
    input_data = rd.match_patterns_list(patterns)
    print(
        f"******************{input_data}"
    )
    output_data = rd_x.read_file()
    print(
        f"******************{output_data}"
    )

    print(f"Reg Numbers---------------->{input_data}")

    # reg = input_data[1]
    for reg in input_data:
        bot = RegFeeder(Configs.REG_VALUATION_URL)
        bot.enter_registration_number(reg)
        print(
            f"Registration number entered: {reg}"
        )
        bot.click_value_your_car()
        if bot.get_error_message():
            print(f"{bot.get_error_message()=}")
        else:
            data = bot.get_valuation_data()
            if data:
                print(f"{data=}")
                for key, val in data.items():
                    if key in output_data.keys():
                        assert val in output_data[key]




