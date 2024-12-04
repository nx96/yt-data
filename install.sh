#!/bin/bash

######## Create a virtual environment
python -m venv yt_env
echo "Virtual environment created."

######## Activate the virtual environment
echo "Activating virtual environment..."
source yt_env/Scripts/activate
echo "Virtual environment activated."

######## Install the required packages
pip install -r requirements.txt
echo "Packages installed."