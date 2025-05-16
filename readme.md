Programmer 101: CodeVeda 🚀
Welcome to Programmer 101: CodeVeda, the ultimate productivity sidekick for coders! This slick Streamlit app, rocking a black-and-neon-green vibe, is your go-to for crushing daily programming chaos. Manage tasks, track coding sprints, hack away in an in-app code editor, and even get cosmic task tips inspired by Vedic astrology. Built for coders by coders, it’s your ticket to staying focused, organized, and in the zone. 🌌💾
✨ Features That’ll Make You Code Like a Pro

Task Manager: Add, edit, and filter tasks with priorities and deadlines. Say goodbye to missed deadlines and hello to ninja-level organization.
Time Tracker: Log coding sessions with notes and visualize your productivity with dope Plotly charts (pie for task split, line for daily grind).
Code Editor: Hack Python scripts right in the app with a monokai-themed editor. Run code on the fly and debug like a boss.
Pomodoro Timer: Smash focus with 25-minute coding sprints. Perfect for battling procrastination.
API Key Manager: Store API keys securely for your favorite tools (GitHub, AI APIs, you name it).
Vedic Astrology Insights: Get task suggestions based on your birth chart (e.g., Sun in Gemini for coding mornings). Cosmic productivity, anyone? 🪐
Black & Neon Green UI: A coder’s dream aesthetic, inspired by late-night coding sessions under neon lights.
Local SQLite Database: Securely stores your tasks, time logs, and credentials. No more lost data.

🛠️ Setup: Get Coding in Minutes
Prerequisites

Python 3.8+ (check with python --version)
Git (for cloning the repo)
A passion for coding and neon vibes 😎

Installation

Clone the Repo:
git clone https://github.com/your-username/codeveda.git
cd codeveda


Install Dependencies:Save the following as requirements.txt:
streamlit==1.38.0
pandas==2.2.2
plotly==5.22.0
streamlit-ace==0.1.1
streamlit-pydantic-form==0.2.0

Then run:
pip install -r requirements.txt


Run the App:
streamlit run app.py

Open http://localhost:8501 in your browser and feel the neon glow!


🚀 Usage: Hack Your Productivity

Register/Login: Sign up with a username and password, or log in to access your dashboard.
Add Tasks: Drop tasks with priorities (Low, Medium, High), statuses (To Do, In Progress, Done), and deadlines.
Track Time: Log coding sessions with notes to keep tabs on your grind.
View Productivity: Check out pie charts for task time splits and line charts for daily coding trends.
Code Editor: Write and run Python scripts in a slick monokai-themed editor.
Pomodoro Timer: Start a 25-minute focus session to code like a machine.
API Keys: Save API keys for your dev tools securely.
Astrology Insights: Get cosmic task tips (e.g., code during Sun hours for max focus).

🌌 Vedic Astrology Bonus
Inspired by your birth chart (Sun in Gemini, Moon in Leo), CodeVeda suggests when to tackle coding, creative tasks, or meetings based on planetary vibes. Want more? Ping us to integrate real-time transit APIs!
📦 Deploy to Production
Streamlit Cloud

Push your repo to GitHub with app.py and requirements.txt.
Sign into Streamlit Cloud, link your repo, and select app.py as the main file.
Deploy and monitor logs for any hiccups.
Note: SQLite works locally but may need a hosted DB (e.g., PostgreSQL) for cloud scalability.

Local Deployment
Run locally with:
streamlit run app.py --server.port 8501

For production, use a WSGI server like Gunicorn:
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app

🐛 Troubleshooting

Blank Pages?
Check app.log for errors.
Ensure dependencies are installed (pip install -r requirements.txt).
Verify Python 3.8+ and SQLite access.
Run a minimal Streamlit app to test:import streamlit as st
st.write("Test Vibe")


Clear browser cache or try Chrome/Firefox.


Database Issues?
Ensure coder_dashboard.db has write permissions (chmod -R u+w .).
Delete and restart to recreate the database.


Still Stuck? Open an issue on GitHub or hit up the community!

🛠️ Future Hacks

GitHub Sync: Link tasks with GitHub Issues or PRs.
Notifications: Email/SMS deadline reminders via Twilio.
Astro API: Real-time Vedic astrology for dynamic task planning.
Export Reports: Download tasks/time logs as CSV or PDF.

🤝 Contributing
Got a killer feature idea? Fork the repo, hack away, and submit a PR. Let’s make CodeVeda the ultimate coder’s companion!
📜 License
MIT License. Code free, vibe hard.
💬 Contact
Drop a line at your-email@example.com or join the coder tribe on X for neon-fueled updates!
Programmer 101: CodeVeda – Code smart, vibe cosmic. 🌌💻
