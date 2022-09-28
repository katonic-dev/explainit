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
import numpy as np
import pandas as pd
from explainit.stattests.chi2_test import chi_stat_test
from explainit.stattests.z_test import z_stat_test
from pytest import approx


def test_freq_obs_eq_freq_exp() -> None:
    # observed and expected frequencies is the same
    reference = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 18, 16, 14, 12, 12])
    current = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 16, 16, 16, 16, 8])
    assert chi_stat_test(reference, current, 0.5) == (
        approx(0.67309, abs=1e-5),
        False,
        0.5,
    )


def test_chi_stat_test_cat_feature() -> None:
    reference = pd.Series(["a", "b", "c"]).repeat([10, 10, 10])
    current = pd.Series(["a", "b", "c"]).repeat([10, 10, 10])
    assert chi_stat_test(reference, current, 0.5) == (approx(1.0, abs=1e-5), False, 0.5)


def test_z_stat_test_cat_feature() -> None:
    reference = pd.Series(["a", "b"]).repeat([10, 10])
    current = pd.Series(["a", "b"]).repeat([10, 10])
    assert z_stat_test(reference, current, 0.5) == (approx(1.0, abs=1e-5), False, 0.5)


def test_cat_feature_with_nans() -> None:
    reference = pd.Series(["a", "b", np.nan]).repeat([10, 10, 10])
    current = pd.Series(["a", "b", np.nan]).repeat([10, 10, 10])
    assert chi_stat_test(reference, current, 0.5) == (approx(1.0, abs=1e-5), False, 0.5)


def test_freq_obs_not_eq_freq_exp() -> None:
    # observed and expected frequencies is not the same
    reference = pd.Series([1, 2, 3, 4, 5, 6]).repeat(
        [x * 2 for x in [16, 18, 16, 14, 12, 12]]
    )
    current = pd.Series([1, 2, 3, 4, 5, 6]).repeat([16, 16, 16, 16, 16, 8])
    assert chi_stat_test(reference, current, 0.5) == (
        approx(0.67309, abs=1e-5),
        False,
        0.5,
    )
