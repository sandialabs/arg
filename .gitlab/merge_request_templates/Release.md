## What does this MR do?

This merge request aims to release ARG <version_number>. 

## Related issues

Mention the issue(s) this MR closes or is related to

## Releasing a new version?

- [ ] Make sure below-listed jobs succeeded:
    - [ ] `deploy` stage > `Upload pyARG in Gitlab.com` job
    - [ ] `deploy` stage > `Upload pyARG in pypi.org` job
    - [ ] `documentation` stage > `pages` job
- [ ] Make sure version number has been updated:
    - [ ] `arg.__version__.py` > `__version__ = <version_number>`
    - [ ] `tests/build_tests/crush/expected/build_tests-crush-Report-LaTeX.yml` > `ARG version: <version_number>`
    - [ ] `tests/build_tests/crush-E/expected/build_tests-crush-Report-LaTeX.yml` > `ARG version: <version_number>`
    - [ ] `tests/build_tests/crush-E/expected/build_tests-crush-Report-Word.yml` > `ARG version: <version_number>`
    - [ ] `.gitlab/deployment/pypi/pyARG/setup.py` > `version=<version_number>`
