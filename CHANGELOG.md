# [1.3](https://github.com/katonic-dev/explainit) (2022-11-3)

---

**Explainit 1.3 release introduces features & major bug fixes**

**Features**

- chore: Added unique_threshold input param ([5b822d9](https://github.com/katonic-dev/explainit/pull/41/commits/5b822d959531bc0d52010f534d87340f4477c570))

**Bug Fixes**

- docs: Updated the port in docs ([dbc4617](https://github.com/katonic-dev/explainit/commit/dbc4617e9801290a29ad75a2c2cf51a08ab1afd0))
- build: Updated pkg version ([cfea76d](https://github.com/katonic-dev/explainit/pull/41/commits/cfea76d7c9ad3040e65cef62737b2d2991bd7b16))
- docs: Updated screenshots ([f194cd5](https://github.com/katonic-dev/explainit/pull/41/commits/f194cd5acf05063af1a48238c3dffbe0bed2419a))
- docs: Added doc-string to build function ([615b8e3](https://github.com/katonic-dev/explainit/pull/41/commits/615b8e3b2178f3e705c9cb83c3840774e4b91588))
- fix: Fixed Typo ([fd3b39b](https://github.com/katonic-dev/explainit/pull/41/commits/fd3b39b70007a698fa332c954a08f63eb460441a))
- fix: Updated doc-string ([ef99f36](https://github.com/katonic-dev/explainit/pull/41/commits/ef99f3615e23725a0b32e638c913ea71ef0ec5bd))
- fix: Quoted the target name during exception ([3b48608](https://github.com/katonic-dev/explainit/pull/41/commits/3b486087ff15ae043ccc24912cd6d12426228e9e))
- docs: Added how to deploy on `custom routes` ([bf7761e](https://github.com/katonic-dev/explainit/pull/41/commits/bf7761ec412a42f3b4a21a820233df18a17d020b))
- docs: Updated getting-started example ([3c10746](https://github.com/katonic-dev/explainit/pull/41/commits/3c10746186b685f8fcd95c90d41d1eb8680dfac5))
- tutorial: Removed sklearn dependency ([cf7d083](https://github.com/katonic-dev/explainit/pull/41/commits/cf7d08370071b34e831ea61a435b92dbc62446f8))
- tutorial: Updated getting-started examples ([f1338d2](https://github.com/katonic-dev/explainit/pull/41/commits/f1338d28a6228c468f1783676a93484532279d63))
- docs: Added reference, production datasets ([b268cbe](https://github.com/katonic-dev/explainit/pull/41/commits/b268cbe55c14ac3063bfdbc6577384cf35183b4d))
- hooks: Removed large-files check hook ([36f2663](https://github.com/katonic-dev/explainit/pull/41/commits/36f266352fd15d59f9d7abbcde25b85a9509fda6))
- style: Added bgcolors to graphs ([5a88518](https://github.com/katonic-dev/explainit/pull/41/commits/5a885187b52f63a0278baa0d43c339af8ad87165))
- style: Updated histogram, scatter plots color, fixed `cat` graph title ([a2823c8](https://github.com/katonic-dev/explainit/pull/41/commits/a2823c8ccb2ea69f1edc8ed8bcb0cba85b081dc5))
- fix: Updated `correlation` table name ([a5b9352](https://github.com/katonic-dev/explainit/pull/41/commits/a5b9352d90ade1b4044cb691a5e5a499ab192717))
- fix: Updated title, highlighted graphs title ([b38b449](https://github.com/katonic-dev/explainit/pull/41/commits/b38b4496f8d54027c5ff5623a79ab2bc09ee0280))
- fix: Fixed the graphs title ([dbf19a7](https://github.com/katonic-dev/explainit/pull/41/commits/dbf19a7aaee64e2959d3a2f270533820e77b4181))
- fix: Updated P-value column name to P-value/Distance ([7e6f7cb](https://github.com/katonic-dev/explainit/pull/41/commits/7e6f7cb28bc9bfc6021c2e025b482008adf717f5))
- fix: Updated the stats-info `Column` to `Feature` ([42c628b](https://github.com/katonic-dev/explainit/pull/41/commits/42c628b707682dfe4cff98ed03ba5fefa487ae23))
- docs: Added repo url, contribution guide ([056537e](https://github.com/katonic-dev/explainit/pull/41/commits/056537e48a136c2ee6d11cd6f4b0426f707bfdbd))
- fix: Updated the default threshold for jensen, wd tests ([406e3d9](https://github.com/katonic-dev/explainit/pull/41/commits/406e3d9a614494ac33aa5c5150b348e19230241a))
- fix: Updated the `cat`, `num` filter condition ([3e4154d](https://github.com/katonic-dev/explainit/pull/41/commits/3e4154d7dc0ec041325fa5976f5e0c14bae8dc9b))
- fix: Fixed the drift logic with threshold ([e0cedec](https://github.com/katonic-dev/explainit/pull/41/commits/e0cedeccf1aadfdc2f16d2c88aaa2f36dcbff1e3))
- docs: Updated screenshots for data&feat summaries ([6c4cc7d](https://github.com/katonic-dev/explainit/pull/41/commits/6c4cc7d95bea4744832539100de26e89e6951fe4))
- fix: Capitalized labels ([763de35](https://github.com/katonic-dev/explainit/pull/41/commits/763de356466b760d6a7a7d83a29618b194287517))
- fix: Capitalized labels ([cd51213](https://github.com/katonic-dev/explainit/pull/41/commits/cd51213a57bbcca5527a5279ed634b02eee46f0a))
- fix: Capitalized labels for feature & df stats ([a56e395](https://github.com/katonic-dev/explainit/pull/41/commits/a56e39503efdd313a97d8a738ffcd5e8f23279da))
- fix: Updated app screenshots to latest ([fc32f05](https://github.com/katonic-dev/explainit/pull/41/commits/fc32f05c6b38ae29b73f11c8c935554f8bca5bd9))
- fix: Fixed the target-drift graph layout ([2a48e45](https://github.com/katonic-dev/explainit/pull/41/commits/2a48e4567d9e52f2dd4b9a2b9c553e46fa8ad0bd))
- fix: Update pkg installation command ([9b8185c](https://github.com/katonic-dev/explainit/pull/41/commits/9b8185c0f14f0f84e15f16abf64d6cb28fede95e))
- fix: removed tolist method as it is an integer ([b9a95d5](https://github.com/katonic-dev/explainit/pull/41/commits/b9a95d55bdd0a3ce5c44d97fb9c0525066735e95))

**Merged Pull Requests**

- update-ports ([5b1fcd8](https://github.com/katonic-dev/explainit/commit/5b1fcd8bd9421fb236ef6ea1ed91b34235d31edb))
- 38-doc-fix-update-app-screenshots ([#38](https://github.com/katonic-dev/explainit/issues/38))([3a452f5](https://github.com/katonic-dev/explainit/pull/41/commits/3a452f58e9acaaf554f67ff4124a68b50f90f491))
- 35-fr-add-unique-value-threshold-parameter ([#35](https://github.com/katonic-dev/explainit/issues/35))([2cdd07f](https://github.com/katonic-dev/explainit/pull/41/commits/2cdd07f7d3945275859b933e63bb12ab19fcada9))
- 27-doc-fix-update-documentation-for-routes ([#27](https://github.com/katonic-dev/explainit/issues/27))([72bd696](https://github.com/katonic-dev/explainit/pull/41/commits/72bd696e4bd2c29be9cbaf1084441b74f0d5395e))
- 31-bug-fix-the-cat-num-features-in-stats-info ([#31](https://github.com/katonic-dev/explainit/issues/31))([b8913fe](https://github.com/katonic-dev/explainit/pull/41/commits/b8913fe552f8cfd0492eb38ceae721e762009084))
- 32-bug-fix-the-drift-not-drift-logic-in-jensenshannon-test ([#32](https://github.com/katonic-dev/explainit/issues/32))([f13dcb6](https://github.com/katonic-dev/explainit/pull/41/commits/f13dcb6db8cb889b3936e1ed8447b72353647fee))
- 25-bug-index-column-issue-in-generating-graphs ([#25](https://github.com/katonic-dev/explainit/issues/25))([502587f](https://github.com/katonic-dev/explainit/pull/41/commits/502587f2edb52486cd69ab7b84b24461a14a95df))
- update-correlation-table-columns ([#23](https://github.com/katonic-dev/explainit/issues/23))([d23bd27](https://github.com/katonic-dev/explainit/commit/d23bd273e7a55047fa052b396502a8086b2c74b6))


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
