# MedTimer — Daily Medicine Routine Organiser

**Student:** Siya Gorasiya  
**Programme:** IBCP Year 1  
**Course:** Python Programming  
**CRS:** Artificial Intelligence  
**School:** Udgam School for Children  

Add your candidate registration number to your final submission document.

## Overview
MedTimer is an educational Python application that helps a user organise a daily medicine schedule, record doses they have taken, and review a seven-day adherence score. It uses Streamlit for the interface and SQLite for local data storage.

## Features
- Name-and-age profile setup.
- Add, edit, archive and delete medicine schedules.
- Colour-coded daily checklist: Taken (green), Upcoming (yellow), Missed (red).
- Mark a dose as taken and receive an encouraging message.
- Seven-day adherence score and daily breakdown.
- General health-organisation tips.
- Separate Python Turtle reward drawing.

## Run locally
1. Install Python 3.10 or newer.
2. Open Command Prompt in the extracted folder.
3. Run `python -m pip install -r requirements.txt`.
4. Run `python -m streamlit run app.py`.
5. If the browser does not open, visit `http://localhost:8501`.

The app creates `medtimer.db` beside `app.py`. Keep this file to retain local records.

## Turtle drawing
Run `python turtle_badge.py` in a separate Command Prompt window. It opens a desktop Turtle window. A hosted Streamlit page cannot open a desktop Turtle window in a visitor's browser, so this feature is demonstrated separately.

## GitHub and deployment
Upload `app.py`, `requirements.txt`, `README.md`, `PLANNING.md`, `TESTING_PLAN.md` and `turtle_badge.py` to a GitHub repository. On Streamlit Community Cloud, create a new app, choose the repository and `app.py`, then deploy. Add your live URL and screenshots to your final submission.

## Limitations and safety
This is an educational prototype, not a medical device. The profile screen is not secure password authentication. It does not send alarms or notifications and does not provide medical advice. Do not enter sensitive medical information. The weekly score reflects only the records entered in the app. Local SQLite storage may not persist across cloud redeployments.
Link of the app:https://medtimer-45yo62xojjmutve4hbka7y.streamlit.app/
