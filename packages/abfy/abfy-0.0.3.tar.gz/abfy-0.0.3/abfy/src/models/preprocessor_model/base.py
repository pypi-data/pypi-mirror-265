from typing import TypeVar

import pandas as pd

from abfy.src.models.result_model.result import PreprocessResult


class BasePreprocessor:
    def process(self, data: pd.DataFrame) -> PreprocessResult:
        raise NotImplementedError()


TBasePreprocessor = TypeVar("TBasePreprocessor", bound=BasePreprocessor)
