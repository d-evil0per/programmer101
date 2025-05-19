import streamlit as st
import time
from datetime import datetime
from controller.codeRunner import default_code, run_python_code,run_streamlit_code, run_javascript_code, run_cpp_code, run_java_code, run_c_code, run_html_code, run_sql_code, run_typescript_code
import sqlite3
from streamlit_monaco import st_monaco
# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('snippets.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            language TEXT NOT NULL,
            code TEXT NOT NULL,
            tags TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Save snippet to database
def save_snippet(title, language, code, tags):
    conn = sqlite3.connect('snippets.db')
    c = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        'INSERT INTO snippets (title, language, code, tags, created_at) VALUES (?, ?, ?, ?, ?)',
        (title, language, code, tags, created_at)
    )
    conn.commit()
    conn.close()
    return True
def delete_snippet(snippet_id):
    try:
        with sqlite3.connect('snippets.db') as conn:
            c = conn.cursor()
            query=f'''
                DELETE FROM snippets
                WHERE id = {snippet_id}
            '''
            # print(query)
            c.execute(query)
            conn.commit()
        return True
    except sqlite3.Error as e:
        st.error(f"Failed to update snippet: {e}")
        return False
def update_snippet(snippet_id, title, language, tags, code):
    try:
        with sqlite3.connect('snippets.db') as conn:
            c = conn.cursor()
            query=f'''
                UPDATE snippets
                SET title = '{title}', language = '{language}', tags = '{tags}', code = '{code}'
                WHERE id = {snippet_id}
            '''
            print(query)
            c.execute(query)
            conn.commit()
        return True
    except sqlite3.Error as e:
        st.error(f"Failed to update snippet: {e}")
        return False
# Retrieve snippets with optional search and filter
def get_snippets(search_query="", language_filter=""):
    conn = sqlite3.connect('snippets.db')
    c = conn.cursor()
    query = 'SELECT id, title, language, code, tags, created_at FROM snippets'
    params = []

        # Build conditions for search and filter
    if search_query or language_filter:
        conditions = []
        
        if search_query:
            conditions.append(f'(title LIKE "%{search_query}%" OR tags LIKE "%{search_query}%")')
        
        if language_filter:
            conditions.append(f'language LIKE "%{language_filter}%"')
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
            # print(query)

        # Execute query with parameters
        c.execute(query)
        
        # Fetch results and format as list of dictionaries
        snippets = [
            {
                "id": row[0],
                "title": row[1],
                "language": row[2],
                "code": row[3],
                "tags": row[4],
                "created_at": row[5]
            }
            for row in c.fetchall()
        ]
    else:
        c.execute(query)
        snippets = [
            {"id": row[0], "title": row[1], "language": row[2], "code": row[3], "tags": row[4], "created_at": row[5]}
            for row in c.fetchall()
        ]
        print(snippets)
    conn.close()
    return snippets

# Code runner component
def coderunnerComponent():
    with st.expander("Test your Snippets here", expanded=False):
        languages = ["Python","Streamlit", "JavaScript", "C++", "Java", "C", "HTML", "SQL", "TypeScript"]
        selected_language = st.selectbox("Select Language", languages)
        # code = st.text_area("Write your code here:", height=300, value=default_code[selected_language], key="code_input")
        if selected_language.lower()=='streamlit':
            lang='python'
        else:
            lang=selected_language.lower()
        content = st_monaco(value=default_code[selected_language], height="600px", language=lang,lineNumbers=True,minimap=False,theme="vs-dark")
        # response_dict = code_editor(default_code[selected_language], lang=lang, height=[19, 22],info=info_bar, buttons=custom_btns)
        # Display the edited code if the user submits changes
        btncol1, btncol2, btncol3, btncol4 = st.columns([0.5, 2, 1, 0.7])
        with btncol1:
            run_code = st.button("Run", icon=":material/play_arrow:")
        with btncol4:
            add_snippet = st.button("Add to library", icon=":material/add_circle_outline:")
    
        # Handle snippet saving
        if add_snippet:
            addSnippet(lang=selected_language,code=content)    
        if run_code:
            code=content
            st.subheader("Output")
            output, error = "", ""
            
            if selected_language == "Python":
                output, error = run_python_code(code)
            elif selected_language == "Streamlit":
                output, error = run_streamlit_code(code)
            elif selected_language == "JavaScript":
                output, error = run_javascript_code(code)
            elif selected_language == "C++":
                output, error = run_cpp_code(code)
            elif selected_language == "Java":
                output, error = run_java_code(code)
            elif selected_language == "C":
                output, error = run_c_code(code)
            elif selected_language == "HTML":
                output, error = run_html_code(code)
            elif selected_language == "SQL":
                output, error = run_sql_code(code)
            elif selected_language == "TypeScript":
                output, error = run_typescript_code(code)
            
            if selected_language == "HTML" and output:
                st.components.v1.html(output, height=400, scrolling=True)
            elif output:
                st.code(output, language="text")
            if error:
                st.error(error)        



