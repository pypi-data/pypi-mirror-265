# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='pytest-databases',
    version='0.1.0',
    description='Reusable database fixtures for any and all databases.',
    long_description='# pytest-databases\n\nReusable test fixtures for any and all databases.\n\n<div align="center">\n\n| Project   |     | Status                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |\n| --------- | :-- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |\n| CI/CD     |     | [![Latest Release](https://github.com/jolt-org/pytest-databases/actions/workflows/publish.yaml/badge.svg)](https://github.com/jolt-org/pytest-databases/actions/workflows/publish.yaml) [![Tests And Linting](https://github.com/jolt-org/pytest-databases/actions/workflows/ci.yaml/badge.svg)](https://github.com/jolt-org/pytest-databases/actions/workflows/ci.yaml) [![Documentation Building](https://github.com/jolt-org/pytest-databases/actions/workflows/docs.yaml/badge.svg)](https://github.com/jolt-org/pytest-databases/actions/workflows/docs.yaml)                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |\n| Quality   |     | [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=jolt-org_pytest-databases&metric=coverage)](https://sonarcloud.io/summary/new_code?id=jolt-org_pytest-databases) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=jolt-org_pytest-databases&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=jolt-org_pytest-databases) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=jolt-org_pytest-databases&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=jolt-org_pytest-databases) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=jolt-org_pytest-databases&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=jolt-org_pytest-databases) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=jolt-org_pytest-databases&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=jolt-org_pytest-databases)                            |\n| Community |     | [![Discord](https://img.shields.io/discord/1149784127659319356?labelColor=F50057&color=202020&label=chat%20on%20discord&logo=discord&logoColor=202020)](https://discord.gg/XpFNTjjtTK)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |\n| Meta      |     | [![Jolt Project](https://img.shields.io/badge/Jolt%20Org-%E2%AD%90-F50057.svg?logo=python&labelColor=F50057&color=202020&logoColor=202020)](https://github.com/jolt-org/) [![types - Mypy](https://img.shields.io/badge/types-Mypy-F50057.svg?logo=python&labelColor=F50057&color=202020&logoColor=202020)](https://github.com/python/mypy) [![License - MIT](https://img.shields.io/badge/license-MIT-F50057.svg?logo=python&labelColor=F50057&color=202020&logoColor=202020)](https://spdx.org/licenses/) [![Jolt Sponsors](https://img.shields.io/badge/Sponsor-%E2%9D%A4-%23202020.svg?&logo=github&logoColor=202020&labelColor=F50057)](https://github.com/sponsors/jolt-org) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json&labelColor=F50057)](https://github.com/astral-sh/ruff) [![code style - Black](https://img.shields.io/badge/code%20style-black-000000.svg?logo=python&labelColor=F50057&logoColor=202020)](https://github.com/psf/black) |\n\n</div>\n\n> [!WARNING] > **Pre-Release Alpha Stage**\n>\n> Please note that pytest-databases is currently in a pre-release alpha stage of development. This means the library is still under\n> active development, and its API is subject to change. We encourage developers to experiment with pytest-databases and provide\n> feedback, but we recommend against using it in production environments until a stable release is available.`\n\n## About\n\nThe `pytest-databases` library aims to make testing with a database as simple as possible.\nIt is designed to offer pre-configured testing setups for many different types and versions of databases.\n\n## Features\n\n`pytest-databases` currently utilizes `docker compose` (or the legacy `docker-compose`) commands to manage the startup and shutdown of each database service. The following databases are currently available:\n\n- **Postgres**: Version 12, 13, 14, 15, and 16 are available\n- **MySQL**: Version 5.6, 5.7 and 8 are available\n- **Oracle**: Version 18c XE and 23C Free are available\n- **SQL Server**: Version 2022 is available\n- **Spanner**: The latest cloud-emulator from Google is available\n- **Cockroach**: Version 23.1-latest is available\n\n## Contributing\n\nAll [Jolt][jolt-org] projects will always be a community-centered, available for contributions of any size.\n\nBefore contributing, please review the [contribution guide][contributing].\n\nIf you have any questions, reach out to us on [Discord][discord], our org-wide [GitHub discussions][jolt-discussions] page,\nor the [project-specific GitHub discussions page][project-discussions].\n\n<hr>\n\n<!-- markdownlint-disable -->\n<p align="center">\n  <!-- github-banner-start -->\n  <img src="https://raw.githubusercontent.com/jolt-org/meta/2901c9c5c5895a83fbfa56944c33bca287f88d42/branding/SVG%20-%20Transparent/logo-full-wide.svg" alt="Litestar Logo - Light" width="20%" height="auto" />\n  <br>A <a href="https://github.com/jolt-org">Jolt Organization</a> Project\n  <!-- github-banner-end -->\n</p>\n\n[jolt-org]: https://github.com/jolt-org\n[contributing]: https://docs.pytest-databases.jolt.rs/latest/contribution-guide.html\n[discord]: https://discord.gg/XpFNTjjtTK\n[jolt-discussions]: https://github.com/orgs/jolt-org/discussions\n[project-discussions]: https://github.com/jolt-org/pytest-databases/discussions\n[project-docs]: https://docs.pytest-databases.jolt.rs\n[install-guide]: https://docs.pytest-databases.jolt.rs/latest/#installation\n[newrepo]: https://github.com/organizations/jolt-org/repositories/new?template=pytest-databases\n',
    author_email='Cody Fincher <cody.fincher@gmail.com>',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    install_requires=[
        'pytest',
    ],
    extras_require={
        'cockroachdb': [
            'psycopg',
        ],
        'mssql': [
            'aioodbc',
        ],
        'mysql': [
            'asyncmy>=0.2.9',
        ],
        'oracle': [
            'oracledb',
        ],
        'postgres': [
            'asyncpg>=0.29.0',
        ],
        'spanner': [
            'google-cloud-spanner',
        ],
        'sqlite': [
            'aiosqlite',
        ],
    },
    packages=[
        'pytest_databases',
        'pytest_databases.docker',
    ],
    package_dir={'': 'src'},
)
