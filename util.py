import openai
import streamlit as st
import requests
from streamlit.components.v1 import html

openai.api_key = st.secrets.api_credentials.openapi_key


def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    return response


def speak(text: str):

    chunk_size = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/kJwrKss0EAIKMz7FSU7r"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": st.secrets.api_credentials.elevenlabsapi_key
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.7
        }
    }

    response = requests.post(url, json=data, headers=headers)
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
