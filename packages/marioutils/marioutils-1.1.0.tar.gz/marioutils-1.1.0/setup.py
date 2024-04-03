from setuptools import find_packages, setup

with open("mario_utils/README.md", 'r') as f:
    long_description = f.read()

setup(
    name="marioutils",
    version="1.1.0",
    description="Utils library for DB connection and logging",
    packages=find_packages(),
    package_data={'mario_utils': ['databasemanagement/*', 'logger/*', '*']},
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarioHdzCtu/MarioUtils",
    author="Mario Hernandez",
    author_email="mariohertu@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "pymssql >= 2.2.11",
        "sqlalchemy >= 2.0.25",
        "mariadb >= 1.1.10"],
    extras_require={
        "dev": ["pytest>=8.0.0"]
    },
    python_requires=">=3.10.12",
    include_dirs=True
)
