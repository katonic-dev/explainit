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
import pandas as pd
from explainit.dashboard import DriftDashboard
from explainit.utils import get_distr_graph_data
from explainit.utils import get_drift_graph_data
from explainit.utils import get_json_data
from explainit.utils import get_small_hist_data
from explainit.utils import get_stats_data
from explainit.utils import target_data_copy
from sklearn import datasets
from sklearn.model_selection import train_test_split

iris = datasets.load_breast_cancer()
iris_frame = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_frame["target"] = iris.target
ref_data, cur_data = train_test_split(iris_frame, train_size=0.80, shuffle=True)
data = DriftDashboard(ref_data, cur_data, "target", "cat").calculate()


(
    drift_data,
    target_data,
    data_summary,
    feature_summary,
    correlation_data,
) = get_json_data(data)

del data


def evaluate_small_hist_data_cur_len():

    small_hist_data_cur = get_small_hist_data(drift_data, "f4")
    assert len(small_hist_data_cur) == len(iris_frame.columns)


def evaluate_small_hist_data_ref_len():

    small_hist_data_ref = get_small_hist_data(drift_data, "f3")
    assert len(small_hist_data_ref) == len(iris_frame.columns)


def evaluate_stats_data_len():

    stats_data = get_stats_data(drift_data)
    assert len(stats_data) == len(iris_frame.columns)


def evaluate_drift_graph_data_len():

    drift_graph_data = get_drift_graph_data(drift_data)
    assert len(drift_graph_data) == len(iris_frame.columns)


def evaluate_distr_graph_data_len():

    distr_graph_data = get_distr_graph_data(drift_data)
    assert len(distr_graph_data) == len(iris_frame.columns)


def evaluate_tdd_copy_len():

    tdd_copy = target_data_copy(target_data)
    assert len(tdd_copy) == len(iris_frame.columns) - 1


if __name__ == "__main__":
    evaluate_small_hist_data_cur_len()
    evaluate_small_hist_data_ref_len()
    evaluate_stats_data_len()
    evaluate_drift_graph_data_len()
    evaluate_distr_graph_data_len()
    evaluate_tdd_copy_len()
