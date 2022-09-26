# Contributing to Explainit

Thank you for considering contributing to Explainit!

## How can you contribute?
We welcome both code and non-code contributions. You can:
* Report a bug
* Improve documentation
* Submit a bug fix
* Propose a new feature or improvement
* Contribute a new feature or improvement
* Test Explainit

## Code contributions
Here is the general workflow:
* Fork the Explainit repository
* Clone the repository
* Make the changes and commit them
* Push the branch to your local fork
* Make sure that all the tests are passing successfully
* Submit a Pull Request with described changes

### Additional information
- Explainit is under active development.
- We are happy to receive a Pull Request for bug fixes or new functions for any section of the app. If you need help or guidance, you can open an Issue first.
- We highly recommend that you open an issue, describe your contribution, share all needed information there and link it to a Pull Request.
- We evaluate Pull Requests taking into account: code architecture and quality, code style, comments & docstrings and coverage by tests.

## 1. Clone repository
```sh
git clone https://github.com/explainit/explainit.git
```

## 2. (Optional, but recommended!) Create virtual environment

#### MacOS / Linux
```sh
cd /path/to/explainit_repo
python3 -m venv venv
. venv/bin/activate
```

#### Windows
```sh
cd C:\path\to\explainit_repo
py -m venv venv
.\venv\Scripts\activate
```

## 3. Use local copy as editable dependency
To use the cloned version in the virtual environment as an app, you need to install the requirements in the editable mode:

#### MacOS / Linux
```sh
cd /path/to/explainit_repo
pip install -e .[dev]
```

#### Windows
```sh
cd C:\path\to\explainit_repo
pip install -e .[dev]
```

## 4. Code-Style--linting

### Conforms to [Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/index.html)
```sh
black explainit
```

### Running flake8
We use flake8 for code style checks.
```sh
flake8 explainit
```

### Running mypy
We use mypy for object types checks.
```sh
# if you are running for the first time, use `mypy --install-types` instead
mypy
```

## 5. Running unit tests
Currently, the project is not fully covered by unit tests, but we are going to add more soon and expect to receive PRs with some unit tests 🙂
```sh
pytest -v
```

## 6. Signing off commits
>  :warning: Warning: using the default integrations with IDEs like VSCode or IntelliJ will not sign commits. When you submit a PR, you'll have to re-sign commits to pass the DCO check.

Use git signoffs to sign your commits. See https://docs.github.com/en/github/authenticating-to-github/managing-commit-signature-verification for details.

Then, you can sign off commits with the `-s` flag:
```sh
git commit -s -m "My first commit"
```

GPG-signing commits with -S is optional.
