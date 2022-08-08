# Employee_Monitoring_Testbed
The basic project setup for Employee Monitoring Testbed is as follows:


# Setting up a database
This project mainly uses PostgreSQL. To connect this backend with your local database add a .env file in the root directory.
The structure of the .env file will be as follows:

SECRET_KEY=
NAME=
USER=
PASSWORD=
HOST=localhost
PORT=5432

None of this needs to be enclosed in commas or speech marks. Also note that HOST and PORT may also need to be changed according to your contextual requirements.


# Setting up environment
You need to set up a python virtual environment in your root directory using any venv of your choice.
I prefer using: "virtualenv venv" if you have virtualenv installed first.

After venv has set up, activate it and run:
pip install -r requirements.txt

It will install all the required libraries and dependencies for your django project.


# Installing new libraries and dependencies
If you have install a new library using pip or any other installer package. Make sure to add it in requirements.txt
please don't use pip freeze as it will add the versions too, and this can cause conflicts in the future releases.
