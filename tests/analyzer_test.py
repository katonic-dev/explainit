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
import unittest

import pandas as pd
from explainit.dashboard import DriftDashboard
from sklearn import datasets
from sklearn.model_selection import train_test_split

iris = datasets.load_breast_cancer()
iris_frame = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_frame["target"] = iris.target
ref_data, cur_data = train_test_split(iris_frame, train_size=0.80, shuffle=True)


class TestStringMethods(unittest.TestCase):
    def evaluate_json_length(self):
        data = DriftDashboard(ref_data, cur_data, "cat").calculate()

        keys = list(data.keys())
        self.assertEqual(len(keys), 5)

    def evaluate_json_keys(self):
        data = DriftDashboard(ref_data, cur_data, "cat").calculate()

        keys = list(data.keys())
        self.assertListEqual(
            keys,
            [
                "data_drift",
                "target_drift",
                "data_summary",
                "feature_summary",
                "correlation",
            ],
        )


if __name__ == "__main__":
    unittest.main()
