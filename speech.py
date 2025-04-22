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

from gtts import gTTS
from io import BytesIO
import streamlit as st


def pronounce_word(word):
    # if st.button("🔊 Pronounce") and word:
    # loading
    # load1 = st.info("Loading pronunciation...")

    tts = gTTS(text=word, lang='en', tld='com')  # US accent
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    st.audio(mp3_fp, format="audio/mp3", autoplay=False)
    st.markdown("""
                    <style>
                    audio {
                        width: 120px !important;  /* Set your desired width */
                        min-width: 70px !important;
                        max-width: 350px !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)
    # load1.empty()

