import os
import types


def env_or_default(env_var: str, default: str):
    if isinstance(default, types.LambdaType):
        return os.environ.get(env_var) or default()

    return os.environ.get(env_var, default)

def match_variant_reg(input_strings):
    """

    :param txt:
    :return:
    """
    return [re.match(r'\w{4}', s).group() if re.match(r'\w{4}', s) else '' for s in input_strings]