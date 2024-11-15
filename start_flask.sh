#!/bin/bash
cd /home/githubrunner/actions-runner/_work/Maze-Solver/Maze-Solver

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install dependencies
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Start the Flask app
python3 app.py
