import streamlit as st



# Custom CSS for styling tiles
st.markdown("""
    <style>
    .tile {
        background-color: #262730;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
        height: 250px;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        margin-bottom: 20px;
    }
    .tile:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(255, 75, 75, 0.2);
    }
    .tile-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #fff;
        margin-bottom: 10px;
    }
    .tile-desc {
        font-size: 0.9em;
        color: #a0aec0;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .header {
        text-align: center;
        margin-bottom: 40px;
    }
    .header h1 {
        font-size: 2.5em;
        color: #fff;
    }
    .header p {
        font-size: 1.1em;
        color: #718096;
        max-width: 800px;
        margin: 0 auto;
    }
    .search-container {
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header">
        <h1>Programmer 101</h1>
        <p>Explore innovative Streamlit project ideas to enhance your coding workflow, from code runners to AI assistants. Each project is designed to solve real-world developer problems with practical features.</p>
    </div>
""", unsafe_allow_html=True)

# Search input
with st.container():
    left, middle, empty, right = st.columns([1, 1.5, 0.5, 0.5])
    with middle:
        search_query = st.text_input("", key="tools_input", placeholder="Search tools...", label_visibility="collapsed")

# Project data
projects = [
    {
        "title": "Code Snippet Organizer",
        "description": "Store and organize code snippets with tags (#regex, #pandas). Features copy button, search, filter, and local/Firebase storage.",
        "icon": "📋",
        "url":"/snippet-library"
    },
    {
        "title": "Dev Time Tracker",
        "description": "Track coding time with start/stop timers, task notes, project categories, weekly charts, and CSV export.",
        "icon": "⏱️",
        "url":"#"
    },
    {
        "title": "Regex Tester",
        "description": "Test regex patterns with live match previews, explanations, and the ability to save favorite patterns.",
        "icon": "🔍",
        "url":"#"
    },
    {
        "title": "Markdown Note Manager",
        "description": "Manage Markdown notes with tagging, categorization, local file sync, and live preview rendering.",
        "icon": "📝",
        "url":"#"
    },
    {
        "title": "Multi-Language Code Runner",
        "description": "Run code in Python, JS, C++, and more with instant output/error display. Supports offline execution via subprocess.",
        "icon": "💻",
        "url":"#"
    },
    {
        "title": "API Request Tester",
        "description": "Test APIs with URL, method, headers, and body inputs. View responses and save request presets.",
        "icon": "🌐",
        "url":"#"
    },
    {
        "title": "GitHub Project Dashboard",
        "description": "View repo stats (stars, forks, issues), filter by language, and render README/commits. Optional GitHub auth.",
        "icon": "🐙",
        "url":"#"
    },
    {
        "title": "Portfolio + Resume Generator",
        "description": "Create resumes/portfolios via forms for experience, projects, and skills. Export as PDF or HTML.",
        "icon": "📄",
        "url":"#"
    },
    {
        "title": "CLI-to-GUI Wrapper",
        "description": "GUI for CLI tools like ffmpeg, yt-dlp, git. Enter flags, run locally, and view real-time logs.",
        "icon": "🖥️",
        "url":"#"
    },
    {
        "title": "Learn/Track New Tech",
        "description": "Track tech learning with roadmaps, resource links, and checkboxes for completed topics.",
        "icon": "📚",
        "url":"#"
    },
    {
        "title": "AI Prompt Vault",
        "description": "Save and categorize AI prompts for ChatGPT/Copilot with tags, templates, and usage history.",
        "icon": "🤖",
        "url":"#"
    },
    {
        "title": "Tech Stack Comparator",
        "description": "Compare frameworks/libraries with pros/cons, benchmarks, popularity, and visual charts.",
        "icon": "⚖️",
        "url":"#"
    },
    {
        "title": "JSON/YAML Viewer + Formatter",
        "description": "View, format, and validate JSON/YAML with syntax highlighting and format conversion.",
        "icon": "📊",
        "url":"#"
    },
    {
        "title": "Cron Job Generator",
        "description": "Generate cron expressions visually with human-readable outputs and current time testing.",
        "icon": "⏰",
        "url":"#"
    },
    {
        "title": "Text/Log Analyzer",
        "description": "Analyze logs with search, filter, error highlighting, and optional regex search.",
        "icon": "🔎",
        "url":"#"
    },
    {
        "title": "Terminal Command Notebook",
        "description": "Store CLI commands with descriptions, copy buttons, tool grouping, and tag/search.",
        "icon": "📓",
        "url":"#"
    },
    {
        "title": "Code Complexity Visualizer",
        "description": "Analyze code complexity (cyclomatic, line counts) using radon/lizard with visualizations.",
        "icon": "📈",
        "url":"#"
    },
    {
        "title": "REST to GraphQL Converter",
        "description": "Convert REST schemas/endpoints to GraphQL with schema/output previews.",
        "icon": "🔄",
        "url":"#"
    },
    {
        "title": "Dockerfile Generator",
        "description": "Generate Dockerfiles by selecting language, base image, env vars, and ports. Download or copy.",
        "icon": "🐳",
        "url":"#"
    },
    {
        "title": "Code Diff Visualizer",
        "description": "Compare code snippets with Git-style diff highlighting for clear change visualization.",
        "icon": "🔀",
        "url":"#"
    },
    {
        "title": "Unit Test Generator",
        "description": "Generate Python unit tests from function code, export to test files, and run tests.",
        "icon": "🧪",
        "url":"#"
    },
    {
        "title": "Shell Script Helper",
        "description": "Build bash/zsh scripts visually with snippet helpers, validation, and previews.",
        "icon": "🐚",
        "url":"#"
    },
    {
        "title": "AI Coding Assistant",
        "description": "Local/offline code explanations, syntax fixes, and comment generation using CodeBERT.",
        "icon": "🧠",
        "url":"#"
    },
    {
        "title": "Git Branch Visualizer",
        "description": "Visualize Git branches, commits, merges, and authors from repo or .git data.",
        "icon": "🌳",
        "url":"#"
    },
    {
        "title": "Terminal Output Formatter",
        "description": "Beautify terminal output with colors and export as HTML or Markdown for sharing.",
        "icon": "🎨",
        "url":"#"
    }
]

# Filter projects based on search query
if search_query:
    search_query = search_query.lower()
    filtered_projects = [
        project for project in projects
        if search_query in project['title'].lower() or search_query in project['description'].lower()
    ]
else:
    filtered_projects = projects

# Display projects in a grid
st.markdown("## Tools")
if not filtered_projects:
    st.warning("No tools found matching your search.")
else:
    for i in range(0, len(filtered_projects), 4):
        cols = st.columns(4)
        for j, col in enumerate(cols):
            if i + j < len(filtered_projects):
                project = filtered_projects[i + j]
                with col:
                    st.markdown(f"""
                        <div class="tile">
                            <div class="tile-title"><a href="{project['url']}", target="_self">{project['icon']} {project['title']}</a></div>
                            <p class="tile-desc">{project['description']}</p>
                        </div>
                    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 40px; color: #718096;">
        <p>Built with Streamlit | © 2025 Programmer 101</p>
    </div>
""", unsafe_allow_html=True)