import streamlit as st
import logging



# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_session_state():
    pass


def configure_page():
    """
    The `configure_page` function sets the configuration for a web page, including the title, icon, and
    layout.
    """
    st.set_page_config(page_title="Programmer101", page_icon=":material/code_blocks:",layout="wide")

def setup_navigation():
    
    pages = {
            "Menu":[st.Page("pages/home.py", title="Home",default=True,icon=":material/home:")],
            "Tools": [
                
                st.Page("pages/snippet-library.py", title="Snippet Library",icon=":material/developer_guide:")
            ]
        }

    pg = st.navigation(pages,position="sidebar",expanded=True)
    pg.run()

def customize_sidebar():
    # st.sidebar.markdown(":green[:material/code_blocks: Programmer101]")
    
    sidecontainer=st.sidebar.container(border=False,key="sidebar-container")
    with sidecontainer:
        st.divider()
        st.markdown('<h6>Made by &nbsp<a href="mailto:dhir.xcess@gmail.com">Deviloper</a></h6>',unsafe_allow_html=True)

# Custom CSS with Tailwind-inspired styles
def apply_custom_styles():
    st.markdown("""
        <style>
        .stColumn {
            align-content:flex-end;
            }
        .st-emotion-cache-1e8q7rb  {
            align-content:flex-end;
            }
            .st-emotion-cache-uh2d79 a{
                color:#fff;
                text-decoration: none;
            }
            [data-testid="stSidebarHeader"]::before {
                content: "[<>] programmer 101";
                font-size: 18px;
                color:rgb(61, 213, 109);
                margin-left:20px;
            }
            .st-key-sidebar-container h6{
                display: flex;
                justify-content: center;
            }
            [class*="st-key-editbtn_"] .st-emotion-cache-ktz07o {
                border:none;
                background:transparent;
                }
            [class*="st-key-deletebtn_"] .st-emotion-cache-ktz07o {
                border:none;
                background:transparent;
                color:#FF4B4B;
                }
        </style>
    """, unsafe_allow_html=True)
def main():
    initialize_session_state()
    configure_page()
    setup_navigation()
    customize_sidebar()
    apply_custom_styles()
if __name__=="__main__":
    main()