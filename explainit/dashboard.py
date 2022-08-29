# Copyright 2022 The Explainit Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY aIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
from typing import Any
from typing import Dict

import pandas as pd
from colorama import Fore
from colorama import Style
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import CatTargetDriftTab
from evidently.dashboard.tabs import DataDriftTab
from evidently.dashboard.tabs import DataQualityTab
from evidently.dashboard.tabs import NumTargetDriftTab


class DriftDashboard:
    """
    Dashboard object that will be used to calculate Data Drift, Target Drift and Data Quality using Evidently Library.

    Args:
        training_data: A pandas dataframe which contains the training data.
        production_data: A pandas dataframe which contains the production data.
        target_col_name: Name of the target column in your data.
        target_col_type: Type of the target feature whether the target feature inside the dataframe is belongs to a CategoricalFeature or NumericFeature.
    """

    def __init__(
        self,
        ref_data: pd.DataFrame,
        cur_data: pd.DataFrame,
        target_col_name: str,
        target_col_type: str,
    ):
        """
        Creates a Dictionary which contains Data drift, target drift and data quality.
        """
        self.ref_data = ref_data
        self.cur_data = cur_data
        self.target_col_name = target_col_name
        self.target_col_type = target_col_type

        self.json_data: Dict[str, Any] = {}
        self.ref_data.rename(columns={self.target_col_name: "target"}, inplace=True)
        self.cur_data.rename(columns={self.target_col_name: "target"}, inplace=True)

    def calculate(self):
        """
        Calculates the information regarding data drift, target drift and data quality.

        Returns:
            Dictionary with drift and quality information.
        """

        # Drift, Quality Dashboard
        if self.target_col_type == "cat":
            print(
                f"Analyzing {Style.BRIGHT + Fore.GREEN}Data Drift{Style.RESET_ALL}...[1/5]"
            )
            self.data_drift_dashboard = Dashboard(tabs=[DataDriftTab(verbose_level=1)])
            print(
                f"Analyzing {Style.BRIGHT + Fore.GREEN}Target Drift{Style.RESET_ALL}...[2/5]"
            )
            self.target_drift_dashboard = Dashboard(
                tabs=[
                    CatTargetDriftTab(verbose_level=1),
                ]
            )
            print(
                f"Analyzing {Style.BRIGHT + Fore.GREEN}Data Quality{Style.RESET_ALL}...[3/5]"
            )
            self.data_quality_dashboard = Dashboard(
                tabs=[
                    DataQualityTab(verbose_level=1),
                ]
            )

        elif self.target_col_type == "num":
            print(
                f"Analyzing {Style.BRIGHT + Fore.GREEN}Data Drift{Style.RESET_ALL}...[1/5]"
            )
            self.data_drift_dashboard = Dashboard(
                tabs=[
                    DataDriftTab(verbose_level=1),
                ]
            )
            print(
                f"Analyzing {Style.BRIGHT + Fore.GREEN}Target Drift{Style.RESET_ALL}...[2/5]"
            )
            self.target_drift_dashboard = Dashboard(
                tabs=[
                    NumTargetDriftTab(verbose_level=1),
                ]
            )
            print(
                f"Analyzing {Style.BRIGHT + Fore.GREEN}Data Quality{Style.RESET_ALL}...[3/5]"
            )
            self.data_quality_dashboard = Dashboard(
                tabs=[
                    DataQualityTab(verbose_level=1),
                ]
            )
        print(f"Analyzing {Style.BRIGHT + Fore.GREEN}results{Style.RESET_ALL}...[4/5]")
        self.data_drift_dashboard.calculate(
            self.ref_data,
            self.cur_data,
        )

        self.drift_data = json.loads(self.data_drift_dashboard._json())

        self.target_drift_dashboard.calculate(
            self.ref_data,
            self.cur_data,
        )

        self.target_drift_data = json.loads(self.target_drift_dashboard._json())

        self.data_quality_dashboard.calculate(
            self.ref_data,
            self.cur_data,
        )

        self.data_quality = json.loads(self.data_quality_dashboard._json())

        self.json_data["data_drift"] = self.drift_data
        self.json_data["target_drift"] = self.target_drift_data
        ref_data = [
            key["values"][0]
            for key in self.data_quality["widgets"][0]["params"]["metrics"]
        ]
        cur_data = [
            key["values"][1]
            for key in self.data_quality["widgets"][0]["params"]["metrics"]
        ]
        labels = [
            key["label"] for key in self.data_quality["widgets"][0]["params"]["metrics"]
        ]
        summary_df = pd.DataFrame(
            {"Metric": labels, "Reference Data": ref_data, "Current Data": cur_data}
        )
        df_data = (summary_df.to_dict("records"),)
        self.json_data["data_summary"] = df_data
        # json_data["data_summary"] = data["widgets"][0]
        self.json_data["feature_summary"] = self.data_quality["widgets"][1]["widgets"]
        self.json_data["correlation"] = self.data_quality["widgets"][2]

        return self.json_data

    def save(self, FILE_PATH):
        """
        Creates a file at the given directory.

        Args:
            FILE_PATH: Path to the file to be saved.

        Returns:
            Saves a json file at the given directory.
        """
        with open(FILE_PATH, "w") as handler:
            json.dump(self.json_data, handler)
