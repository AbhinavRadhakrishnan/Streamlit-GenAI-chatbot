from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq


#load env variables

load_dotenv() #here both the chatbot file and .env file are on same directory so no need f metioning the path inside the parenthisis

#streamlit page setup

st.set_page_config(
    page_title="ChatBot",
    layout="centered",
    page_icon=("🤖"),
)

st.markdown(
    """
    <h1 style='text-align: center;'>🗪 What can I help with?</h1>
    """,
    unsafe_allow_html=True
)

# ---- Side-by-side small subtitles ----
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        "<p style='font-size:16px; text-align:center;'>✍️ Help me write</p>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        "<p style='font-size:16px; text-align:center;'>📘 Explain concepts</p>",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        "<p style='font-size:16px; text-align:center;'>➕ More</p>",
        unsafe_allow_html=True
    )
#initiate chat history

if "chat_history" not in st.session_state: # we use session state becuase when user interacts with the bot the entire streamlit scripts is gonna rerun
    #and if we simple make a chat_histroy list the variables stored in it will also get refreshed so thats why we use session
    #it will keep the varibles  same unless we refres the entire page
    st.session_state.chat_history = [] #initiated chat_history

#show the chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]): # it will automatically show an emoji according to role
        st.markdown(message["content"])

#llm initiate

llm = ChatGroq(
    model= "llama-3.1-8b-instant",
    temperature=0 # want similar value as value increases the answer we get would be more creative each time
)

#input box

user_prompt = st.chat_input("Ask Something")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user","content": user_prompt})

    response = llm.invoke(
        input = [{"role" : "system" , "content" : "you are an helpful assistant"}, *st.session_state.chat_history]

    )
    assistant_response = response.content
    st.session_state.chat_history.append({"role" : "assistant","content" : assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
 