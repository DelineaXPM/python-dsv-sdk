# Release

- Run [changie-trigger-release](https://github.com/DelineaXPM/python-dsv-sdk/actions/workflows/changie-trigger-release.yml).
- Make sure `python-dsv-sdk/delinea/__init__.py` was included in the pull request.
- Once changie files are merged, the [release](https://github.com/DelineaXPM/python-dsv-sdk/actions/workflows/release.yml) should trigger and publish.
  - pypi should be updated: [pypi link](https://pypi.org/project/python-dsv-sdk/)
  - [github release should also have been created](https://github.com/DelineaXPM/python-dsv-sdk/releases) (this is just for more consistent releases and also triggering update in slack channels via release).
