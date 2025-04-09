from setuptools import setup, find_packages

setup(
    name="rockpaperscissors-bot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "python-telegram-bot[job-queue]>=20.7",
        "apscheduler>=3.10.4",
        "pytz>=2023.3",
        "tzlocal>=5.0.1",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.7",
)