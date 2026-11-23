# MedTimer — Project Planning

## Problem and purpose
Keeping track of a daily medicine routine can be difficult. MedTimer is a visual organiser that lets a user save a schedule, record doses, and review consistency over a week.

## Intended user
A student or adult who wants a simple daily checklist. The prototype uses a name-and-age profile and is not designed for sensitive medical records.

## Objectives
1. Build an attractive and clear Streamlit interface.
2. Allow the user to add, edit, archive and delete medicine schedules.
3. Show Taken, Upcoming and Missed statuses using colours.
4. Record completed doses and show encouraging feedback.
5. Calculate a seven-day adherence score.
6. Demonstrate Python Turtle graphics in a companion file.
7. Store records locally using SQLite.

## Inputs, processing and outputs

| Type | Details |
|---|---|
| Inputs | Name, age, medicine name, dose, scheduled time, start date and dose-completion action |
| Processing | Validate inputs, save records in SQLite, compare current time with schedule, calculate weekly percentage |
| Outputs | Personalised greeting, daily checklist, status colours, confirmation, weekly score, tips and Turtle drawing |

## Main algorithm
- Create SQLite tables if they do not exist.
- If no profile exists, show profile setup.
- Read active medicine records.
- For each medicine scheduled today, check whether a dose log exists.
- If logged, show Taken (green); if not logged and scheduled time is later, show Upcoming (yellow); otherwise show Missed (red).
- When Mark taken is selected, save the date and timestamp.
- Calculate adherence: **(doses logged ÷ scheduled doses) × 100**.
- Show a Turtle celebration when weekly adherence reaches 80%.

## Interface plan
Profile setup; Dashboard; My medicines; Weekly progress; Health tips; About.

## Data storage
SQLite stores the profile, medicine schedules and dose logs in `medtimer.db`. On the same computer, records remain after closing and reopening the app as long as this database file is kept.

## Limitations and responsible use
The app has no real alarms, no secure password login and no medical decision-making. It is an educational prototype. Follow qualified healthcare advice and do not use this app as a replacement for official medicine instructions.
