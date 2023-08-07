import openai
import streamlit as st

from elevenlabs import generate, play

openai.api_key = st.secrets.api_credentials.openapi_key
st.secrets.api_credentials.elevenlabsapi_key


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
    audio = generate(
        text=text,
        api_key=st.secrets.api_credentials.elevenlabsapi_key,
        voice="Arnold",
        model='eleven_multilingual_v1',
        stream=True
    )

    play(audio)
