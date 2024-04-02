

import sys
import traceback
from typing import List, TypeVar

from abfy.src.models.configuration_model.config import BaseConfig
from abfy.src.models.message.message import Message, MessageCollection, Source, Status
from abfy.src.models.result_model.result import AnalysisResult, BasePreprocessPipelineResult
from abfy.src.utils.experiment.group_sequential import GroupSequentialTest
from abfy.src.utils.experiment.result_utils import filter_analysis_results
from abfy.src.utils.logger import logger


class BaseAnalyser:
    def __init__(self, config: BaseConfig, preprocess_result: BasePreprocessPipelineResult, **kwargs):
        self.config = config
        self.preprocess_result = preprocess_result
        self._args = kwargs
        self.group_sequential = GroupSequentialTest()
        self.message_collection = MessageCollection()
        self.fitter_dict = {}

    def _analysis(self) -> List[AnalysisResult]:
        results = []
        for metric in self.config.metrics:
            try:
                result = self._analyze_metric(metric)
                results.extend(result)
            except Exception as e:
                # Rip out the string representation that would be formed by print_exception()
                exc_type, exc_value, exc_traceback = sys.exc_info()
                exceptions = traceback.format_exception(exc_type, exc_value, exc_traceback)

                # Add a catchall message
                self.message_collection.add_metric_message(
                    metric.column_name,
                    Message(
                        source=Source.analysis,
                        status=Status.fail,
                        title=f"Unable to analyze metric {metric.column_name}",
                        description=f"""unable to analyze metric {metric.column_name} due to {e}, will skip: {"".join(exceptions)}""",
                    ),
                )
        return results

    def _analyze_metric(self, metric) -> List[AnalysisResult]:
        raise NotImplementedError

    def run(self) -> List[AnalysisResult]:
        logger.info("Start analyzing....")
        analysis_results = self._analysis()
        validated_analysis_results, message_collection = filter_analysis_results(analysis_results)
        self.message_collection.combine(message_collection)
        logger.info("Finished experiment analysis!")
        return validated_analysis_results


TBaseAnalyser = TypeVar("TBaseAnalyser", bound=BaseAnalyser)
