from fairlearn.metrics import MetricFrame
from fairlearn.metrics import (
    count,
    selection_rate,
    equalized_odds_difference,
    false_positive_rate,
    false_negative_rate,


    true_negative_rate,
    true_positive_rate,

    demographic_parity_difference,
    demographic_parity_ratio,
    equalized_odds_difference,
    equalized_odds_ratio,
)

from pydantic import BaseModel
import typing
import numpy as np
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
from sklearn.metrics import confusion_matrix, precision_score
from typing import Any,Dict

class Fairness(BaseModel):
    task_type: Any = "fairness"
    evaluation_type: Any = "fairness"

    references: typing.Any = None
    predictions: typing.Any = None
    sensitive_features: typing.Any = None
    prediction_scores: typing.Any = None
    label_type: str = "binary"

    metrics_to_report = [

        "balanced_accuracy",
        "balanced_acc_error",
        "selection_rate",
        "false_positive_rate",
        "false_positive_error",
        "false_negative_rate",
        "false_positive_error"

        "true_positive_rate",
        "true_negative_rate",

        "demographic_parity_difference",
        "demographic_parity_ratio",
        "equalized_odds_difference",
        "equalized_odds_ratio",
        "equalized_odds",
    ]

    kwargs: dict = {}

    def setup_kwargs(self):
        if "average" not in self.kwargs:
            if self.label_type == "multilabel":
                self.kwargs["average"] = "micro"

    def compute_error_metric(self, metric_value, sample_size):
        """Compute standard error of a given metric based on the assumption of
        normal distribution.

        Parameters:
        metric_value: Value of the metric
        sample_size: Number of data points associated with the metric

        Returns:
        The standard error of the metric
        """
        metric_value = metric_value / sample_size
        return (
            1.96
            * np.sqrt(metric_value * (1.0 - metric_value))
            / np.sqrt(sample_size)
        )

    def false_positive_error(self, y_true, y_pred):
        """Compute the standard error for the false positive rate estimate."""
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return self.compute_error_metric(fp, tn + fp)

    def false_negative_error(self, y_true, y_pred):
        """Compute the standard error for the false negative rate estimate."""
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return self.compute_error_metric(fn, fn + tp)

    def balanced_accuracy_error(self, y_true, y_pred):
        """Compute the standard error for the balanced accuracy estimate."""
        fpr_error, fnr_error = self.false_positive_error(
            y_true, y_pred
        ), self.false_negative_error(y_true, y_pred)
        return np.sqrt(fnr_error**2 + fpr_error**2) / 2

    def true_positive_parity(self, y_pred, y_true, sensitive_features):
        """Calculate True Positive Parity."""
        if sensitive_features is None:
            conf_mat = confusion_matrix(y_true, y_pred)
            tpr = conf_mat[1, 1] / (conf_mat[1, 0] + conf_mat[1, 1])
            return tpr
        else:
            conf_matrices = {}
            for sens_group in np.unique(sensitive_features):
                mask = (sensitive_features == sens_group)
                y_pred_group = y_pred[mask]
                y_true_group = y_true[mask]
                conf_matrices[sens_group] = confusion_matrix(
                    y_true_group, y_pred_group)

            # Calculate true positive rates for each group
            tpr_rates = {}
            for group, conf_mat in conf_matrices.items():
                tpr = conf_mat[1, 1] / (conf_mat[1, 0] + conf_mat[1, 1])
                tpr_rates[group] = tpr

            # Convert dict_values to lists
            tpr_rates = list(tpr_rates.values())

            return max(tpr_rates) - min(tpr_rates)

    def false_positive_parity(self, y_pred, y_true, sensitive_features):
        """Calculate False Positive Parity."""
        if sensitive_features is None:
            conf_mat = confusion_matrix(y_true, y_pred)
            fpr = conf_mat[0, 1] / (conf_mat[0, 1] + conf_mat[0, 0])
            return fpr
        else:
            conf_matrices = {}
            for sens_group in np.unique(sensitive_features):
                mask = (sensitive_features == sens_group)
                y_pred_group = y_pred[mask]
                y_true_group = y_true[mask]
                conf_matrices[sens_group] = confusion_matrix(
                    y_true_group, y_pred_group)

            # Calculate false positive rates for each group
            fpr_rates = {}
            for group, conf_mat in conf_matrices.items():
                fpr = conf_mat[0, 1] / (conf_mat[0, 1] + conf_mat[0, 0])
                fpr_rates[group] = fpr

            # Convert dict_values to lists
            fpr_rates = list(fpr_rates.values())

            return max(fpr_rates) - min(fpr_rates)

    def predictive_value_parity(self, y_pred, y_true, sensitive_features):
        """Calculate Predictive Value Parity."""
        if sensitive_features is None:
            precision = precision_score(y_true, y_pred)
            return precision
        else:
            precisions = {}
            for sens_group in np.unique(sensitive_features):
                mask = (sensitive_features == sens_group)
                y_pred_group = y_pred[mask]
                y_true_group = y_true[mask]
                precisions[sens_group] = precision_score(
                    y_true_group, y_pred_group)

            # Convert dict_values to lists
            precisions = list(precisions.values())
            return max(precisions) - min(precisions)

    def equalized_odds_refined(self, y_pred, y_true, sensitive_features):
        """Calculate Equalized Odds."""
        tpp = self.true_positive_parity(y_pred, y_true, sensitive_features)
        fpp = self.false_positive_parity(y_pred, y_true, sensitive_features)

        return {'tpp_diff': tpp, 'fpp_diff': fpp}

    # def equalized_odds(self,y_pred, y_true, sensitive_features):

    #     if sensitive_features is None:
    #         conf_mat = confusion_matrix(y_true, y_pred)
    #         fp = conf_mat[0,1] / (conf_mat[0,1] + conf_mat[0,0])
    #         fn = conf_mat[1,0] / (conf_mat[1,0] + conf_mat[1,1])
    #         return abs(fp - fn) < 0.05
    #     else:
    #         conf_matrices = {}
    #         for sens_group in np.unique(sensitive_features):
    #             mask = (sensitive_features == sens_group)
    #             y_pred_group = y_pred[mask]
    #             y_true_group = y_true[mask]
    #             conf_matrices[sens_group] = confusion_matrix(y_true_group, y_pred_group)

    #         # Calculate false positive and false negative rates for each group
    #         fp_rates = {}
    #         fn_rates = {}
    #         for group, conf_mat in conf_matrices.items():
    #             fp = conf_mat[0,1] / (conf_mat[0,1] + conf_mat[0,0])
    #             fn = conf_mat[1,0] / (conf_mat[1,0] + conf_mat[1,1])
    #             fp_rates[group] = fp
    #             fn_rates[group] = fn

    #         # Check if false positive and false negative rates are approximately equal
    #         # print("False positive rates:")
    #         # print(fp_rates)
    #         # print("False negative rates:")
    #         # print(fn_rates)
    #         # Convert dict_values to lists
    #         fp_rates = list(fp_rates.values())
    #         fn_rates = list(fn_rates.values())

    #         avg_fp_rate = np.mean(fp_rates)
    #         avg_fn_rate = np.mean(fn_rates)

    #         diff = np.abs(avg_fp_rate - avg_fn_rate)

    #         return diff

    def setup(self):
        self.setup_kwargs()

    def compute(self):

        self.setup()

        fairness_metrics: dict = {
            # "count": count,
            "balanced_accuracy": balanced_accuracy_score,
            "balanced_acc_error": self.balanced_accuracy_error,
            "selection_rate": selection_rate,
            "false_positive_rate": false_positive_rate,
            "false_positive_error": self.false_positive_error,
            "false_negative_rate": false_negative_rate,
            "false_negative_error": self.false_negative_error,

            "true_positive_rate": true_positive_rate,
            "true_negative_rate": true_negative_rate,

        }

        demography_metrics: dict = {

            "demographic_parity_difference": demographic_parity_difference,
            "demographic_parity_ratio": demographic_parity_ratio,
            "equalized_odds_difference": equalized_odds_difference,
            "equalized_odds_ratio": equalized_odds_ratio,
            "true_positive_parity": self.true_positive_parity,
            "false_positive_parity": self.false_positive_parity,
            "predictive_value_parity": self.predictive_value_parity,
            # "equalized_opportunity": self.equalized_odds_refined
        }

        metrics = {}

        for metric_name, metric_func in fairness_metrics.items():
            try:
                metrics[metric_name] = {'value': metric_func(
                    y_true=self.references, y_pred=self.predictions)}
            except Exception as e:
                print("Unable to compute", metric_name)
                print(e)

        for metric_name, metric_func in demography_metrics.items():
            try:  # Converted them to list to add Status and Risk Analysis afterwards.
                # metrics[metric_name] = [metric_func(
                #     y_true=self.references, y_pred=self.predictions,
                #     sensitive_features=self.sensitive_features)]

                # Converting them to dict.
                metrics[metric_name] = {'value': metric_func(
                    y_true=self.references, y_pred=self.predictions,
                    sensitive_features=self.sensitive_features)}
            except Exception as e:
                print("Unable to compute", metric_name)
                print(e)

        return metrics

        # metricframe_unmitigated = MetricFrame(
        #     metrics=fairness_metrics,
        #     y_true=self.references,
        #     y_pred=self.predictions,
        #     sensitive_features=self.sensitive_features,
        # )

        # metricframe_unmitigated.by_group[self.metrics_to_report]

        # metricframe_unmitigated.difference()[self.metrics_to_report]

        # met = metricframe_unmitigated.overall[self.metrics_to_report]

        # met = met.to_dict()

        # print("met", met)


# {'balanced_accuracy': 0.5100950394181764,
#  'balanced_acc_error': 0.01100533987433068,
#  'selection_rate': 0.34114285714285714,
#  'false_positive_rate': 0.3366760425583955,
#  'false_positive_error': 0.010243020003662515,
#  'false_negative_rate': 0.6431338786052518}


# {'balanced_accuracy': 0.5087131092423438,
#  'balanced_acc_error': 0.010994738119548174,
#  'selection_rate': 0.34114285714285714,
#  'false_positive_rate': 0.337287513758102,
#  'false_positive_error': 0.010247590942302624,
#  'false_negative_rate': 0.6452862677572105}

# balanced_accuracy      0.019392
# false_positive_rate    0.002971
# false_negative_rate    0.035814
