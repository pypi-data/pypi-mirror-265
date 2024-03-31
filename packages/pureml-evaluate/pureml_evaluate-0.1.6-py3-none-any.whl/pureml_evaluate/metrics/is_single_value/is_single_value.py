from pureml_evaluate.metrics.data_metric_base import DataMetricBase
import pandas as pd
from typing import Any
from pydantic import ConfigDict


class IsSingleValue(DataMetricBase):
    name: Any = 'is_single_value'
    input_type: Any = 'dataframe'
    output_type: Any = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def parse_data(self, data):
        return data

    def compute(self, data, **kwargs):
        data_columns = data.columns
        data_columns = data_columns.tolist()

        single_value_columns = []
        for column in data_columns:
            if data[column].nunique() == 1:
                single_value_columns.append(column)

        return {
            self.name: single_value_columns
        }
