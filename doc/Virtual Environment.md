# Virtual Environment

## Documentation

Please note that most of the documentation can be found [here](https://virtualenv.pypa.io/en/stable/).

## Install & Setup

1. After installing Python, confirm that you have the correct python installed to the path with `python --version` (should be python 3.6.4)
2. Open a terminal and run `pip install virtualenv`
3. `cd` to the directory you wish to create the virtual environment
4. Create a Virtual Environment in the local directory with `virtualenv venv`
5. Start the Virtual Environment by following the instructions found [here](https://virtualenv.pypa.io/en/stable/userguide/#activate-script).
6. Install previous environments by running `pip install -r requirements.txt` in the same directory that the `requirements.txt` file is located.

## Installing Packages

1. Start the Virtual Environment by following the instructions found [here](https://virtualenv.pypa.io/en/stable/userguide/#activate-script).
2. Install a new package by running `pip install <package_name>`
3. Once the package is installed, update the requirements by running `pip freeze > requirements.txt`