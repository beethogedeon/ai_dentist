import openai
import streamlit as st
from elevenlabslib import *

openai.api_key = st.secrets.api_credentials.openapi_key
user = ElevenLabsUser(st.secrets.api_credentials.elevenlabsapi_key)


def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    return response


def speak(text: str, voice_name: str):

    voice = user.get_voices_by_name(voice_name)[0]  # This is a list because multiple voices can have the same name
    voice.play_preview(playInBackground=True)
    voice.generate_play_audio_v2(text, playbackOptions=PlaybackOptions(runInBackground=True), generationOptions=GenerationOptions(model_id="eleven_multilingual_v1"))

