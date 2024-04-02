from typing import List

import pandas as pd
from scipy.stats import skew, skewtest

from abfy.src.models.configuration_model.base_objects import (
    ExperimentGroup,
    Metric,
    MetricAggregateFunc,
    MetricType,
)
from abfy.src.models.message.message import Message, Source, Status
from abfy.src.models.preprocessor_model.base import BasePreprocessor
from abfy.src.models.result_model.result import PreprocessResult
from abfy.src.utils.constants import Constants
from abfy.src.utils.logger import logger

MESSAGE_TITLE = "Distribution check"


class DistributionPreprocessor(BasePreprocessor):
    def __init__(self, metrics: List[Metric], experiment_groups: List[ExperimentGroup]):
        self.metrics = metrics
        self.experiment_groups = experiment_groups

    def process(self, data: pd.DataFrame) -> PreprocessResult:
        """
        Check if the sample size is large enough to conduct t-tests
        Methodology is referring to Rule 7 in https://exp-platform.com/Documents/2014%20experimentersRulesOfThumb.pdf
        """

        preprocess_result = PreprocessResult(data)
        for metric in self.metrics:

            # Skip this metric if it is not eligible for checking the distribution
            if not (
                metric.check_distribution
                and metric.metric_aggregate_func == MetricAggregateFunc.mean
                and metric.metric_type == MetricType.continuous
            ):
                continue

            logger.info(f"Checking distribution for {metric.column_name}...")
            for group in self.experiment_groups:
                group_name = group.column_name
                data_to_use = data
                if metric.cluster:
                    cluster_name = metric.cluster.column_name
                    data_to_use = data.groupby([group_name] + [cluster_name])[metric.column_name].mean().reset_index()
                skewness = data_to_use.groupby(group_name)[metric.column_name].aggregate(skew)
                sample_size = data_to_use.groupby(group_name).size()
                # skew test only works when there are more 8 samples
                if any(sample_size <= Constants.DISTRIBUTION_SAMPLE_SIZE_THRESHOLD):

                    preprocess_result.message_collection.add_metric_message(
                        metric.column_name,
                        Message(
                            source=Source.validation,
                            status=Status.warn,
                            title=MESSAGE_TITLE,
                            description=f"{Constants.DISTRIBUTION_SAMPLE_SIZE_THRESHOLD} samples are required in group {group_name}",
                        ),
                    )

                else:
                    eligible = list(sample_size[sample_size > Constants.DISTRIBUTION_SAMPLE_SIZE_THRESHOLD].index)
                    skewtest_stats = (
                        data_to_use[data_to_use[group_name].isin(eligible)]
                        .groupby(group_name)[metric.column_name]
                        .aggregate(skewtest)
                    )
                    skewtest_pvalue = skewtest_stats.str[1]
                    if any(skewtest_pvalue < Constants.DISTRIBUTION_SKEW_PVALUE_THRESHOLD):
                        skewed_groups = list(
                            skewtest_pvalue[skewtest_pvalue < Constants.DISTRIBUTION_SKEW_PVALUE_THRESHOLD].index
                        )

                        preprocess_result.message_collection.add_metric_message(
                            metric.column_name,
                            Message(
                                source=Source.validation,
                                status=Status.warn,
                                title=MESSAGE_TITLE,
                                description=f"{metric.column_name} for {skewed_groups} is skewed",
                            ),
                        )

                if any(abs(skewness) > 1):
                    skewed_variations = list(skewness[abs(skewness) > 1].index)
                    sample_size_needed = 355 * skewness[skewed_variations] ** 2
                    sample_size = sample_size[skewed_variations]
                    variations_wo_enough_samples = list(sample_size[sample_size < sample_size_needed].index)
                    if len(variations_wo_enough_samples) > 0:
                        needed_samples = list(sample_size_needed[variations_wo_enough_samples].astype(int))

                        description = (
                            f"Not enough samples to test significance. \n"
                            f"Groups: {variations_wo_enough_samples}, needed samples: {needed_samples}"
                        )

                        preprocess_result.message_collection.add_metric_message(
                            metric.column_name,
                            Message(
                                source=Source.validation,
                                status=Status.warn,
                                title=MESSAGE_TITLE,
                                description=description,
                            ),
                        )

        return preprocess_result
