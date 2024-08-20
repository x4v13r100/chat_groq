from groq import Groq
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("API_KEY_GROQ"))

def get_ai_response(messages):
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
        stream=True,
    )    
    response = "".join(chunk.choices[0].delta.content or "" for chunk in completion)
    return response

def chat():
    st.title("Chat with AI")
    st.write("Bienvenido al chat con IA GROQ ! Ingresa tu consulta:")
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
    def submit():
        user_input = st.session_state.user_input  
        if user_input.lower() == 'exit':
            st.write("Gracias por tu consulta ! Adios")
            st.stop()
            
        st.session_state['messages'].append({'role': 'user', 'content': user_input})

        with st.spinner("Generando respuesta..."):
            ai_response = get_ai_response(st.session_state['messages'])
            st.session_state['messages'].append({'role': 'assistant', 'content': ai_response})
            
        st.session_state.user_input = ""
    
    for message in st.session_state['messages']:
        role = "Tu" if message['role'] == 'user' else "Bot"
        st.write(f"**{role}:** {message['content']}")
    
    with st.form(key="chat_form", clear_on_submit=True):
        st.text_input("Tu:", key="user_input")
        submit_button = st.form_submit_button(label="Enviar", on_click=submit)
        
if __name__ == "__main__":
    chat()

#correr streamlit sobre un venv
#streamlit run main.py