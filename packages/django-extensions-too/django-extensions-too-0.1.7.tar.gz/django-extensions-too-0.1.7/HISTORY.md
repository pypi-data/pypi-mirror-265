# History

All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/).

## 0.1.7 (2025-04-03)

- Move to ruff and add tests.

## 0.1.6 (2023-06-21)

- Change to new Python packaging style with `pyproject.toml`.

## 0.1.5 (2022-08-29)

- Ignore `sorl-thumbnail` `cache/` files.

## 0.1.4 (2021-09-03)

- Added `manifest_storage_check` to test manifest storage methods locally.

## 0.1.3 (2021-08-24)

- Fixed `delete_unreferenced_files` and `missing_files` to not assume local file storage backend.

## 0.1.2 (2017-04-03)

- Added a `delete_unreferenced_files` command which deletes all files in MEDIA_ROOT that are not referenced in the database.

## 0.1.1 (2017-04-03)

- Fixed a bug with an outdated permissions method call in `fix_proxy_permissions` command.

## 0.1.0 (2017-03-30)

- First release on PyPI.
