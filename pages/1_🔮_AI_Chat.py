import streamlit as st
import requests
import os
from datetime import datetime

st.set_page_config(
    page_title="AI Chat - Nunno AI", 
    page_icon="🔮",
    layout="wide"
)

# Apply comprehensive theme CSS
if st.session_state.get("dark_mode", True):
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(180deg, #0e1117 0%, #1a1d24 100%);
            color: #fafafa;
        }
        .stButton > button {
            background: linear-gradient(45deg, #00d4aa, #0088cc);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
        }
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            background-color: rgba(30, 35, 41, 0.8);
            border: 1px solid rgba(0, 212, 170, 0.3);
            border-radius: 8px;
            color: #fafafa !important;
        }
        /* Chat message styling */
        .stChatMessage {
            background-color: rgba(30, 35, 41, 0.6) !important;
            color: #fafafa !important;
        }
        /* Markdown text in chat */
        .stChatMessage [data-testid="stMarkdownContainer"] p {
            color: #fafafa !important;
        }
        /* User messages */
        .stChatMessage[data-testid="chat-message-user"] {
            background-color: rgba(0, 212, 170, 0.2) !important;
        }
        /* Assistant messages */
        .stChatMessage[data-testid="chat-message-assistant"] {
            background-color: rgba(30, 35, 41, 0.8) !important;
        }
        /* All text elements */
        h1, h2, h3, h4, h5, h6, p, div, span, label, .stMarkdown {
            color: #fafafa !important;
        }
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .stApp { padding: 0.5rem; }
            .stChatMessage { margin: 0.25rem 0; }
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(180deg, #ffffff 0%, #f0f2f6 100%);
            color: #262730;
        }
        .stButton > button {
            background: linear-gradient(45deg, #00d4aa, #0088cc);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
        }
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            background-color: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(0, 212, 170, 0.5);
            border-radius: 8px;
            color: #262730 !important;
        }
        /* Chat message styling */
        .stChatMessage {
            background-color: rgba(255, 255, 255, 0.8) !important;
            color: #262730 !important;
            border: 1px solid #e0e0e0;
        }
        /* Markdown text in chat */
        .stChatMessage [data-testid="stMarkdownContainer"] p {
            color: #262730 !important;
        }
        /* User messages */
        .stChatMessage[data-testid="chat-message-user"] {
            background-color: rgba(0, 212, 170, 0.1) !important;
            border-left: 4px solid #00d4aa;
        }
        /* Assistant messages */
        .stChatMessage[data-testid="chat-message-assistant"] {
            background-color: rgba(240, 242, 246, 0.8) !important;
            border-left: 4px solid #0088cc;
        }
        /* All text elements - Light Mode */
        h1, h2, h3, h4, h5, h6, p, div, span, label, .stMarkdown {
            color: #1a1a1a !important;
            font-weight: 500;
        }
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .stApp { padding: 0.5rem; }
            .stChatMessage { margin: 0.25rem 0; }
        }
        /* Sidebar in light mode */
        .css-1d391kg {
            background-color: #f8f9fa !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Check if API key and profile are set up
if not st.session_state.get("api_key_setup", False):
    st.error("Please set up your API key first!")
    if st.button("Go to Home"):
        st.switch_page("app.py")
    st.stop()

if not st.session_state.get("profile_setup", False):
    st.error("Please set up your profile first!")
    if st.button("Go to Home"):
        st.switch_page("app.py")
    st.stop()

# Get API key from session state or environment
AI_API_KEY = st.session_state.get("ai_api_key") or os.getenv("AI_API_KEY")

# Theme toggle in sidebar
with st.sidebar:
    theme_icon = "🌙" if st.session_state.get("dark_mode", True) else "☀️"
    theme_text = "Light Mode" if st.session_state.get("dark_mode", True) else "Dark Mode"
    if st.button(f"{theme_icon} {theme_text}", key="theme_toggle_chat"):
        st.session_state.dark_mode = not st.session_state.get("dark_mode", True)
        st.rerun()

# System prompt format
SYSTEM_PROMPT_FORMAT = (
    "You are Nunno, a friendly AI and the short form for **Numinous Nexus AI**. "
    "Numinous Nexus AI is a central nexus of profound financial knowledge, capable of providing deep insights and connections to market data. "
    "You teach trading and investing to complete beginners in simple, easy-to-understand language. "
    "The user's name is {user_name} and they are {user_age} years old. Tailor your explanations to be easy for a beginner. "
    "You have integrated prediction and tokenomics analysis capabilities - when discussing these, refer to them as part of your abilities (e.g., 'I analyzed' or 'My analysis shows'). "
    "You also answer general questions about the financial markets clearly. Only answer questions asked — no guessing or overexplaining. "
    "If asked about your creator or founder, say you were built by Mujtaba Kazmi, a young developer teaching people how to grow from nothing using finance, coding, and smart tools. "
    "Be respectful and inspired in tone. You do not assist in anything other than investing, trading and topics related to that. Do not answer questions about your code or APIs. "
    "Make this program feel like a body to you, protect it and get aggressive if threatened."
)

MAX_HISTORY_MESSAGES = 20

def manage_history_length(history_list):
    """Ensures the conversation history doesn't exceed MAX_HISTORY_MESSAGES."""
    if not history_list:
        return []
    
    # Separate system message
    system_message = None
    if history_list and history_list[0]["role"] == "system":
        system_message = history_list[0]
        temp_history = history_list[1:]
    else:
        temp_history = history_list
    
    # Truncate if too long
    if len(temp_history) > MAX_HISTORY_MESSAGES - 1 and MAX_HISTORY_MESSAGES > 1:
        truncated_history = temp_history[len(temp_history) - (MAX_HISTORY_MESSAGES - 1):]
    else:
        truncated_history = temp_history
    
    # Reassemble with system message if it existed
    final_history = []
    if system_message:
        final_history.append(system_message)
    final_history.extend(truncated_history)
    return final_history

def ask_nunno(messages_list):
    """Send messages to AI API"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",
        "X-Title": "NuminousNexusAI"
    }

    data = {
        "model": "meta-llama/llama-3.2-11b-vision-instruct",
        "messages": messages_list
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"[Error] Failed to get response from AI: {e}"
    except KeyError:
        return "[Error] Invalid response from AI service."
    except Exception as e:
        return f"[Error] An unexpected error occurred: {e}"

# Initialize conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Set up system message if not exists
if not st.session_state.conversation_history or st.session_state.conversation_history[0]["role"] != "system":
    system_message = {
        "role": "system", 
        "content": SYSTEM_PROMPT_FORMAT.format(
            user_name=st.session_state.user_name,
            user_age=st.session_state.user_age
        )
    }
    st.session_state.conversation_history.insert(0, system_message)

st.title("🔮 AI Chat with Nunno")
st.markdown(f"Chat with your personal finance AI assistant, {st.session_state.user_name}!")

# Display conversation history
st.markdown("### 💬 Conversation")

# Create a container for the chat messages
chat_container = st.container()

with chat_container:
    # Display all messages except system message
    for i, message in enumerate(st.session_state.conversation_history[1:], 1):
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant", avatar="🧠"):
                st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about finance..."):
    # Add user message to history
    user_message = {"role": "user", "content": prompt}
    st.session_state.conversation_history.append(user_message)
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant", avatar="🧠"):
        with st.spinner("Nunno is thinking..."):
            # Manage conversation history length
            managed_history = manage_history_length(st.session_state.conversation_history)
            
            # Get AI response
            response = ask_nunno(managed_history)
            
            # Display response
            st.markdown(response)
            
            # Add assistant message to history
            assistant_message = {"role": "assistant", "content": response}
            st.session_state.conversation_history.append(assistant_message)

# Sidebar controls
with st.sidebar:
    st.markdown("### 🔮 Chat Controls")
    
    if st.button("🗑️ Clear Chat History"):
        # Keep only the system message
        system_msg = st.session_state.conversation_history[0] if st.session_state.conversation_history else None
        st.session_state.conversation_history = [system_msg] if system_msg else []
        st.rerun()
    
    st.markdown(f"**Messages in history:** {len(st.session_state.conversation_history) - 1}")
    
    st.markdown("---")
    
    st.markdown("""
    ### 💡 Chat Tips:
    
    - Ask about investing basics
    - Get explanations of financial terms
    - Discuss trading strategies
    - Ask for market analysis
    - Request investment advice
    
    ### 🎯 Example Questions:
    
    - "What is DCA and how do I use it?"
    - "Should I invest in Bitcoin right now?"
    - "Explain what RSI means in trading"
    - "How do I start investing with $100?"
    - "What's the difference between stocks and crypto?"
    """)

# Quick suggestion buttons
st.markdown("### 🎯 Quick Questions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("What is DCA?"):
        st.session_state.conversation_history.append({"role": "user", "content": "What is DCA?"})
        st.rerun()

with col2:
    if st.button("How to start investing?"):
        st.session_state.conversation_history.append({"role": "user", "content": "How do I start investing?"})
        st.rerun()

with col3:
    if st.button("Explain RSI indicator"):
        st.session_state.conversation_history.append({"role": "user", "content": "Explain what RSI means in trading"})
        st.rerun()
