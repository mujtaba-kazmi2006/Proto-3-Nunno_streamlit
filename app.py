import streamlit as st
import os
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Nunno AI - Finance Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables FIRST
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_age" not in st.session_state:
    st.session_state.user_age = ""
if "profile_setup" not in st.session_state:
    st.session_state.profile_setup = False
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "ai_api_key" not in st.session_state:
    st.session_state.ai_api_key = ""
if "api_key_setup" not in st.session_state:
    st.session_state.api_key_setup = False
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

def get_theme_css():
    """Return CSS based on current theme mode"""
    if st.session_state.dark_mode:
        return """
        <style>
            .stApp {
                background: linear-gradient(180deg, #0e1117 0%, #1a1d24 100%);
                color: #fafafa;
            }
            
            /* Custom metrics styling */
            [data-testid="metric-container"] {
                background-color: rgba(30, 35, 41, 0.8);
                border: 1px solid rgba(0, 212, 170, 0.2);
                padding: 1rem;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            /* Button styling */
            .stButton > button {
                background: linear-gradient(45deg, #00d4aa, #0088cc);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .stButton > button:hover {
                background: linear-gradient(45deg, #00b894, #0074cc);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 212, 170, 0.3);
            }
            
            /* Sidebar styling */
            .css-1d391kg {
                background-color: #1e2329;
            }
            
            /* Input styling */
            .stTextInput > div > div > input {
                background-color: rgba(30, 35, 41, 0.8);
                border: 1px solid rgba(0, 212, 170, 0.3);
                border-radius: 8px;
                color: #fafafa !important;
            }
            
            /* All text elements */
            h1, h2, h3, h4, h5, h6, p, div, span, label, .stMarkdown {
                color: #fafafa !important;
            }
            
            /* Mobile responsive */
            @media (max-width: 768px) {
                .stApp { padding: 0.5rem; }
                h1 { font-size: 1.5rem !important; }
                h2 { font-size: 1.3rem !important; }
                h3 { font-size: 1.1rem !important; }
                .stButton > button { width: 100%; margin-bottom: 0.5rem; }
            }
        </style>
        """
    else:
        return """
        <style>
            .stApp {
                background: linear-gradient(180deg, #ffffff 0%, #f0f2f6 100%);
                color: #262730;
            }
            
            /* Custom metrics styling */
            [data-testid="metric-container"] {
                background-color: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(0, 212, 170, 0.3);
                padding: 1rem;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            /* Button styling */
            .stButton > button {
                background: linear-gradient(45deg, #00d4aa, #0088cc);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .stButton > button:hover {
                background: linear-gradient(45deg, #00b894, #0074cc);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 212, 170, 0.3);
            }
            
            /* Sidebar styling */
            .css-1d391kg {
                background-color: #f8f9fa;
            }
            
            /* Input styling */
            .stTextInput > div > div > input {
                background-color: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(0, 212, 170, 0.5);
                border-radius: 8px;
                color: #262730 !important;
            }
            
            /* All text elements - Light Mode */
            h1, h2, h3, h4, h5, h6, p, div, span, label, .stMarkdown {
                color: #262730 !important;
            }
            
            /* Better contrast for light mode */
            .stMarkdown p, .stMarkdown div {
                color: #1a1a1a !important;
                font-weight: 500;
            }
            
            /* Mobile responsive */
            @media (max-width: 768px) {
                .stApp { padding: 0.5rem; }
                h1 { font-size: 1.5rem !important; }
                h2 { font-size: 1.3rem !important; }
                h3 { font-size: 1.1rem !important; }
                .stButton > button { width: 100%; margin-bottom: 0.5rem; }
            }
        </style>
        """

# Apply theme CSS
st.markdown(get_theme_css(), unsafe_allow_html=True)

# Strong text visibility overrides
override_css = f"""
<style>
    /* CRITICAL TEXT VISIBILITY OVERRIDES */
    body, div, p, span, h1, h2, h3, h4, h5, h6, label, .stMarkdown, .stText {{
        color: {"#fafafa" if st.session_state.get('dark_mode', True) else "#1a1a1a"} !important;
        text-shadow: none !important;
    }}
    
    /* Dashboard content specifically */
    [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] * {{
        color: {"#fafafa" if st.session_state.get('dark_mode', True) else "#1a1a1a"} !important;
        font-weight: 500 !important;
    }}
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {{
        .stApp {{ 
            padding: 0.5rem !important; 
        }}
        
        .main .block-container {{
            padding: 1rem 0.5rem !important;
        }}
        
        h1 {{ font-size: 1.5rem !important; }}
        h2 {{ font-size: 1.3rem !important; }}
        h3 {{ font-size: 1.1rem !important; }}
        
        .stButton > button {{ 
            width: 100% !important; 
            margin-bottom: 0.5rem !important; 
        }}
        
        [data-testid="stSidebar"] {{
            width: 280px !important;
        }}
    }}
    
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    
    /* Success/warning/error styling */
    .stSuccess {{
        background-color: rgba(0, 212, 170, 0.1);
        border-left: 4px solid #00d4aa;
    }}
    
    .stWarning {{
        background-color: rgba(255, 167, 38, 0.1);
        border-left: 4px solid #ffa726;
    }}
    
    .stError {{
        background-color: rgba(255, 75, 75, 0.1);
        border-left: 4px solid #ff4b4b;
    }}
    
    /* Chart container styling */
    .js-plotly-plot {{
        border-radius: 10px;
    }}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        border: 1px solid rgba(0, 212, 170, 0.2);
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(45deg, #00d4aa, #0088cc);
        color: white;
    }}
    
    /* Progress bar */
    .stProgress > div > div > div {{
        background-color: #00d4aa;
    }}
    
    /* Theme toggle button */
    .theme-toggle {{
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
    }}
</style>
"""