@st.dialog("Add Snippet")
def addSnippet(lang="Python",code=""):
    st.write("Add snippet into the library..")
    title = st.text_input("Snippet Title", placeholder="Enter a title for your snippet")
    languages = ["Python","Streamlit","JavaScript", "C++", "Java", "C", "HTML", "SQL", "TypeScript"]
    selected_language = st.selectbox("Select programming Language", languages,index=languages.index(lang))
    snippet = st.text_area("Write your code here:",code, height=300)
    tags = st.text_input("",placeholder="Add tags with comma sperated!!")
    if st.button("Add", icon=":material/add_circle_outline:"):
        save_snippet(title, selected_language, snippet, tags)
        st.toast('Adding Snippet!')
        time.sleep(.5)
        st.toast('Hooray! Saved', icon='🎉')
        st.rerun()          
@st.dialog("Edit Snippet")
def editSnippet(snippet_id="",language="Python",code="",tags="",title=""):
    st.write("Update snippet into the library..")
    up_title = st.text_input("Update Snippet Title",title, placeholder="Enter a title for your snippet")
    up_languages = ["Python","Streamlit","JavaScript", "C++", "Java", "C", "HTML", "SQL", "TypeScript"]
    up_selected_language = st.selectbox("Update programming Language", up_languages,index=up_languages.index(language))
    up_snippet = st.text_area("Write your code here:",code, height=300)
    up_tags = st.text_input("",tags,placeholder="Add tags with comma sperated!!")
    if st.button("update", icon=":material/add_circle_outline:"):
        update_snippet(snippet_id, up_title, up_selected_language, up_tags, up_snippet)
        st.toast('updating Snippet!')
        time.sleep(.5)
        st.toast('Hooray! Updated!!', icon='🎉')
        st.rerun()    
@st.dialog("Are you sure?")
def deleteSnippet(snippet_id=""):
    st.markdown("Do you want to delete this snippet :red[**permanently**]?")
    left,middle,right=st.columns([0.5,1,0.5])
    if left.button("Yes", icon=":material/check_circle:"):
        delete_snippet(snippet_id)
        st.toast('updating Snippet!')
        time.sleep(.5)
        st.toast('Hooray! Updated!!', icon='🎉')
        st.rerun()  
    if right.button("No", icon=":material/cancel:"):
        st.rerun()   
def updateDailog(snippet_id,language,code,tags,title):
    editSnippet(snippet_id,language,code,tags,title) 
def deleteDailog(snippet_id):
    deleteSnippet(snippet_id) 
def snippetLibrary():
    # Set page configuration with a celestial favicon and title
    st.markdown("""<style>
                .stColumn {
                align-content:flex-end;
                }
                </style>""", unsafe_allow_html=True)
    st.title("Snippet Library")

    with st.container():
        left,middle,empty,right=st.columns([1.5,1,0.5,0.5])
        with left:
            key_search=st.text_input(" ",key="snippet_search", placeholder="Search...",icon=":material/search:",label_visibility="collapsed")
        with middle:
            lang_filter= st.selectbox(" ",["Python","Streamlit", "JavaScript", "C++", "Java", "C", "HTML", "SQL", "TypeScript"],index=None,placeholder="Filter by Tags...",label_visibility="collapsed")
        with right:
            
            if st.button("Add Snippet", icon=":material/add_circle_outline:"):
                addSnippet()
        coderunnerComponent()
        snippets_details = get_snippets(key_search, lang_filter)
        if not snippets_details:
            st.info("No snippets found. Save some using the 'Add to library' button above.")
        else:
            for i in range(0, len(snippets_details), 4):
                cols = st.columns(4)
                for j, col in enumerate(cols):
                    if i + j < len(snippets_details):
                        snippet = snippets_details[i + j]
                        with col:
                            with st.container(border=True):
                                # {updateDailog(snippet['id'],  snippet['language'],snippet['code'], snippet['tags'],snippet['title'])}s

                                left,middle,right1,right2=st.columns([0.4,0.2,0.1,0.1])
                                left.markdown(f":green[**Snippet #{snippet['id']}**]")
                                if right1.button(":material/edit:",key="editbtn_"+str(snippet['id']),help="Edit Snippet"):
                                    updateDailog(snippet['id'],  snippet['language'],snippet['code'], snippet['tags'],snippet['title'])
                                if right2.button(":material/delete:",key="deletebtn_"+str(snippet['id']),help="Delete Snippet"):
                                    deleteDailog(snippet['id'])
                                st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items: center;">
                                            <div style="margin-right:auto"><strong>{snippet['title']}</strong></div>
                                            """,unsafe_allow_html=True)
                                badges=""
                                for tag in (snippet['tags'] or '').split(','):
                                    badges+=f":green-badge[:material/tag: {tag.strip()}] "
                                st.markdown(badges)
                                with st.expander(snippet['language'].upper(),expanded=True):
                                    if snippet['language'].lower()=="streamlit":
                                        st.code(snippet['code'],language='python',height=200)
                                    else:    
                                        st.code(snippet['code'],language=snippet['language'].lower(),height=200)


if __name__=="__main__":
    # Initialize database
    init_db()
    snippetLibrary()
