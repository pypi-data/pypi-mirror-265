from typing import Union

import pandas as pd

from abfy.src.models.configuration_model.config import BaseConfig
from abfy.src.models.data_model import DataLoader
from abfy.src.models.message.message import MessageCollection
from abfy.src.models.preprocessor_model.ab.log_transform_preprocessor import (
    LogTransformPreprocessor,
    LowMemLogXformPreprocessor,
)
from abfy.src.models.preprocessor_model.base import TBasePreprocessor
from abfy.src.models.result_model.result import BasePreprocessPipelineResult, PreprocessResult


class BasePreprocessPipeline:
    def __init__(self, config: BaseConfig):
        self.config = config
        self.message_collection: MessageCollection = MessageCollection()

    def execute_common_preprocesses(self, data: Union[pd.DataFrame, DataLoader]) -> pd.DataFrame:
        result = PreprocessResult(data)
        # Log Transforms
        for metric in self.config.metrics:
            if metric.log_transform:
                if isinstance(data, DataLoader):
                    result = self.execute_preprocess(data, LowMemLogXformPreprocessor(column_name=metric.column_name))
                else:
                    result = self.execute_preprocess(data, LogTransformPreprocessor(column_name=metric.column_name))

        return result.processed_data

    def execute_preprocess(self, data: pd.DataFrame, preprocessor: TBasePreprocessor) -> PreprocessResult:
        result = preprocessor.process(data)
        self.message_collection.combine(result.message_collection)
        return result

    def run(self, data: Union[pd.DataFrame, DataLoader]) -> BasePreprocessPipelineResult:
        raise NotImplementedError()
