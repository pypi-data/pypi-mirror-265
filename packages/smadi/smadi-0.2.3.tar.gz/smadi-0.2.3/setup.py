"""
    Setup file for smadi.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.5.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""

from setuptools import setup

if __name__ == "__main__":
    try:
        setup(
            version="0.2.3",
            dependency_links=["https://pypi.org/"],
            install_requires=[
                "pandas",
                "numpy",
                "scipy",
                "xarray",
                "netCDF4",
                "numba",
                "eomaps",
                "statsmodels",
                "scikit-learn",
                "cartopy",
                "matplotlib",
                "dask",
                "flake8",
                "pyflakes",
                "yapf",
                "cadati",
                "pytesmo",
                "ascat",
                "pygeobase",
                "pygeogrids",
                "pynetcf",
                "cmcrameri",
                "fibgrid",
                "datashader",
                "pycountry",
                "PyQt5",
                "PySide2",
                "autopep8",
            ],
        )

    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
