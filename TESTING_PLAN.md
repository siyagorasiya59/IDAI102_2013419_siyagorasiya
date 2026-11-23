# MedTimer — Testing Plan and Evidence

Run every test yourself and complete the final two columns. Do not mark a test as passed until you have tried it.

| No. | Test | Action | Expected result | Actual result | Status |
|---:|---|---|---|---|---|
| 1 | Empty profile | Submit without a name | Validation message appears | To test | To test |
| 2 | Profile | Enter name and age | Personalised dashboard opens | To test | To test |
| 3 | Add medicine | Enter name, dose, time and start date | Medicine is saved | To test | To test |
| 4 | Required fields | Leave name or dose blank | Error message appears | To test | To test |
| 5 | Edit medicine | Change medicine details | Updated details are saved | To test | To test |
| 6 | Archive | Archive a medicine | It disappears from active checklist | To test | To test |
| 7 | Delete | Confirm deletion | Medicine and dose history are removed | To test | To test |
| 8 | Upcoming | Add a future scheduled time | Yellow Upcoming status appears | To test | To test |
| 9 | Missed | Leave a past scheduled time unlogged | Red Missed status appears | To test | To test |
| 10 | Taken | Select Mark taken | Green Taken status and encouragement appear | To test | To test |
| 11 | Weekly score | Log doses and open Weekly progress | Percentage matches logged/scheduled × 100 | To test | To test |
| 12 | Persistence | Close and reopen app, keeping `medtimer.db` | Profile, medicines and logs remain | To test | To test |
| 13 | Turtle | Run `python turtle_badge.py` | Turtle drawing window appears | To test | To test |

## Screenshots to collect
- [ ] Profile setup
- [ ] Dashboard and status colours
- [ ] Add/edit medicine page
- [ ] Weekly progress
- [ ] Health tips
- [ ] Turtle drawing window
- [ ] GitHub repository
- [ ] Deployed Streamlit app

The table is a test plan, not evidence of completed testing. Enter your real observations after running the app.
