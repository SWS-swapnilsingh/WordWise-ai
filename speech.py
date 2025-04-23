# import streamlit as st
# from google import genai
# from gtts import gTTS

# # st.set_page_config(layout="wide")
# # st.title("US English Pronunciation")

# # word = st.text_input("Enter a word to hear its US English pronunciation:")
# def pronounce_word2(word):
#     tts = gTTS(text=word, lang='en', tld='com')  # 'com' gives US accent
#     tts.save("pronounce.mp3")
#     audio_file = open("pronounce.mp3", "rb")
#     st.audio(audio_file.read(), format="audio/mp3")


# ------------------------------------------------------------------

# Imports the gTTS (Google Text-to-Speech) class from the gtts library. This library provides an interface to Google
#  Translate’s text-to-speech API, allowing you to convert text into spoken audio (MP3 format) in Python
from gtts import gTTS

# Imports BytesIO from Python’s built-in io module. BytesIO allows you to create in-memory binary streams that behave like file objects.
#  This is useful for manipulating audio (such as MP3 data from gTTS) or other binary data without saving to disk
from io import BytesIO

#Importing the Streamlit library, which is used to build interactive web applications 
# for data science and machine learning projects in Python. The alias st is commonly used to access Streamlit's 
# functions for displaying text, widgets, charts, and handling user input in the app
import streamlit as st


def pronounce_word(word):

    # Generate US English pronunciation audio for the word using gTTS.
    tts = gTTS(text=word, lang='en', tld='com')   # 'tld=com' ensures US accent
    mp3_fp = BytesIO()   # Create an in-memory file object for the audio.
    tts.write_to_fp(mp3_fp)   # Write the TTS output to the in-memory file.
    mp3_fp.seek(0)   # Reset the pointer to the start of the file.

    st.markdown("""
                    <style>
                    audio {
                        width: 120px !important;  /* Set your desired width */
                        min-width: 70px !important;
                        max-width: 350px !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)
    
    # Displays an audio player for the generated pronunciation audio.
    st.audio(mp3_fp, format="audio/mp3", autoplay=False)


