from typing import Union

import pandas as pd

from abfy.src.models.configuration_model.config import AbConfig
from abfy.src.models.data_model import DataLoader
from abfy.src.models.message.enums import Source, Status
from abfy.src.models.message.message import Message
from abfy.src.models.preprocessor_model.ab.distribution_preprocessor import (
    DistributionPreprocessor,
)
from abfy.src.models.preprocessor_model.ab.flicker_preprocessor import FlickerPreprocessor
from abfy.src.models.preprocessor_model.ab.imbalance_preprocessor import ImbalancePreprocessor
from abfy.src.models.result_model.result import AbPreprocessPipelineResult
from abfy.src.pipeline.preprocess_pipelines.preprocess_pipeline import BasePreprocessPipeline
from abfy.src.utils.logger import logger


class AbPreprocessPipeline(BasePreprocessPipeline):
    def __init__(self, config: AbConfig):
        super().__init__(config)
        self.config: AbConfig = config

    def run(self, data: Union[pd.DataFrame, DataLoader]) -> AbPreprocessPipelineResult:
        data = self.execute_common_preprocesses(data)

        result = AbPreprocessPipelineResult(processed_data=data)

        # For low mem mode, we only need small subset of columns to do these tests over
        required_cols = self._get_required_columns_for_preprocessing()
        subdf = data[required_cols] if isinstance(data, DataLoader) else data

        # Imbalance Check
        if self.config.is_check_imbalance:
            try:
                imb = ImbalancePreprocessor(
                    experiment_groups=self.config.experiment_groups,
                    experiment_randomize_units=self.config.experiment_randomize_units,
                    cluster=self.config.cluster,
                    check_imbalance_method=self.config.check_imbalance_method,
                )
                imbalance_result = self.execute_preprocess(subdf, imb)
                subdf = imbalance_result.processed_data
                result.are_buckets_imbalanced = imbalance_result.are_buckets_imbalanced
            except Exception as e:
                logger.error(f"Error while running imbalance test: {e}")

        # Flicker Check if needed. In lowmem mode flicker removal will do nothing.
        if self.config.is_check_flickers:
            try:
                flkr = FlickerPreprocessor(
                    experiment_groups=self.config.experiment_groups,
                    experiment_randomize_units=self.config.experiment_randomize_units,
                    cluster=self.config.cluster,
                    is_remove_flickers=self.config.is_remove_flickers,
                )
                flicker_result = self.execute_preprocess(subdf, flkr)
                subdf = flicker_result.processed_data
                result.does_flicker_exists = flicker_result.does_flicker_exists

                if isinstance(data, DataLoader) and self.config.is_remove_flickers:
                    msg = Message(
                        source=Source.validation,
                        status=Status.warn,
                        title="Can't flicker with lowmem mode.",
                        description="Low memory has not implemented flicker removal.",
                    )
                    flicker_result.message_collection.add_overall_message(msg)
            except Exception as e:
                logger.error(f"Error while running flicker test: {e}")

        # Distribution Check. Skip for data loader case bc requires reload for each metric.
        try:
            if not isinstance(data, DataLoader):
                dist = DistributionPreprocessor(self.config.metrics, self.config.experiment_groups)
                distribution_result = self.execute_preprocess(subdf, dist)
                subdf = distribution_result.processed_data
        except Exception as e:
            logger.error(f"Error while running distribution test: {e}")

        # Since data loader doesn't support deflickering, hold onto original object.
        result.processed_data = data if isinstance(data, DataLoader) else subdf

        return result

    def _get_required_columns_for_preprocessing(self):
        """
        When working from disk we only need a subset of columns to check for problems. To reduce
        memory footprint, only load those columns up. Returns column list.
        """
        cols = [eg.column_name for eg in self.config.experiment_groups if eg is not None]
        cols += [u.column_name for u in self.config.experiment_randomize_units if u is not None]
        cols += [c.column_name for c in [self.config.cluster] if c is not None]
        deduped_column_names = list(set(cols))

        return deduped_column_names
