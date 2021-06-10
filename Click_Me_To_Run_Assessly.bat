rem Create a python virual environment named virtualenv and activate
python -m venv virtualenv
CALL virtualenv\Scripts\activate

rem Install requirements to virtual environment
python -m pip install -r requirements.txt

rem Run the streamlit website
streamlit run main.py