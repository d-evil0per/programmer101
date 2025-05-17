import sqlite3
import json

# JSON data (the provided snippets)
json_data = [
    {
        "title": "Slider for Numeric Input",
        "tags": ["streamlit", "python", "slider", "input", "widget"],
        "code": "import streamlit as st\n\n# Slider for selecting a numeric value\nage = st.slider('Select your age', min_value=0, max_value=100, value=25, step=1)\nst.write(f'Your age is: {age}')",
        "language": "Streamlit"
    },
    {
        "title": "File Uploader",
        "tags": ["streamlit", "python", "file-uploader", "input", "data"],
        "code": "import streamlit as st\n\n# File uploader for CSV files\nuploaded_file = st.file_uploader('Upload a CSV file', type=['csv'])\nif uploaded_file is not None:\n    import pandas as pd\n    df = pd.read_csv(uploaded_file)\n    st.write('Uploaded file:', df)",
        "language": "Streamlit"
    },
    {
        "title": "Checkbox for Toggle",
        "tags": ["streamlit", "python", "checkbox", "input", "ui"],
        "code": "import streamlit as st\n\n# Checkbox to toggle visibility\nshow_text = st.checkbox('Show greeting', value=True)\nif show_text:\n    st.write('Hello, Streamlit!')\nelse:\n    st.write('Greeting hidden')",
        "language": "Streamlit"
    },
    {
        "title": "Radio Buttons for Single Selection",
        "tags": ["streamlit", "python", "radio", "input", "selection"],
        "code": "import streamlit as st\n\n# Radio buttons for single choice\ncolor = st.radio('Choose a color', ['Red', 'Blue', 'Green'])\nst.write(f'You selected: {color}')",
        "language": "Streamlit"
    },
    {
        "title": "Multiselect Dropdown",
        "tags": ["streamlit", "python", "multiselect", "input", "dropdown"],
        "code": "import streamlit as st\n\n# Multiselect for multiple choices\nfruits = st.multiselect('Select your favorite fruits', ['Apple', 'Banana', 'Orange', 'Mango'])\nst.write(f'You selected: {fruits}')",
        "language": "Streamlit"
    },
    {
        "title": "Text Area for Long Input",
        "tags": ["streamlit", "python", "textarea", "input", "widget"],
        "code": "import streamlit as st\n\n# Text area for longer text input\nfeedback = st.text_area('Enter your feedback', height=150)\nif feedback:\n    st.write('Your feedback:', feedback)",
        "language": "Streamlit"
    },
    {
        "title": "Number Input Widget",
        "tags": ["streamlit", "python", "number-input", "input", "widget"],
        "code": "import streamlit as st\n\n# Number input for precise numeric values\nquantity = st.number_input('Enter quantity', min_value=0, max_value=100, value=10, step=1)\nst.write(f'Quantity selected: {quantity}')",
        "language": "Streamlit"
    },
    {
        "title": "Date Input Picker",
        "tags": ["streamlit", "python", "date-input", "input", "calendar"],
        "code": "import streamlit as st\n\n# Date input for selecting a date\ndate = st.date_input('Select a date')\nst.write(f'Selected date: {date}')",
        "language": "Streamlit"
    },
    {
        "title": "Time Input Picker",
        "tags": ["streamlit", "python", "time-input", "input", "clock"],
        "code": "import streamlit as st\n\n# Time input for selecting a time\ntime = st.time_input('Select a time')\nst.write(f'Selected time: {time}')",
        "language": "Streamlit"
    },
    {
        "title": "Color Picker",
        "tags": ["streamlit", "python", "color-picker", "input", "ui"],
        "code": "import streamlit as st\n\n# Color picker for selecting a color\ncolor = st.color_picker('Pick a color', '#FF0000')\nst.write(f'Selected color: {color}')\nst.markdown(f'<div style=\"background-color:{color};height:50px;\"></div>', unsafe_allow_html=True)",
        "language": "Streamlit"
    },
    {
        "title": "Progress Bar",
        "tags": ["streamlit", "python", "progress-bar", "ui", "feedback"],
        "code": "import streamlit as st\nimport time\n\n# Progress bar for task progress\nprogress = st.progress(0)\nfor i in range(100):\n    time.sleep(0.05)\n    progress.progress(i + 1)\nst.write('Task completed!')",
        "language": "Streamlit"
    },
    {
        "title": "Spinner for Loading",
        "tags": ["streamlit", "python", "spinner", "ui", "feedback"],
        "code": "import streamlit as st\nimport time\n\n# Spinner during processing\nwith st.spinner('Processing...'):\n    time.sleep(2)\n    st.write('Processing complete!')",
        "language": "Streamlit"
    },
    {
        "title": "Sidebar Navigation",
        "tags": ["streamlit", "python", "sidebar", "layout", "navigation"],
        "code": "import streamlit as st\n\n# Sidebar for navigation\nst.sidebar.title('Navigation')\npage = st.sidebar.selectbox('Go to', ['Home', 'Settings', 'About'])\nst.write(f'You are on the {page} page')",
        "language": "Streamlit"
    },
    {
        "title": "Columns Layout",
        "tags": ["streamlit", "python", "columns", "layout", "ui"],
        "code": "import streamlit as st\n\n# Two-column layout\ncol1, col2 = st.columns(2)\nwith col1:\n    st.write('Column 1 content')\n    st.button('Button 1')\nwith col2:\n    st.write('Column 2 content')\n    st.button('Button 2')",
        "language": "Streamlit"
    },
    {
        "title": "Expander for Collapsible Content",
        "tags": ["streamlit", "python", "expander", "layout", "ui"],
        "code": "import streamlit as st\n\n# Expander for collapsible content\nwith st.expander('See more details'):\n    st.write('This is hidden by default')\n    st.write('Click to expand/collapse')",
        "language": "Streamlit"
    },
    {
        "title": "Session State Counter",
        "tags": ["streamlit", "python", "session-state", "state", "interaction"],
        "code": "import streamlit as st\n\n# Session state for persistent counter\nif 'count' not in st.session_state:\n    st.session_state.count = 0\nif st.button('Increment'):\n    st.session_state.count += 1\nst.write(f'Count: {st.session_state.count}')",
        "language": "Streamlit"
    },
    {
        "title": "Form for Batch Submission",
        "tags": ["streamlit", "python", "form", "input", "submission"],
        "code": "import streamlit as st\n\n# Form for batch input submission\nwith st.form(key='my_form'):\n    name = st.text_input('Name')\n    age = st.number_input('Age', min_value=0)\n    submit = st.form_submit_button('Submit')\nif submit:\n    st.write(f'Name: {name}, Age: {age}')",
        "language": "Streamlit"
    },
    {
        "title": "Area Chart Visualization",
        "tags": ["streamlit", "python", "chart", "visualization", "plot"],
        "code": "import streamlit as st\nimport pandas as pd\nimport numpy as np\n\n# Area chart for data visualization\nchart_data = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])\nst.area_chart(chart_data)",
        "language": "Streamlit"
    },
    {
        "title": "Metric Display",
        "tags": ["streamlit", "python", "metric", "data-display", "ui"],
        "code": "import streamlit as st\n\n# Metric for key performance indicators\nst.metric(label='Temperature', value='25°C', delta='1.2°C')\nst.metric(label='Sales', value='$1000', delta='-5%')",
        "language": "Streamlit"
    },
    {
        "title": "Custom CSS Styling",
        "tags": ["streamlit", "python", "css", "styling", "ui"],
        "code": "import streamlit as st\n\n# Custom CSS for styling\nst.markdown('''\n    <style>\n    .big-font {\n        font-size: 24px;\n        color: #FF4B4B;\n    }\n    </style>\n''', unsafe_allow_html=True)\nst.markdown('<p class=\"big-font\">Styled text with CSS</p>', unsafe_allow_html=True)",
        "language": "Streamlit"
    }
]

def create_and_insert_snippets(db_name="snippets.db"):
    try:
        # Connect to SQLite database (creates file if it doesn't exist)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Insert JSON data into the table
        for item in json_data:
            # Convert tags list to a comma-separated string
            tags_str = ",".join(item["tags"])
            cursor.execute('''INSERT INTO snippets (title, tags, code, language)
                              VALUES (?, ?, ?, ?)''',
                           (item["title"], tags_str, item["code"], item["language"]))

        # Commit changes
        conn.commit()
        print(f"Successfully inserted {len(json_data)} snippets into {db_name}")

        # Verify the tags are stored as comma-separated strings
        cursor.execute("SELECT title, tags FROM snippets")
        rows = cursor.fetchall()
        print("\nVerifying stored tags:")
        for row in rows:
            title, tags = row
            print(f"Title: {title}, Tags: {tags}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close connection
        if conn:
            conn.close()
            print("Database connection closed")

if __name__ == "__main__":
    create_and_insert_snippets()