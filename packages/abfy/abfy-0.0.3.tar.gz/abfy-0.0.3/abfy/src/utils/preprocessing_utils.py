

from typing import Any

import pandas as pd

from abfy.src.models.configuration_model.base_objects import HypothesisTesting


def is_normal_distribution(data: pd.DataFrame, column_name: str) -> bool:
    return True


def decide_hypothesis_test_type(info: Any):
    return HypothesisTesting.t_test
