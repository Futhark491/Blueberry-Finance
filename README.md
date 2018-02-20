# Blueberry-Finance

SLU Software Engineering Project: An accounting website for managing a budget.

## Team

**Scrum Master:**
> Ben Schwabe

**Front-end & UX Team:**
> Kyle Bagwill,
> Thomas Salvi

**Flask Team:**
> Mark Gerken,
> Ben Schwabe

**Database Team:**
> John Mitton

**Project Guidance:**
> Jacob Sukhodolsky, PhD

## Requirements

- Python 3.3+ (Tested on Python 3.6.4)
- An internet connection (for set up and external webserver hosting)

## Set up

1. Install [Python](https://www.python.org/downloads/)
2. If not installed, install Virtualenv with `pip install virtualenv`
3. Navigate in a terminal window to the root directory of the project and set up a virtual environment with `virtualenv venv`
4. Activate the virtual environment with `venv\Scripts\activate` on a Windows machine or `soruce venv\bin\activate`
	- *More complete directions can be found [here](https://virtualenv.pypa.io/en/stable/userguide/#activate-script)*
5. Install the required Python packages with `pip install -r requirements.txt`

## Usage
1. Configure `main.py` by making sure the `APP_HOST` and `APP_PORT` are the correct host and port to your program
2. Activate the virtual environment (detailed instructions can be found [here](https://virtualenv.pypa.io/en/stable/userguide/#activate-script))
3. Run `python main.py` and wait for the Flask server to announce that it is running on the given IP and port.
4. Access the application by going to the given IP and port on any web browser.
