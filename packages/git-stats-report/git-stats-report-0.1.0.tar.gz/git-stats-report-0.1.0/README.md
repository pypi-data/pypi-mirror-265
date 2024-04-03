# git-report

| PyPI    | [![PyPI Downloads](https://img.shields.io/pypi/dm/git-report?style=for-the-badge&label=Installations&color=steelblue&logo=pypi)](https://pypistats.org/packages/git-report) [![PyPI Version](https://img.shields.io/pypi/v/git-report?style=for-the-badge&logo=pypi)](https://pypi.org/project/git-report/) ![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/elc/git-report/test.yml?style=for-the-badge&logo=githubactions&label=CICD) <br> ![Unreleased Commits](https://img.shields.io/github/commits-difference/elc/git-report?base=develop&head=master&style=for-the-badge&logo=git&label=Unreleased%20Commits) ![Last Released date](https://img.shields.io/github/last-commit/elc/git-report/master?style=for-the-badge&logo=git&label=Last%20Released%20on) 	|
|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| Quality | [![Coveralls branch](https://img.shields.io/coverallsCoverage/github/ELC/git-report?branch=master&style=for-the-badge&logo=coveralls)](https://coveralls.io/github/ELC/git-report) [![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/ELC/git-report?style=for-the-badge&logo=codeclimate)](https://codeclimate.com/github/ELC/git-report) [![Code Climate technical debt](https://img.shields.io/codeclimate/tech-debt/ELC/git-report?style=for-the-badge&logo=codeclimate)](https://codeclimate.com/github/ELC/git-report) <br> ![OSSF-Scorecard Score](https://img.shields.io/ossf-scorecard/github.com/ELC/git-report?style=for-the-badge&label=OpenSSF%20Score) [![Dependabot](https://img.shields.io/badge/Dependabot-Enabled-brightgreen?style=for-the-badge&logo=dependabot)](https://github.com/ELC/git-report/blob/master/.github/dependabot.yml)                                                                                                           	|
| Format  | ![Conventional Commits](https://img.shields.io/badge/semantic--release-conventional-steelblue?logo=semantic-release&style=for-the-badge) ![Commitlint](https://img.shields.io/badge/commitlint-%E2%9C%93-brightgreen?logo=commitlint&style=for-the-badge) <br> ![Pre Commit](https://img.shields.io/badge/Pre--Commit-%E2%9C%93-brightgreen?style=for-the-badge&logo=precommit) ![Format](https://img.shields.io/badge/Format-Ruff-brightgreen?style=for-the-badge&color=black) ![Linting](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fcharliermarsh%2Fruff%2Fmain%2Fassets%2Fbadge%2Fv2.json&style=for-the-badge&label=Linting)                                                                                                                                	|
| Legal   | [![FOSSA Status](https://img.shields.io/badge/LICENSE%20SCAN-PASSING-CD2956?style=for-the-badge&logo=fossa)](https://app.fossa.com/projects/git%2Bgithub.com%2FELC%2Fgit-report) [![PyPI - License](https://img.shields.io/pypi/l/git-report?style=for-the-badge&logo=opensourceinitiative)](./LICENSE) ![Commercial Use](https://img.shields.io/badge/Comercial_Use-%E2%9C%93-brightgreen?style=for-the-badge)                                                                                                                                                                                                                                                                                                                                                                                  	|

💢🔍 breaking change detection in Python - Compatible with Semantic Version and Semantic Release

## Usage

Use the --help flag for detailed options:

```shell
git-report --help
```

git-report can be used in different ways, the most straightforward one is:

```shell
git-report --paths "tests" --target-version "<to-be-release-version>" --test-command "pytest tests"
```

The `test-command` could be any command and does not need to be Python specific

### Combine with scripts

It is also possible to simplify the `test-command` by always using something like `pipenv scripts` or `npm scripts`

So in the `project.json` / `Pipfile`, one could define the test command and use git-report with `npm run test` or `pipenv run test` instead:

```shell
git-report --paths "tests" --target-version "<to-be-release-version>" --test-command "pipenv run test"
```

```shell
git-report --paths "tests" --target-version "<to-be-release-version>" --test-command "npm run test"
```


## Semantic Release

If using the Python-Semantic-Release module, installable with:

```shell
pipx install python-semantic-release
```

One can integrate it with git-report by using:

```shell
git-report -t "$(semantic-release -v version --print)"
```

## Installation


### With Pipx

Recommended instalation for CICD is through `pipx` with a pinned version:

```shell
pip install pipx==1.2.0
pipx run git-report==0.18.0 --paths "tests" --target-version "<to-be-release-version>" --test-command "pytest tests"
```

That command will create a virtual environment just for git-report and run the test command from there.

### With pip

Instalation can be done with pip as usual:

```shell
pip install git-report
```

Pipenv and poetry equivalents can be used as well.

## F.A.Q.

## License

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FELC%2Fgit-report.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FELC%2Fgit-report)
