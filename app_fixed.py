import streamlit as st
import sqlite3
from pathlib import Path
from datetime import date, datetime, time, timedelta
import html

DB = Path(__file__).with_name("medtimer.db")
st.set_page_config(page_title="MedTimer", page_icon="⏰", layout="wide")

def db():
    c = sqlite3.connect(DB, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c

def setup():
    with db() as c:
        c.execute("CREATE TABLE IF NOT EXISTS profile(id INTEGER PRIMARY KEY CHECK(id=1), name TEXT, age INTEGER)")
        c.execute("""CREATE TABLE IF NOT EXISTS meds(
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, dose TEXT NOT NULL,
            at TEXT NOT NULL, start TEXT NOT NULL, active INTEGER DEFAULT 1)""")
        c.execute("""CREATE TABLE IF NOT EXISTS logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT, med_id INTEGER, day TEXT, taken_at TEXT,
            UNIQUE(med_id, day))""")
        c.commit()

def profile():
    with db() as c:
        return c.execute("SELECT * FROM profile WHERE id=1").fetchone()

def meds(active=True):
    with db() as c:
        q = "SELECT * FROM meds"
        if active: q += " WHERE active=1"
        return c.execute(q + " ORDER BY at").fetchall()

def taken(mid, day):
    with db() as c:
        return c.execute("SELECT 1 FROM logs WHERE med_id=? AND day=?", (mid, day.isoformat())).fetchone() is not None

def log_dose(mid, day):
    with db() as c:
        c.execute("INSERT OR IGNORE INTO logs(med_id,day,taken_at) VALUES(?,?,?)",
                  (mid, day.isoformat(), datetime.now().isoformat(timespec="seconds")))
        c.commit()

def weekly(active_meds, today):
    start = today - timedelta(days=6)
    with db() as c:
        rows = c.execute("SELECT med_id,day FROM logs WHERE day BETWEEN ? AND ?",
                         (start.isoformat(), today.isoformat())).fetchall()
    done = {(r["med_id"], r["day"]) for r in rows}
    total = count = 0
    for m in active_meds:
        first = max(start, date.fromisoformat(m["start"]))
        if first <= today:
            for n in range((today-first).days + 1):
                d = first + timedelta(days=n)
                total += 1
                count += (m["id"], d.isoformat()) in done
    return (round(count*100/total) if total else 0), count, total

setup()
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:linear-gradient(130deg,#f3f7ff,#f4fbf7,#fff8f0)}
.block-container{max-width:1150px;padding-top:1.5rem}
.hero{background:linear-gradient(115deg,#243b67,#426c91,#5b9a91);padding:28px;border-radius:22px;color:white;margin-bottom:18px}
.hero h1{color:white;margin:0}.hero p{color:#edf5fa;margin:5px 0 0}
.card{background:white;border:1px solid #e6edf4;border-radius:16px;padding:17px;margin-bottom:12px;box-shadow:0 6px 20px #1d35570b}
.metric{background:white;border:1px solid #e6edf4;border-radius:16px;padding:16px}
.label{font-size:.8rem;color:#718096;font-weight:700;text-transform:uppercase}
.value{font-size:1.8rem;color:#1d2d48;font-weight:800}
.badge{display:inline-block;border-radius:30px;padding:5px 11px;font-weight:800;font-size:.8rem}
.green{background:#d9f5e6;color:#167447}.yellow{background:#fff1c9;color:#956500}.red{background:#ffe0df;color:#a52b2b}
.tip{background:#fff6e5;border-left:5px solid #efb64a;border-radius:10px;padding:13px;color:#654b19}

/* Readability fixes: dark text on the light main-page background. */
:root{color-scheme:light}
.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{color:#243047 !important}
[data-testid="stMain"] p,
[data-testid="stMain"] li,
[data-testid="stMain"] label,
[data-testid="stMain"] small,
[data-testid="stMain"] .stMarkdown,
[data-testid="stMain"] .stMarkdown p,
[data-testid="stMain"] [data-testid="stCaptionContainer"],
[data-testid="stMain"] [data-testid="stWidgetLabel"],
[data-testid="stMain"] [data-testid="stExpander"] summary,
[data-testid="stMain"] [data-testid="stExpander"] summary p{color:#243047 !important}
[data-testid="stMain"] input,
[data-testid="stMain"] textarea,
[data-testid="stMain"] [data-baseweb="select"] *,
[data-testid="stMain"] [data-baseweb="input"] input{color:#243047 !important}
[data-testid="stMain"] input,
[data-testid="stMain"] textarea,
[data-testid="stMain"] [data-baseweb="select"] > div{background-color:#ffffff !important}
[data-testid="stMain"] button{color:#243047}
[data-testid="stMain"] .hero,
[data-testid="stMain"] .hero h1,
[data-testid="stMain"] .hero p{color:#ffffff !important}
[data-testid="stMain"] .metric .label{color:#64748b !important}
[data-testid="stMain"] .metric .value{color:#1d2d48 !important}
[data-testid="stMain"] .badge.green{color:#167447 !important}
[data-testid="stMain"] .badge.yellow{color:#956500 !important}
[data-testid="stMain"] .badge.red{color:#a52b2b !important}
[data-testid="stMain"] .tip{color:#654b19 !important}
</style>""", unsafe_allow_html=True)

p = profile()
today = date.today()
if not p:
    st.markdown('<div class="hero"><h1>⏰ Welcome to MedTimer</h1><p>Your simple daily medicine routine organiser.</p></div>', unsafe_allow_html=True)
    st.subheader("Create your profile")
    with st.form("profile"):
        n = st.text_input("What should we call you?")
        a = st.number_input("Your age", 1, 110, 16)
        ok = st.form_submit_button("Create my profile ✨", use_container_width=True)
    if ok:
        if not n.strip(): st.error("Please enter your name.")
        else:
            with db() as c:
                c.execute("INSERT OR REPLACE INTO profile(id,name,age) VALUES(1,?,?)",(n.strip(),a))
                c.commit()
            st.rerun()
    st.info("Educational prototype only. This profile screen is not secure password-based authentication. Do not enter sensitive medical information.")
    st.stop()

name = p["name"]
active = meds()
with st.sidebar:
    st.title("⏰ MedTimer")
    st.caption(f"Hello, {name}! · Age {p['age']}")
    page = st.radio("Navigate",["Dashboard","My medicines","Weekly progress","Health tips","About"])
    st.caption("Your daily health companion")

if page == "Dashboard":
    st.markdown(f'<div class="hero"><h1>Good day, {html.escape(name)}! 🌿</h1><p>Small steps, taken consistently, make a meaningful difference.</p></div>',unsafe_allow_html=True)
    score, done, total = weekly(active,today)
    taken_today = sum(taken(m["id"],today) for m in active)
    upcoming = missed = 0
    for m in active:
        if not taken(m["id"],today):
            if datetime.strptime(m["at"],"%H:%M").time() < datetime.now().time(): missed += 1
            else: upcoming += 1
    cols=st.columns(4)
    for col,label,val in zip(cols,["Today's doses","Upcoming","Missed","Weekly score"],[f"{taken_today}/{len(active)}",upcoming,missed,f"{score}%"]):
        col.markdown(f'<div class="metric"><div class="label">{label}</div><div class="value">{val}</div></div>',unsafe_allow_html=True)
    st.subheader("Today's checklist")
    if not active: st.info("No medicines yet. Open My medicines to add your first schedule.")
    for m in active:
        is_done=taken(m["id"],today)
        passed=datetime.strptime(m["at"],"%H:%M").time() < datetime.now().time()
        status,cls=("Taken","green") if is_done else (("Missed","red") if passed else ("Upcoming","yellow"))
        a,b,c=st.columns([4,1,1.4])
        a.markdown(f'<div class="card"><b>💊 {html.escape(m["name"])}</b><br><small>{html.escape(m["dose"])} · {m["at"]}</small></div>',unsafe_allow_html=True)
        b.markdown(f'<div style="padding-top:18px"><span class="badge {cls}">{status}</span></div>',unsafe_allow_html=True)
        if is_done: c.caption("Logged ✓")
        elif c.button("Mark taken",key=f"take{m['id']}"):
            log_dose(m["id"],today)
            st.session_state["encourage"]=m["name"]
            st.balloons()
            st.rerun()
    if st.session_state.pop("encourage",None):
        st.success(f"Well done, {name}! You logged your dose. One positive step at a time! 🌟")
    st.markdown('<div class="tip">💡 MedTimer records your routine; it does not send alarms or replace advice from a doctor or pharmacist.</div>',unsafe_allow_html=True)

elif page == "My medicines":
    st.markdown('<div class="hero"><h1>💊 My medicines</h1><p>Add, update, archive or delete your daily schedule.</p></div>',unsafe_allow_html=True)
    with st.expander("＋ Add a medicine",expanded=not bool(active)):
        with st.form("add"):
            n=st.text_input("Medicine name")
            d=st.text_input("Dose / instructions",placeholder="e.g. 1 tablet")
            t=st.time_input("Daily scheduled time",time(9,0))
            s=st.date_input("Start date",today)
            ok=st.form_submit_button("Add medicine")
        if ok:
            if not n.strip() or not d.strip(): st.error("Enter both the medicine name and dose.")
            else:
                with db() as c:
                    c.execute("INSERT INTO meds(name,dose,at,start) VALUES(?,?,?,?)",(n.strip(),d.strip(),t.strftime("%H:%M"),s.isoformat()))
                    c.commit()
                st.success("Medicine added.")
                st.rerun()
    for m in meds(False):
        with st.expander(f"{m['name']} · {m['dose']} · {m['at']}"+("" if m["active"] else " · Archived")):
            if m["active"]:
                with st.form(f"edit{m['id']}"):
                    n=st.text_input("Name",m["name"])
                    d=st.text_input("Dose",m["dose"])
                    t=st.time_input("Time",datetime.strptime(m["at"],"%H:%M").time())
                    s=st.date_input("Start date",date.fromisoformat(m["start"]))
                    save=st.form_submit_button("Save changes")
                if save:
                    if n.strip() and d.strip():
                        with db() as c:
                            c.execute("UPDATE meds SET name=?,dose=?,at=?,start=? WHERE id=?",(n.strip(),d.strip(),t.strftime("%H:%M"),s.isoformat(),m["id"]))
                            c.commit()
                        st.rerun()
                    else: st.error("Name and dose are required.")
                x,y=st.columns(2)
                if x.button("Archive",key=f"arc{m['id']}"):
                    with db() as c: c.execute("UPDATE meds SET active=0 WHERE id=?",(m["id"],)); c.commit()
                    st.rerun()
                if y.button("Delete permanently",key=f"del{m['id']}"):
                    st.session_state[f"confirm{m['id']}"]=True
                if st.session_state.get(f"confirm{m['id']}"):
                    st.warning("This also removes the medicine's dose history.")
                    if st.button("Confirm delete",key=f"yes{m['id']}"):
                        with db() as c:
                            c.execute("DELETE FROM logs WHERE med_id=?",(m["id"],))
                            c.execute("DELETE FROM meds WHERE id=?",(m["id"],))
                            c.commit()
                        st.rerun()

elif page == "Weekly progress":
    st.markdown('<div class="hero"><h1>📈 Weekly progress</h1><p>Your last seven days at a glance.</p></div>',unsafe_allow_html=True)
    score,done,total=weekly(active,today)
    a,b,c=st.columns(3)
    a.metric("Adherence score",f"{score}%"); b.metric("Doses logged",done); c.metric("Scheduled doses",total)
    st.progress(score/100 if total else 0)
    if not total: st.info("Add a medicine and start logging doses to see your score.")
    for offset in range(6,-1,-1):
        day=today-timedelta(days=offset); due=got=0
        for m in active:
            if date.fromisoformat(m["start"])<=day:
                due+=1; got+=taken(m["id"],day)
        st.write(f"**{day.strftime('%a, %d %b')}** — {got}/{due} doses logged")
        st.progress(got/due if due else 0)

elif page == "Health tips":
    st.markdown('<div class="hero"><h1>🌱 Little health reminders</h1><p>Build a routine that feels manageable.</p></div>',unsafe_allow_html=True)
    for title,body in [
        ("Create a routine","Link your schedule to a regular daily activity if that matches the instructions you were given."),
        ("Use a checklist","Mark a dose only after you have taken it."),
        ("Read the label","Follow directions from your doctor or pharmacist. Do not change a dose based on an app suggestion."),
        ("Plan ahead","Contact your pharmacy or healthcare professional before you run out of a prescribed medicine."),
        ("Ask when unsure","If you miss a dose, check the official instructions or ask a qualified healthcare professional. Do not double a dose unless instructed.")
    ]:
        st.markdown(f'<div class="card"><b>✨ {title}</b><br>{body}</div>',unsafe_allow_html=True)
    st.caption("General organisation tips only; not medical advice.")

else:
    st.markdown('<div class="hero"><h1>About MedTimer</h1><p>A Python and Streamlit project for the Year 1 Python Programming assessment.</p></div>',unsafe_allow_html=True)
    st.markdown("""
**Purpose:** Organise a daily medicine schedule, record completed doses and review a seven-day score.

**Technology:** Python, Streamlit and SQLite.

**Turtle reward:** Run `python turtle_badge.py` in a separate Command Prompt window to see the Python Turtle reward drawing. Desktop Turtle windows cannot open inside a hosted Streamlit page.

**Limitations:** The profile screen is not secure authentication. The app does not send real alarms or notifications, and it does not provide medical advice. The weekly score reflects only entries recorded in this app. SQLite local files may not persist across cloud redeployments. This is an educational prototype, not a medical device.
""")
    score,done,total=weekly(active,today)
    if total and score>=80:
        st.success("Your weekly score is 80% or higher — great consistency! 🐢")
        st.balloons()
    else: st.info("The Turtle celebration unlocks when your weekly score reaches 80%.")
st.markdown("---")
st.caption("MedTimer · IBCP Year 1 · Python Programming · Educational prototype")
