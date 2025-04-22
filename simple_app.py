import streamlit as st
from google import genai
import os
from format import format_str
from speech import pronounce_word
from gtts import gTTS
from io import BytesIO

# Configure the Gemini API with your API key from environment variable

api_key = os.environ.get("GEMINI_API_KEY")


if not api_key:
    st.error("Please set the GEMINI_API_KEY environment variable.")
    st.stop()

client = genai.Client(api_key=api_key)


st.set_page_config(layout="wide")
# col1, col2, col3 = st.columns([1, 3, 1], gap="medium")

# Check if screen is small (add this near the top of your script)
st.markdown("""
    <script>
    if (window.innerWidth < 768) {
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: true,
            key: 'mobile_view'
        }, '*');
    }
    </script>
    """, unsafe_allow_html=True)

# Initialize session state for mobile view
if 'mobile_view' not in st.session_state:
    st.session_state.mobile_view = False


# Adjust column ratios for better responsiveness
if st.session_state.get('mobile_view', False):
    col1, col2 = st.columns([1, 1])
else:
    col1, col2, col3 = st.columns([1, 3, 1], gap="medium")

format_str = format_str

def get_enhanced_meaning(word):
    """Queries the Gemini API for enhanced word meaning."""
    # prompt = f"Provide a detailed definition, example sentences, and relevant synonyms for the word '{word}'."
    prompt = f""" 

            1. Give the most common usage and meaning of the word in English. Use simple English. Do not use any technical terms. Do not use any complex words.

            2. Give the Etymology of the word. Where does it come from?

            3. Simple pronunciation in US English. Tell which part to stress and a similar pronunciation word.

            4. Tell the part of speech. For example: noun, verb, adjective, etc.

            5. First, Second, and Third forms of that word. This applies to verbs. Example: go – went – gone.

            6. How can other forms of speech be created from it? Show how the word can become a noun, verb, adjective, adverb, etc., and give those forms.

            7. Some number of example sentences. Use simple, useful sentences that help in understanding the word in context.

            8. Common phrases of this word and their meaning. Meaning of each phrase. A usage rating out of 5 (5 = very common, 1 = rare). Give one example sentence. Mention industries or topics where that phrase is mostly used (e.g., business, education, casual speech, technology, etc.)

            9. Present the result in a structured format={format_str}.

            10. Add Synonyms and Antonyms under heading "Other Details".

            word: {word}
            """
    

    try:
        response = client.models.generate_content(
                            model='gemini-2.0-flash',
                            contents=prompt
                        )
        return response.text
    except Exception as e:
        return f"Error fetching information: {e}"


# with col1:
#     st.write("#### Pronunciation")
#     st.write("country: US")
#     # st.write("Tcomprehensive, engaging, and easy-to-understand format. It provides most common meaning of that word, example sentences, pronunciation guides, verb forms, and common phrases along with usage rating for any English word requested.")
#     word = st.text_input("Enter word:", key="pronunciation_word")
#     pronounce_word(word)


def get_pronunciation(word):
    """Fetches the pronunciation of a word."""
    prompt = f"""Simple pronunciation in US English for word={word}. Tell which part to stress and a similar pronunciation word."""
    try:
        response = client.models.generate_content(
                            model='gemini-2.0-flash',
                            contents=prompt
                        )
        return response.text
    except Exception as e:
        return f"Error fetching information: {e}"
    

@st.fragment
def pronunciation_section():
    st.write("#### Pronunciation")
    st.write("country: US")
    word = st.text_input("Enter word:", key="pronunciation_word")
    st.write("**Note:** Downloading audio is available.")

    if word:
        load2 = st.info(f"Loading pronunciation...")
        st.write(get_pronunciation(word))
        pronounce_word(word)
        load2.info(f"Pronunciation for: **{word}**")


