# [1.2](https://github.com/katonic-dev/explainit) (2022-10-8)

---

**Explainit 1.2 release introduces bug fixes**

**Bug Fixes**

- Updated naming convention, typo ([5fc4095]())
- Fixed typo in feature summary stats graph ([6dd7f9a](https://github.com/katonic-dev/explainit/commit/6dd7f9aa1a64376d460b11b1fe4f0295019d692f))
- Updated changelog ([6e2d32e](https://github.com/katonic-dev/explainit/commit/6e2d32e915ac1d8e7f3c574bfa69a740a9fb5e63))
- Updated release version ([29d5965](https://github.com/katonic-dev/explainit/commit/29d59652c3c57ef3e831effedc562f0f3d81f823))
- Update bug-report template ([9655ded](https://github.com/katonic-dev/explainit/commit/9655ded53bd1cec081841a75c0f97708d05a6cfb))
- Updated `current` dataset label to `production` ([2b563ed](https://github.com/katonic-dev/explainit/commit/2b563edb276790997f73039eb3cb8bf669fe7780))
- Updated architecture diagram ([5632a7a](https://github.com/katonic-dev/explainit/commit/5632a7aee061f1e17cc7506996c20c3d401380b0))
- Added type validation for input params ([9899702](https://github.com/katonic-dev/explainit/commit/9899702d18d571c3bdcc07cfcc10688318412d28))
- Updated `train-test` labels to `ref-prod` ([6d24e90](https://github.com/katonic-dev/explainit/commit/6d24e9000c95ae2644001f49a3f17add415cf5fb))
- Updated build function input params ([7ae5e19](https://github.com/katonic-dev/explainit/commit/7ae5e19f3a479812411e557f8538ece4e3681c3b))
- Update getting-started example ([348ac0d](https://github.com/katonic-dev/explainit/commit/348ac0ddc8f4ebf8d32ec796881e1567686d9c24))
- Updated Getting-started example with docs ([2a68460](https://github.com/katonic-dev/explainit/commit/2a68460782d08e882a9872d345006bf62fe41972))
- Updated features, drift definition ([89f5daa](https://github.com/katonic-dev/explainit/commit/89f5daaaf951b749ea469c27dfa77a167fba5631))
- Updated doc URLs ([a83a44d](https://github.com/katonic-dev/explainit/commit/a83a44db88d85f023fb14a87c7026cd9297e71a3))
- Changed colorpalette for histograms ([2cea54d](https://github.com/katonic-dev/explainit/commit/2cea54dfbe8bf012a5b2cdbdd01983a02636b352))
- Changed colorpalette for histograms ([52ac6c5](https://github.com/katonic-dev/explainit/commit/52ac6c53d2fc520291926fbbdae7c098ea227f0a))
- Expanded metric container by +5rem ([335d8c7](https://github.com/katonic-dev/explainit/commit/335d8c7113785ec94e491b7a3377f3e33204b67a))
- Added hr spacing below tabs section ([f01af59](https://github.com/katonic-dev/explainit/commit/f01af59486847e9a314ebe4c859266b94f8e7d5f))
- changed indicator, hist colors & added KDE ([c785b57](https://github.com/katonic-dev/explainit/commit/c785b57203b4eca1b876346cc0b8cb4f7cfea291))
- Removed unwanted horizontal space below tabs ([d7975f9](https://github.com/katonic-dev/explainit/commit/d7975f949cfb089d7df38336ac2c36306807cf97))
- Updated punctuation ([7b3ceca](https://github.com/katonic-dev/explainit/commit/7b3ceca4d15305d05a908278c946988acaabf290))
- Updated datetime in input params ([9689f02](https://github.com/katonic-dev/explainit/commit/9689f021e4610b6ab44535ab9b9948ba83d68195))
- Updated the output ([8d4771c](https://github.com/katonic-dev/explainit/commit/8d4771c24390f9fdf10658129c1511b7a1e5eca2))
- Updated the getting-started guide ([7680bf9](https://github.com/katonic-dev/explainit/commit/7680bf9db39418f58d90fe51cfebbf3eb8181315))
- Updated punctuation ([538e3a7](https://github.com/katonic-dev/explainit/commit/538e3a7e98c4f2b24ce472cb43c7384dd4169a94))
- Updated concept-drift definition, fixed typo ([88654d1](https://github.com/katonic-dev/explainit/commit/88654d13272dd4c4760cc426366e269055dbe8f9))


**Merged Pull Requests**

- 21-bug-fix-typo-in-feature-summary-stats ([#22](https://github.com/katonic-dev/explainit/pull/22)) ([40e7154](https://github.com/katonic-dev/explainit/commit/40e7154fb44482d6f91f4631b547df429fc84086))
- 19-doc-fix-update-release-version ([#20](https://github.com/katonic-dev/explainit/pull/20)) ([8a5f937](https://github.com/katonic-dev/explainit/commit/8a5f937f3a2c3ea9ce67a1ab7ad7ec8c371a4c18))
- 17-doc-fix-update-the-app-workflow ([#18](https://github.com/katonic-dev/explainit/pull/18)) ([e67edf7](https://github.com/katonic-dev/explainit/commit/e67edf7b15a6f0d7ffc73abd98455703142db826))
- 14-br-update-build-function-input-parameters ([#16](https://github.com/katonic-dev/explainit/pull/16)) ([59fdba5](https://github.com/katonic-dev/explainit/commit/59fdba5c4f74fc4a8a0c86262c2bad126388205b))
- 13-doc-fix-update-typo-punctuation ([#15](https://github.com/katonic-dev/explainit/pull/15)) ([812b1c0](https://github.com/katonic-dev/explainit/commit/812b1c0399dfb5c603406289560cbd095c1b4d7f))


# [1.1](https://github.com/katonic-dev/explainit) (2022-9-28)

---

**Explainit 1.1 release introduces major features**

**Features**

- [Python] Introducing 5 major Independent Statistical Tests (Chi-Square, Jensen-Shannon, Kolmogorov-Smirnov, Wasserstein-Distance, Z-Score) to calculate & Detect Drifts in Data (for both Batch Data and Production Data).
- [Python] Added Histograms, Pie-charts & Scatter Graphs modules for Data Quality Management, Data Summary & Feature Summary calculation.
- [Python] Added Correlation Graphs modules to get the insights of the relationship between features.
- [Python] Removed support for 2 Statistial Tests (Population Stability Index (PSI), Kullback Leibler Divergence (KL Div)).

**Documentation**

- Updated Contribution Guide.
- Updated Code-base Structure.
- Updated Explainit Documentation.
- Updated Explainit Tests.


# [1.0](https://github.com/katonic-dev/explainit) (2022-8-29)

---

**Explainit 1.0 general availability release introduces major features**

- Drift Detection (for both Features & Target)
- Data Quality Management

**Features**

- [Python] Introducing Explainit to Detect Drifts in Data (for both Batch Data and Production Data) at the same time.
- [Python] Introducing Explainit for Data Quality Management.
- [Python] Introducing Explainit Data Metrices to Understand the in-depth relationship between features and target as well as between the features.

**Documentation**

- Introducing Explainit documentation.
- Introducing end-to-end Tutorials Examples.
- Introducing Explainit Roadmap.
- Introducing Explainit Tests.
