from typing import List

import pandas as pd

from abfy.src.models.configuration_model.config import DiDConfig
from abfy.src.models.preprocessor_model.base import BasePreprocessor
from abfy.src.models.result_model.result import PreprocessResult
from abfy.src.utils.diff_in_diff.prep_data import (
    get_data_between_start_end_date,
    prep_data_for_diff_in_diff,
)


class PrepDiDPreprocessor(BasePreprocessor):
    def __init__(self, config: DiDConfig, control_unit_ids: List[int]):
        self.config = config
        self.control_unit_ids = control_unit_ids

    def process(self, data: pd.DataFrame) -> PreprocessResult:
        """prepare data for diff in diff analysis"""
        experiment_data = get_data_between_start_end_date(
            data,
            self.config.date.column_name,
            self.config.matching_start_date,
            self.config.experiment_end_date,
        )

        diff_in_diff_data = prep_data_for_diff_in_diff(
            experiment_data,
            self.config.treatment_unit_ids,
            self.control_unit_ids,
            self.config.experiment_randomize_units[0].column_name,
            self.config.date.column_name,
            self.config.experiment_start_date,
        )

        preprocess_result = PreprocessResult(processed_data=diff_in_diff_data)
        return preprocess_result
