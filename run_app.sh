#!/bin/bash
echo "Creating virtual environment..."
python3.12 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

echo "Starting the app..."
streamlit run app.py
