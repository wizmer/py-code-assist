from setuptools import setup, find_packages

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

setup(
    name="ds-cdp",
    version="0.0.1",
    use_scm_version=True,
    url="https://github.com/pepsico/ds-cdp",
    packages=find_packages(exclude=("tests", "notebooks", "DBML")),
    include_package_data=True,
    setup_requires=["setuptools_scm", "pytest-runner"],
    tests_require=["pytest"],
    install_requires=requirements,
    entry_points={"console_scripts": ["ds-cdp=ds_cdp.main:run"]},  # NOQA
    classifiers=["Programming Language :: Python :: 3"],
)