@st.fragment
def meaning_section():
    st.title("✨ Go Beyond Word Meaning ✨")
    st.write("This is designed to help users learn English words in a comprehensive, engaging, and easy-to-understand format. It provides most common meaning of that word, example sentences, pronunciation guides, verb forms, and common phrases along with usage rating for any English word requested.")
    word_to_lookup = st.text_input("Enter a word:", key="lookup_word")
    
    if word_to_lookup:
        a = st.info(f"Searching for: **{word_to_lookup}**...")
        gemini_output = get_enhanced_meaning(word_to_lookup)
        
        if gemini_output.startswith("Error"):
            st.error(gemini_output)
        else:
            a.info(f"Result for: **{word_to_lookup}**")
            # st.markdown(gemini_output)

            # Split the output at the pronunciation section
            parts = gemini_output.split("### 📢 Pronunciation (US English):")

            if len(parts) == 2:
                st.markdown(parts[0] + "### 📢 Pronunciation (US English):")
                # Insert pronunciation button here

                tts = gTTS(text=word_to_lookup, lang='en', tld='com')  # US accent
                mp3_fp1 = BytesIO()
                tts.write_to_fp(mp3_fp1)
                mp3_fp1.seek(0)
                st.audio(mp3_fp1, format="audio/mp3")
                # Inject custom CSS to control the audio player's width
                st.markdown("""
                    <style>
                    audio {
                        width: 120px !important;  /* Set your desired width */
                        min-width: 70px !important;
                        max-width: 350px !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)

                # st.markdown('<div id="audio1-container">', unsafe_allow_html=True)
                # st.audio(mp3_fp1, format="audio/mp3", autoplay=False)
                # st.markdown('</div>', unsafe_allow_html=True)
                # st.markdown("""
                #     <style>
                #     #audio1-container audio {
                #         width: 220px !important;
                #         min-width: 120px !important;
                #         max-width: 250px !important;
                #         /* Any other custom styles */
                #     }
                #     </style>
                #     """, unsafe_allow_html=True)


                st.markdown(parts[1])
            else:
                st.markdown(gemini_output)

            # if st.button("🔊"):
            # tts = gTTS(text=word_to_lookup, lang='en', tld='com')  # 'com' gives US accent
            # tts.save("pronounce.mp3")
            # audio_file = open("pronounce.mp3", "rb")
            # st.audio(audio_file.read(), format="audio/mp3")



with col1:
    # pronunciation_section()
    audio_container = st.container()
    with audio_container:
        st.markdown('<div style="max-width:100%; overflow:hidden;">', unsafe_allow_html=True)
        pronunciation_section()
        st.markdown('</div>', unsafe_allow_html=True)
        



def main():
    # with col2:
    #     st.title("✨ Word Meaning Explorer ✨")
        
    #     st.write("This is designed to help users learn English words in a comprehensive, engaging, and easy-to-understand format. It provides most common meaning of that word, example sentences, pronunciation guides, verb forms, and common phrases along with usage rating for any English word requested.")
        
    #     word_to_lookup = st.text_input("Enter a word:", key="lookup_word")
        

    #     if word_to_lookup:
    #         a = st.info(f"Searching for: **{word_to_lookup}**...")
    #         gemini_output = get_enhanced_meaning(word_to_lookup)

    #         if gemini_output.startswith("Error"):
    #             st.error(gemini_output)
    #         else:
    #             a.info(f"Result for: **{word_to_lookup}**")
    #             st.markdown(gemini_output)

    
    with col2:
        meaning_section()



if __name__ == "__main__":
    main()



footer_html = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background: #222;
    color: #fff;
    text-align: center;
    padding: 15px 0;
    z-index: 100;
}
.footer a {
    color: #fff;
    margin: 0 10px;
    text-decoration: none;
}
</style>
<div class="footer">
    <span>Created with ♥️ by Swapnil Singh</span>
    <a href="https://www.linkedin.com/in/swapnil-singh-b995a9184/" target="_blank"><i class="fab fa-linkedin"></i></a>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
