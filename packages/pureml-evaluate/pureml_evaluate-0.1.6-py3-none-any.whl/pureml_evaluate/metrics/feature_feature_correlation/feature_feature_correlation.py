import pandas as pd
from pureml_evaluate.metrics.data_metric_base import DataMetricBase
from typing import Any


class FeatureFeatureCorrelation(DataMetricBase):
    name: Any = 'feature_feature_correlation'
    input_type: Any = 'dataframe'
    output_type: Any = pd.DataFrame

    def parse_data(self, data):
        return data

    def compute(self, data, **kwargs):
        correlation_matrix = data.corr()

        return {
            self.name: correlation_matrix
        }
