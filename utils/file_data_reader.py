import re
from dataclasses import dataclass

from utils.log import logger

@dataclass
class Reader:
    """
    Data Class to extract registration number from given txt file
    """

    txt_file_path: str

    def match_pattern(self, pattern):
        """

        :return:
        """
        reg_numbers_list = []
        try:
            with open(self.txt_file_path, "r") as lines:
                for ln in lines:
                    matches = re.findall(pattern, ln)
                    if matches:
                        reg_numbers_list.extend(matches)

        except FileNotFoundError:
            logger.error(f"{self.txt_file_path} NOT found")
        except Exception as e:
            logger.error(f"Error {e}")

        return reg_numbers_list

    def read_file(self):
        """

        :return:
        """
        results = {}

        with open(self.txt_file_path, "r") as lines:
            headers = lines.readline().strip().split(",")
            results = {header.strip(): [] for header in headers}
            for ln in lines:
                data = ln.strip().split(",")
                for header, value in zip(headers, data):
                    results[header.strip()].append(value.strip())
        return results

    def match_patterns_list(self, patterns):
        # TODO: return from dict
        pattern_list = []
        for x in patterns:
            pattern_list.extend(self.match_pattern(x))
        return pattern_list




if __name__ == "__main__":
    import os

    from utils.configs import Configs
    # logger = logging_config()
    # pattern = r"\b[A-Z]{2}\d{2}\s?[A-Z]{3}\b"
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