st.markdown(override_css, unsafe_allow_html=True)

# API Keys from environment variables or session state
AI_API_KEY = st.session_state.ai_api_key if st.session_state.ai_api_key else os.getenv("AI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def show_api_key_setup():
    """Display API key setup screen"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1>🔑 API Key Setup</h1>
        <h2>Please provide your OpenRouter AI API key to continue</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    ### 🤖 OpenRouter AI API Key Required
    
    To use the AI chat functionality, you need to provide your OpenRouter API key.
    
    **How to get your API key:**
    1. Visit [OpenRouter](https://openrouter.ai/)
    2. Sign up or log in to your account
    3. Go to your API keys section
    4. Copy your API key
    
    **Your API key will be securely stored for this session only.**
    """)
    
    api_key = st.text_input(
        "Enter your OpenRouter API Key:",
        type="password",
        placeholder="sk-or-v1-...",
        help="Your API key starts with 'sk-or-v1-'"
    )
    
    if st.button("Save API Key", type="primary"):
        if api_key and api_key.startswith("sk-or-v1-"):
            st.session_state.ai_api_key = api_key
            st.session_state.api_key_setup = True
            st.success("API key saved successfully!")
            st.rerun()
        elif api_key:
            st.error("Invalid API key format. OpenRouter keys start with 'sk-or-v1-'")
        else:
            st.error("Please enter your API key.")

def show_welcome():
    """Display welcome screen"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1>🌟✨💫🧠 Welcome to Nunno AI!</h1>
        <h2>💰 Your Personal Finance Assistant</h2>
        <h3>📊 Built by Mujtaba Kazmi</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if not st.session_state.profile_setup:
        st.markdown("### 👤 Let's set up your profile first!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("What's your name?", value=st.session_state.user_name)
        
        with col2:
            age = st.text_input("How old are you?", value=st.session_state.user_age)
        
        if st.button("Save Profile", type="primary"):
            if name and age:
                st.session_state.user_name = name
                st.session_state.user_age = age
                st.session_state.profile_setup = True
                st.success(f"Welcome, {name}! Your profile has been saved.")
                st.rerun()
            else:
                st.error("Please fill in both name and age.")
    else:
        st.success(f"👋 Welcome back, {st.session_state.user_name} ({st.session_state.user_age} years old)!")
        
        if st.button("Edit Profile"):
            st.session_state.profile_setup = False
            st.rerun()

def main():
    # Theme toggle button in top corner
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        theme_icon = "🌙" if st.session_state.dark_mode else "☀️"
        theme_text = "Light Mode" if st.session_state.dark_mode else "Dark Mode"
        if st.button(f"{theme_icon} {theme_text}", key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    # Check if API key is set up first
    if not st.session_state.api_key_setup:
        show_api_key_setup()
        return
    
    # Sidebar
    with st.sidebar:
        st.title("🧠 Nunno AI")
        st.markdown("Your Finance Learning Companion")
        
        if st.session_state.profile_setup:
            st.markdown(f"👤 **{st.session_state.user_name}** ({st.session_state.user_age})")
        
        st.markdown("---")
        
        st.markdown("""
        ### 🚀 What I can help you with:
        
        - 🔮 **AI Chat**: Ask me anything about finance
        - 📊 **Trading Analysis**: Technical analysis with confluences
        - 💰 **Tokenomics**: Analyze cryptocurrency investments
        - 📰 **Market News**: Latest financial news
        - ⚙️ **Settings**: Manage your profile and preferences
        """)
        
        st.markdown("---")
        
        st.markdown("""
        ### 💡 Quick Tips:
        - Ask me naturally in plain English
        - I can analyze any cryptocurrency
        - Try "Analyze Bitcoin" or "Should I invest in Ethereum?"
        - Check market news for the latest updates
        """)

    # Main content
    if not st.session_state.profile_setup:
        show_welcome()
    else:
        st.markdown(f"""
        # 🎉 Welcome to Nunno AI, {st.session_state.user_name}!
        
        I'm here to help you learn investing and trading in simple terms.
        
        ### 🚀 Choose what you'd like to do:
        
        Use the sidebar navigation to explore different features:
        
        - **🔮 AI Chat**: Have a conversation with me about finance
        - **📊 Trading Analysis**: Get technical analysis with confluence signals  
        - **💰 Tokenomics**: Analyze cryptocurrency investments
        - **📰 Market News**: Stay updated with latest market news
        - **⚙️ Settings**: Manage your profile and preferences
        
        ### 💡 Getting Started:
        
        1. **New to trading?** Start with the AI Chat to ask basic questions
        2. **Want to analyze a coin?** Use the Tokenomics page
        3. **Looking for signals?** Check out Trading Analysis
        4. **Stay informed?** Visit Market News for latest updates
        
        Select a page from the sidebar to get started! 👈
        """)
        
        # Quick action buttons
        st.markdown("### 🎯 Quick Actions:")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔮 Start AI Chat", use_container_width=True):
                st.switch_page("pages/1_🔮_AI_Chat.py")
        
        with col2:
            if st.button("📊 Trading Analysis", use_container_width=True):
                st.switch_page("pages/2_📊_Trading_Analysis.py")
        
        with col3:
            if st.button("💰 Tokenomics", use_container_width=True):
                st.switch_page("pages/3_💰_Tokenomics.py")
        
        with col4:
            if st.button("📰 Market News", use_container_width=True):
                st.switch_page("pages/4_📰_Market_News.py")

if __name__ == "__main__":
    main()
