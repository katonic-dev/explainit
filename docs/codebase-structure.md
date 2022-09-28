# Codebase structure

Let's examine the Explainit codebase.
This analysis is accurate as of Explainit 1.0.

```
$ tree -L 1 -d
.
├── docs
├── examples
├── explainit
├───tests
└───workflow
```

## Python SDK

The Python SDK lives in `explainit`.
The majority of Explainit logic lives in these Python files/folders:
* The core Drift objects defined in (`stattest`).
* The core Graph objects defined in (`graphs`).
* The core correlation objects defined in (`correlations`).
* The core data summary objects defined in (`analyzer`).
* The main app functions is defined in `app.py`.
* The `tabs` functions is defined in `tabs.py`.
* The `stat info` functions is defined in `utils.py`.
* The `correlation` functions is defined in `correlation.py`.
* The `workflow` functions for top section is defined in `workflow.py`.
* The `header` functionality for top section is defined in `header.py`.
* The `banner` functions for top section is defined in `banner.py`.

```
$ tree --dirsfirst -L 1 explainit
├───analyzer
├───assets
├───correlations
├───stattests
├───__init__.py
├───app.py
├───banner.py
├───correlation.py
├───dashboard.py
├───header.py
├───tabs.py
├───utils.py
└───workflow.py
```
