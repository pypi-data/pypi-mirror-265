from setuptools import setup, find_packages

setup(
    name="pingexcelutil",
    version="0.0.5",
    author="Vorapol Ping",
    description="Ping's Excel Utility Package",
    packages=find_packages(exclude=["test", "test*", "test-.*", "tests"]),
    install_requires=[
        "pandas >= 2.0.0",
        "xlsxwriter >= 3.0.0",
    ]
)
