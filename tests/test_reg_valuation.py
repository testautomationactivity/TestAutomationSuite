import pytest
from utils.file_data_reader import Reader
from utils.configs import Configs
from pages.landing_page import LandingPage

from utils.log import logger

def test_valid_registration_details(setup):
    patterns = Configs.REGEX_PATTERNS
    rd = Reader(Configs.INPUT_FILE)
    output_rd = Reader(Configs.OUTPUT_FILE)
    input_data = rd.match_patterns_list(patterns)
    logger.debug( f"Validate registration numbers {input_data}...")
    output_data = output_rd.read_file()
    logger.debug(f"{output_data=}...")
    for reg in input_data:
        logger.debug( f"Entering registration number {reg}...")
        enter_reg = LandingPage(setup)
        enter_reg.enter_registration_number(reg)
        enter_reg.click_value_your_car()
        if enter_reg.get_error_message():
            logger.warning(f"Registration number {reg} is invalid")
        else:
            reg_data = enter_reg.get_valuation_data()
            logger.debug(f"{reg_data=}...")
            if reg_data:
                for key, val in reg_data.items():
                    if key in output_data.keys():
                        assert val in output_data[key]
                        logger.info(f"{key} validated")
                logger.info(f"Registration number {reg} validated")




