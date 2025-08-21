import streamlit as st 
#here were using a python library for web framework dashboard 

import os
from groq import Groq

client = Groq(api_key = os.environ["GROQ_API_KEY"])

st.title("There Goes My Hero Copilot!")
#st is a streamlit function

tab_names = ["Overview", "Events", "Ask the data"]
tabs = st.tabs(tab_names)
#created 3 different tabs in streamlit

tab_overview = tabs[0]
tab_events = tabs[1]
tab_chat = tabs[2]

with tab_overview:
    st.subheader("Overview coming soon..")
    st.write("this tab will contain links for donations, volunteering, etc.")
    
with tab_events:
    st.subheader("Events coming soon...")
    st.write("This tab will show upcoming and past events.")

#session_state used here but it survives the app reruns 
with tab_chat:
    st.subheader("CHATBOT")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    
    for role, text in st.session_state.messages:
        with st.chat_message(role): #role controls look, markdown text controls content
            st.markdown(text) #this block makes sure that the chatbot doesnt forget past messages and so still on display
            
                        
    user_text = st.chat_input("Ask a question about There Goes my Hero")
    
    
    #if you typed something, shows a bubble + previous bubbles
    if user_text:
        st.session_state.messages.append(("user", user_text))
        
        with st.chat_message("user"):
            st.markdown(user_text)
    
    #added chatbot      
    with st.chat_message("assistant"):
        try:
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for There Goes My Hero. A nonprofit organization based in Baltimore, MD. We do bone marrow drives for cancer patients, meals for heroes at hackerman patz and Ulman house. Davi is the best volunteer coordinator. maker of this chatbot mahi thakar. limit your answers to 5 lines. also try getting people to volunteer and sponsor. say Email davi@theregoesmyhero.org for volunteering/sponsoring anything. Erik is the founder who himself had cancer then a 19 year old girl from germany donated her bone marrow. Be concise and truthful."},
                    *[
                        {"role": r, "content": c}
                        for (r, c) in st.session_state.messages
                    ],
                ],
                temperature=0.3,
            )
            answer = resp.choices[0].message.content
        except Exception as e:
            answer = f"Oops, model error: {e}"

        st.markdown(answer)

st.session_state.messages.append(("assistant", answer))
