from typing import List, Optional

import pandas as pd

from abfy.src.models.configuration_model.config import DiDConfig
from abfy.src.models.preprocessor_model.diff_in_diff.matching_preprocessor import (
    MatchingPreprocessor,
)
from abfy.src.models.preprocessor_model.diff_in_diff.prep_did_preprocessor import (
    PrepDiDPreprocessor,
)
from abfy.src.models.result_model.result import DiffinDiffPreprocessPipelineResult
from abfy.src.pipeline.preprocess_pipelines.preprocess_pipeline import BasePreprocessPipeline
from abfy.src.utils.error import InputConfigError
from abfy.src.utils.logger import logger


class DiffinDiffPreprocessPipeline(BasePreprocessPipeline):
    def __init__(
        self,
        config: DiDConfig,
        control_unit_ids: Optional[List[int]] = None,
    ):
        super().__init__(config)
        self.control_unit_ids = control_unit_ids

    def matching(self, data: pd.DataFrame) -> DiffinDiffPreprocessPipelineResult:
        data = self.execute_common_preprocesses(data)

        logger.info("Start market matching.....")
        matching_preprocessor = MatchingPreprocessor(config=self.config, control_unit_ids=self.control_unit_ids)
        matching_result = self.execute_preprocess(data, matching_preprocessor)
        logger.info("Finished market matching!")

        return DiffinDiffPreprocessPipelineResult(
            processed_data=matching_result.processed_data,
            matched_control_units=matching_result.matched_units,
        )

    def run(self, data: pd.DataFrame) -> DiffinDiffPreprocessPipelineResult:
        data = self.execute_common_preprocesses(data)

        if self.control_unit_ids is not None and len(self.control_unit_ids) > 0:
            self._validate_user_provided_control_units(self.control_unit_ids)
            logger.info("Using user provided control units in diff-in-diff and skip matching")

        # Run matching in order to find matched control units
        matching_result = self.matching(data)
        data = matching_result.processed_data

        # Feed matched control units in to the Prep Diff In Diff Preprocessor
        prep_did_preprocessor = PrepDiDPreprocessor(
            config=self.config, control_unit_ids=matching_result.matched_unit_ids
        )

        prep_did_result = self.execute_preprocess(data, prep_did_preprocessor)

        return DiffinDiffPreprocessPipelineResult(
            processed_data=prep_did_result.processed_data,
            matched_control_units=matching_result.matched_control_units,
        )

    def _validate_user_provided_control_units(self, control_units: List[int]):
        # check if provided list contains treatment unit ids
        if not set(self.config.treatment_unit_ids).isdisjoint(control_units):
            raise InputConfigError("Control units must not contain any treatment unit!")
