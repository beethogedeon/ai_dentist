import streamlit as st
from streamlit_chat import message
from util import generate_response, speak

st.title("Dental Assistant")
st.write("This is a demo of a virtual dental assistant. You can ask it questions about toothaches and it will respond with a diagnosis and recommended actions.")
st.info("This assistant is powered by Gedeon Gbedonou")
# container for chat history
response_container = st.container()
# container for text box
container = st.container()

if 'already_speak' not in st.session_state:
    st.session_state["already_speak"] = []

# Initialise session state variables
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a virtual dantist assistant. You are a symptom checker for users with toothaches. You needs to ask users a series of questions and record the answers. Specifically, there are about 20 questions that need to be asked. They should be asked one at a time. The user experience should be conversational - like human were chatting with a dentist. Answers to the questions should then be summarized in a specific format. The user will be asked to approved the accuracy of the summary. Once the summary is verified by the user, based on the summary to be given to you in additional to a dental diagnosis training document that will guide you to generate an accurate diagnosis and recommended actions for the user concerning their toothache."}
    ]

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))

        if not (len(st.session_state['generated']) - 1 in st.session_state['already_speak']):
            speak(st.session_state["generated"][len(st.session_state['generated']) - 1])
            st.session_state['already_speak'].append(len(st.session_state['generated']) - 1)

