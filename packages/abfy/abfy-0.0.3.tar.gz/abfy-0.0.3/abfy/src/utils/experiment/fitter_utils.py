from typing import List, Optional, Tuple, Union

import pandas as pd

from abfy.src.models.configuration_model.base_objects import (
    ColumnType,
    Covariate,
    CovariateType,
    MetricType,
    TColumn,
)
from abfy.src.models.data_model import DataLoader
from abfy.src.utils.constants import Constants


def get_covariates_by_type(
    covariates: List[Covariate],
) -> Tuple[List[Covariate], List[Covariate], List[Covariate]]:
    # get covariates that need to calculate group mean
    categorical_covariates, numerical_covariates, ratio_covariates = [], [], []

    for covariate in covariates:
        if covariate.value_type == CovariateType.categorial:
            categorical_covariates.append(covariate)
        elif covariate.value_type == CovariateType.numerical:
            numerical_covariates.append(covariate)
        # TODO: distinguish between categorical and numerical ratio covariates
        elif covariate.value_type == CovariateType.ratio:
            ratio_covariates.append(covariate)
    return categorical_covariates, numerical_covariates, ratio_covariates


def get_demean_column_name(original_column_name: str) -> str:
    return f"{original_column_name}_{Constants.FIXED_EFFECT_DEMEAN_COLUMN_POSTFIX}"


def get_resid_column_name(column_name):
    return f"{column_name}_resid"


def get_column_names_for_fitter(columns: List[Optional[TColumn]]) -> List[str]:
    column_names = []
    for column in columns:
        if column:
            if column.column_type == ColumnType.metric and column.metric_type == MetricType.ratio:
                column_names.extend(
                    [
                        column.denominator_column.column_name,
                        column.numerator_column.column_name,
                    ]
                )
            else:
                if column.column_type == ColumnType.covariate and column.value_type == CovariateType.ratio:
                    column_names.extend(
                        [
                            column.denominator_column.column_name,
                            column.numerator_column.column_name,
                        ]
                    )
                else:
                    column_names.extend([column.column_name])
    return list(set(column_names))  # make sure no duplicate column names in list


def process_data_for_fitter(
    required_columns: List[Optional[TColumn]], data: Union[pd.DataFrame, DataLoader]
) -> pd.DataFrame:
    """
    To optimize for memory when input data has multiple columns, first create a copy of
    a subset of necessary data for fitter, then in-place remove the rows with missing values

    :param required_columns: required columns like experiment group, covariates for fitter
    :param data: input data feeding into the fitter
    :return: output data that only contains the required columns and without any missing value
    """
    column_names = get_column_names_for_fitter(required_columns)
    processed_data = data[[column for column in column_names if column in data.columns]].copy()
    processed_data.dropna(inplace=True)
    return processed_data
