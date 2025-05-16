import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, timedelta
import logging
import hashlib
import streamlit_ace as ace
from pydantic import BaseModel, Field, ValidationError
from io import StringIO
from contextlib import redirect_stdout

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
st.set_page_config(layout="wide")
# SQLite database setup
def init_db():
    try:
        conn = sqlite3.connect('coder_dashboard.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                     username TEXT PRIMARY KEY, 
                     password TEXT NOT NULL,
                     api_key TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT,
                     task TEXT,
                     priority TEXT,
                     status TEXT,
                     deadline TEXT,
                     FOREIGN KEY (username) REFERENCES users (username))''')
        c.execute('''CREATE TABLE IF NOT EXISTS time_logs (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT,
                     date TEXT,
                     task TEXT,
                     duration INTEGER,
                     notes TEXT,
                     FOREIGN KEY (username) REFERENCES users (username))''')
        conn.commit()
        conn.close()
        logging.info("Database initialized successfully")
    except Exception as e:
        logging.error(f"Database initialization failed: {e}")
        st.error(f"Database error: {e}")

init_db()

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Custom CSS with Tailwind-inspired styles
def set_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
        body, .stApp {
            background-color: #000;
            color: #39FF14;
            font-family: 'Fira Code', monospace;
        }
        .stButton>button {
            background-color: #39FF14;
            color: #000;
            border: 2px solid #39FF14;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #2ECC71;
            transform: scale(1.05);
        }
        .stTextInput>div>input, .stSelectbox>div>select, .stDateInput>div>input, .stTextArea>textarea {
            background-color: #2A2F33;
            color: #39FF14;
            border: 1px solid #39FF14;
            border-radius: 8px;
            padding: 8px;
        }
        .stDataFrame, .stPlotlyChart {
            background-color: #2A2F33;
            border: 1px solid #39FF14;
            border-radius: 8px;
            padding: 15px;
        }
        h1, h2, h3 {
            color: #39FF14;
            padding-bottom: 8px;
            margin-bottom: 15px;
        }
        .stMarkdown, .stMarkdown p {
            color: #39FF14;
        }
        .stExpander {
            background-color: #2A2F33;
            border: 1px solid #39FF14;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        .stContainer {
            background-color: #2A2F33;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            background-color: #2A2F33;
            border-radius: 8px;
            margin-bottom: 20px;
            background:transparent;
        }
        .tooltip {
            font-size: 0.9em;
            color: #2ECC71;
            margin-top: 5px;
        }
                .st-key-logout_button{
                    align-self: flex-end;
                    display: flex;
                }
        </style>
    """, unsafe_allow_html=True)

# Pydantic models for validation
class TaskForm(BaseModel):
    task_name: str = Field(..., min_length=1, max_length=100)
    priority: str = Field(..., pattern="^(Low|Medium|High)$")
    status: str = Field(..., pattern="^(To Do|In Progress|Done)$")
    deadline: str

class TimeLogForm(BaseModel):
    task: str = Field(..., min_length=1)
    duration: int = Field(..., ge=1)
    notes: str = Field(default="", max_length=500)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.pomodoro_running = False
    st.session_state.pomodoro_time = 25 * 60
    st.session_state.code_output = ""

# Database functions
def load_tasks(username):
    with st.spinner("Loading tasks..."):
        try:
            conn = sqlite3.connect('coder_dashboard.db')
            df = pd.read_sql_query("SELECT * FROM tasks WHERE username = ?", conn, params=(username,))
            conn.close()
            return df
        except Exception as e:
            logging.error(f"Error loading tasks for {username}: {e}")
            st.error(f"Failed to load tasks: {e}")
            return pd.DataFrame(columns=["id", "username", "task", "priority", "status", "deadline"])

def save_task(username, task_data):
    with st.spinner("Saving task..."):
        try:
            conn = sqlite3.connect('coder_dashboard.db')
            c = conn.cursor()
            c.execute("INSERT INTO tasks (username, task, priority, status, deadline) VALUES (?, ?, ?, ?, ?)",
                      (username, task_data.task_name, task_data.priority, task_data.status, task_data.deadline))
            conn.commit()
            conn.close()
            logging.info(f"Task saved for {username}: {task_data.task_name}")
        except Exception as e:
            logging.error(f"Error saving task: {e}")
            st.error(f"Failed to save task: {e}")

def update_task(task_id, task_data):
    with st.spinner("Updating task..."):
        try:
            conn = sqlite3.connect('coder_dashboard.db')
            c = conn.cursor()
            c.execute("UPDATE tasks SET task = ?, priority = ?, status = ?, deadline = ? WHERE id = ?",
                      (task_data.task_name, task_data.priority, task_data.status, task_data.deadline, task_id))
            conn.commit()
            conn.close()
            logging.info(f"Task {task_id} updated")
        except Exception as e:
            logging.error(f"Error updating task {task_id}: {e}")
            st.error(f"Failed to update task: {e}")

def load_time_logs(username):
    with st.spinner("Loading time logs..."):
        try:
            conn = sqlite3.connect('coder_dashboard.db')
            df = pd.read_sql_query("SELECT * FROM time_logs WHERE username = ?", conn, params=(username,))
            conn.close()
            return df
        except Exception as e:
            logging.error(f"Error loading time logs for {username}: {e}")
            st.error(f"Failed to load time logs: {e}")
            return pd.DataFrame(columns=["id", "username", "date", "task", "duration", "notes"])

def save_time_log(username, log_data):
    with st.spinner("Saving time log..."):
        try:
            conn = sqlite3.connect('coder_dashboard.db')
            c = conn.cursor()
            c.execute("INSERT INTO time_logs (username, date, task, duration, notes) VALUES (?, ?, ?, ?, ?)",
                      (username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), log_data.task, log_data.duration, log_data.notes))
            conn.commit()
            conn.close()
            logging.info(f"Time log saved for {username}: {log_data.task}")
        except Exception as e:
            logging.error(f"Error saving time log: {e}")
            st.error(f"Failed to save time log: {e}")

def register_user(username, password):
    with st.spinner("Registering user..."):
        try:
            conn = sqlite3.connect('coder_dashboard.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                      (username, hash_password(password)))
            conn.commit()
            conn.close()
            logging.info(f"User registered: {username}")
            return True
        except sqlite3.IntegrityError:
            logging.warning(f"Username already exists: {username}")
            return False
        except Exception as e:
            logging.error(f"Error registering user: {e}")
            st.error(f"Registration failed: {e}")
            return False

def login_user(username, password):
    with st.spinner("Logging in..."):
        try:
            conn = sqlite3.connect('coder_dashboard.db')
            c = conn.cursor()
            c.execute("SELECT password FROM users WHERE username = ?", (username,))
            result = c.fetchone()
            conn.close()
            if result and result[0] == hash_password(password):
                logging.info(f"User logged in: {username}")
                return True
            logging.warning(f"Login failed for {username}")
            return False
        except Exception as e:
            logging.error(f"Error during login: {e}")
            st.error(f"Login error: {e}")
            return False

def save_api_key(username, api_key):
    with st.spinner("Saving API key..."):
        try:
            conn = sqlite3.connect('coder_dashboard.db')
            c = conn.cursor()
            c.execute("UPDATE users SET api_key = ? WHERE username = ?", (api_key, username))
            conn.commit()
            conn.close()
            logging.info(f"API key saved for {username}")
        except Exception as e:
            logging.error(f"Error saving API key: {e}")
            st.error(f"Failed to save API key: {e}")

def pomodoro_timer():
    if st.session_state.pomodoro_running:
        if st.session_state.pomodoro_time > 0:
            st.session_state.pomodoro_time -= 1
            st.markdown(f"**Pomodoro Timer**: {st.session_state.pomodoro_time // 60}:{st.session_state.pomodoro_time % 60:02d}")
            st.rerun()
        else:
            st.session_state.pomodoro_running = False
            st.success("Pomodoro session complete! Take a break.")
    else:
        if st.button("Start 25-Min Pomodoro"):
            st.session_state.pomodoro_running = True
            st.session_state.pomodoro_time = 25 * 60
            st.rerun()

def auth_page():
    set_custom_css()
    st.title("Programmer 101")
    st.markdown("Welcome to your coder's command center. Log in or register to start crushing it! 🚀", unsafe_allow_html=True)
    col1, col2 = st.tabs(["Login", "Register"])
    
    with col1:
        st.subheader("Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            st.markdown("<p class='tooltip'>Enter your credentials to access the dashboard.</p>", unsafe_allow_html=True)
            if st.form_submit_button("Login"):
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Welcome, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
    
    with col2:
        st.subheader("Register")
        with st.form("register_form"):
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            st.markdown("<p class='tooltip'>Choose a unique username and secure password.</p>", unsafe_allow_html=True)
            if st.form_submit_button("Register"):
                if register_user(new_username, new_password):
                    st.success("Registration successful! Please log in.")
                else:
                    st.error("Username already exists or registration failed.")

def dashboard_page():
    set_custom_css()
    

    # Header Section
    hcol1,hcol2,hcol3,hcol4=st.columns([1.5,2,0.5,0.3])
    hcol1.title("Programmer101 Dashboard")
    hcol3.markdown(f"""
            <div class='header'>
                <div>
                    <span style='color: #39FF14; font-weight: bold;align-self: flex-end;display: flex;'>Welcome, {st.session_state.username}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with hcol4:
        if st.button("Logout", key="logout_button", help="Click to log out and return to login page"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()


    pomodoro_timer()

    tasks_df = load_tasks(st.session_state.username)
    time_logs_df = load_time_logs(st.session_state.username)

    # Middle Section: Tasks/Time Tracking (Left) and Productivity (Right)
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        # Task Management
        with st.container():
            st.subheader("Tasks")
            with st.form("task_form"):
                task_name = st.text_input("Task Name", placeholder="Enter task name")
                priority = st.selectbox("Priority", ["Low", "Medium", "High"])
                status = st.selectbox("Status", ["To Do", "In Progress", "Done"])
                deadline = st.date_input("Deadline", min_value=datetime.today())
                st.markdown("<p class='tooltip'>Add tasks to stay organized.</p>", unsafe_allow_html=True)
                if st.form_submit_button("Add Task"):
                    try:
                        task_data = TaskForm(
                            task_name=task_name,
                            priority=priority,
                            status=status,
                            deadline=deadline.strftime("%Y-%m-%d")
                        )
                        save_task(st.session_state.username, task_data)
                        st.success("Task added successfully!")
                        st.rerun()
                    except ValidationError as e:
                        st.error(f"Invalid input: {e}")

            if not tasks_df.empty:
                status_filter = st.selectbox("Filter Tasks", ["All", "To Do", "In Progress", "Done"])
                filtered_tasks = tasks_df if status_filter == "All" else tasks_df[tasks_df["status"] == status_filter]
                st.dataframe(filtered_tasks[["task", "priority", "status", "deadline"]], use_container_width=True, height=200)
                
                with st.expander("Edit Task"):
                    task_to_edit = st.selectbox("Select Task to Edit", filtered_tasks["task"])
                    if task_to_edit:
                        task_data = tasks_df[tasks_df["task"] == task_to_edit].iloc[0]
                        with st.form("edit_task_form"):
                            new_task_name = st.text_input("Task Name", task_data["task"])
                            new_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(task_data["priority"]))
                            new_status = st.selectbox("Status", ["To Do", "In Progress", "Done"], index=["To Do", "In Progress", "Done"].index(task_data["status"]))
                            new_deadline = st.date_input("Deadline", value=datetime.strptime(task_data["deadline"], "%Y-%m-%d"))
                            if st.form_submit_button("Update Task"):
                                try:
                                    edit_data = TaskForm(
                                        task_name=new_task_name,
                                        priority=new_priority,
                                        status=new_status,
                                        deadline=new_deadline.strftime("%Y-%m-%d")
                                    )
                                    update_task(task_data["id"], edit_data)
                                    st.success("Task updated successfully!")
                                    st.rerun()
                                except ValidationError as e:
                                    st.error(f"Invalid input: {e}")
            else:
                st.markdown("<p class='tooltip'>No tasks yet. Add one above!</p>", unsafe_allow_html=True)

        # Time Tracking
        with st.container():
            st.subheader("Time Tracking")
            if not tasks_df.empty:
                with st.form("time_log_form"):
                    task = st.selectbox("Task", tasks_df["task"].tolist())
                    duration = st.number_input("Duration (Minutes)", min_value=1, step=1)
                    notes = st.text_area("Notes", placeholder="What did you work on?")
                    st.markdown("<p class='tooltip'>Log time spent on tasks.</p>", unsafe_allow_html=True)
                    if st.form_submit_button("Log Time"):
                        try:
                            log_data = TimeLogForm(task=task, duration=duration, notes=notes)
                            save_time_log(st.session_state.username, log_data)
                            st.success("Time logged successfully!")
                            st.rerun()
                        except ValidationError as e:
                            st.error(f"Invalid input: {e}")
            else:
                st.markdown("<p class='tooltip'>Add tasks to log time.</p>", unsafe_allow_html=True)

    with col2:
        # Productivity Dashboard
        with st.container():
            st.subheader("Productivity Insights")
            if not time_logs_df.empty:
                time_logs_df["date"] = pd.to_datetime(time_logs_df["date"])
                date_range = st.date_input("Date Range", [datetime.today() - timedelta(days=7), datetime.today()])
                start_date, end_date = date_range
                filtered_logs = time_logs_df[
                    (time_logs_df["date"] >= pd.to_datetime(start_date)) & 
                    (time_logs_df["date"] <= pd.to_datetime(end_date) + timedelta(days=1))
                ]
                if not filtered_logs.empty:
                    task_summary = filtered_logs.groupby("task")["duration"].sum().reset_index()
                    fig = px.pie(task_summary, values="duration", names="task", title="Time per Task",
                                 color_discrete_sequence=["#39FF14", "#2ECC71", "#1F8A44"],
                                 height=300)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    daily_summary = filtered_logs.groupby(filtered_logs["date"].dt.date)["duration"].sum().reset_index()
                    fig2 = px.line(daily_summary, x="date", y="duration", title="Daily Coding Time",
                                   line_shape="spline", color_discrete_sequence=["#39FF14"],
                                   height=300)
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.markdown("<p class='tooltip'>No logs in this date range.</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p class='tooltip'>Log time to see insights.</p>", unsafe_allow_html=True)

    # Bottom Section: Code Editor, API Key, Astrology
    with st.container():
        st.subheader("Code Editor")
        code = ace.st_ace(
            value="# Write your code here\nprint('Hello, Coder!')",
            language="python",
            theme="monokai",
            font_size=14,
            min_lines=8,
            max_lines=15
        )
        col_run, col_clear = st.columns([1, 1])
        with col_run:
            if st.button("Run Code", help="Execute the code above"):
                output_buffer = StringIO()
                try:
                    with redirect_stdout(output_buffer):
                        exec(code)
                    output = output_buffer.getvalue()
                    st.session_state.code_output = output if output else "Code executed successfully (no output)."
                except Exception as e:
                    st.session_state.code_output = f"Error: {str(e)}"
                    logging.error(f"Code execution error: {e}")
                finally:
                    output_buffer.close()
        with col_clear:
            if st.button("Clear Console", help="Reset console output"):
                st.session_state.code_output = ""
        st.markdown("**Console Output**")
        st.text_area("Output", value=st.session_state.code_output, height=100, disabled=True)
        st.markdown("<p class='tooltip'>Write and run Python code; view results here.</p>", unsafe_allow_html=True)

    with st.container():
        st.subheader("API Key Manager")
        with st.form("api_key_form"):
            api_key = st.text_input("API Key", type="password", placeholder="Enter key for external tools")
            st.markdown("<p class='tooltip'>Securely store API keys for your tools.</p>", unsafe_allow_html=True)
            if st.form_submit_button("Save API Key"):
                save_api_key(st.session_state.username, api_key)
                st.success("API key saved successfully!")
                st.rerun()




if not st.session_state.logged_in:
    auth_page()
else:
    dashboard_page()