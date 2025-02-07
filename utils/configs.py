import os
import sys
from dotenv import load_dotenv
from utils.utilities import env_or_default

load_dotenv()

class Configs:
    """

    """
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    REG_VALUATION_URL = env_or_default("REG_VALUATION_URL", "https://motorway.co.uk")
    REGEX_PATTERNS = env_or_default("REGEX_PATTERNS", [r"\b[A-Z]{2}\d{2}\s?[A-Z]{3}\b"])
    OUTPUT_FILE = env_or_default("OUTPUT_FILE", f"{ROOT_DIR}\\testdata\\car_Output - V5.txt")
    INPUT_FILE = env_or_default("OUTPUT_FILE", f"{ROOT_DIR}\\testdata\\car_Input - V5.txt")
