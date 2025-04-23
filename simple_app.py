#Importing the Streamlit library, which is used to build interactive web applications 
# for data science and machine learning projects in Python. The alias st is commonly used to access Streamlit's 
# functions for displaying text, widgets, charts, and handling user input in the app
import streamlit as st

# Importing the genai module from Google's Gen AI SDK. This library allows you to interact
#  with Google's generative AI models (like Gemini) and integrate their capabilities, such
#  as text generation, into your Python applications
from google import genai

# Imports Python’s built-in os module, which provides functions for interacting with the 
# operating system. This includes file and directory management, environment variables, and process management
import os

# Imports the gTTS (Google Text-to-Speech) class from the gtts library. This library provides an interface to Google
#  Translate’s text-to-speech API, allowing you to convert text into spoken audio (MP3 format) in Python
from gtts import gTTS

# Imports BytesIO from Python’s built-in io module. BytesIO allows you to create in-memory binary streams that behave like file objects.
#  This is useful for manipulating audio (such as MP3 data from gTTS) or other binary data without saving to disk
from io import BytesIO

from format import format_str
from speech import pronounce_word
from footer import footer_html



# Configure the Gemini API with your API key from environment variable
api_key = os.environ.get("GEMINI_API_KEY")


# Checks if the variable 'api_key' is empty or not set.
if not api_key:
    # Displays an error message in the Streamlit app to inform the user 
    # that the required API key is missing.
    st.error("Please set the GEMINI_API_KEY environment variable.")
    # Stops the execution of the Streamlit app immediately.
    # This prevents the rest of the code from running without the necessary API key.
    st.stop()


# Creates an instance of the Google GenAI Client using the provided API key.
# This client object is used to interact with Google's Gemini Developer API,
# allowing you to send requests for generative AI tasks such as text generation, chat, etc.
# The 'api_key' parameter authenticates your requests to the Gemini API.
client = genai.Client(api_key=api_key)


# Configure the default settings for the Streamlit app page.
# The 'layout' parameter controls how the app's content is displayed on the screen.
# Setting layout="wide" makes the app use the full width of the browser window,
# instead of the default centered column with fixed width.
# This is especially useful for apps with wide tables, charts, or dashboards.
# NOTE: This must be the first Streamlit command in your script (after imports)
# and can only be called once per app page.
st.set_page_config(layout="wide")


hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)



# Checks if screen is small (should be added near the top of your script)
# Inject a custom JavaScript snippet into the Streamlit app using st.markdown.
# The 'unsafe_allow_html=True' parameter allows raw HTML/JS to be rendered.
st.markdown("""
    <script>
            
    // Check if the browser window's width is less than 768 pixels (common breakpoint for mobile devices).
    if (window.innerWidth < 768) {
            
        // If so, it sends a message to the Streamlit frontend using window.parent.postMessage, setting a custom value (mobile_view: true).
        // This message uses the 'postMessage' API to notify Streamlit that the app is being viewed on a mobile device.
        // The message contains:
        //   - type: 'streamlit:setComponentValue' (Streamlit listens for this to set custom component values)
        //   - value: true (indicates mobile view is active)
        //   - key: 'mobile_view' (the key you can use in your Streamlit app to check for mobile view)
        // You can then use this value in your Streamlit Python code (with a custom component or callback) to adapt your app’s layout or features for mobile users
        // The * in the context of window.parent.postMessage(..., '*') is known as the wildcard target origin. It means that the message sent via postMessage can be received by a window from any origin, regardless of its domain, protocol, or port
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: true,
            key: 'mobile_view'
        }, '*');
    }
    </script>
    """, unsafe_allow_html=True)


# Checks if the key 'mobile_view' exists in Streamlit's session state.
# Streamlit's session_state is a dictionary-like object that persists values
# across reruns and user interactions within a single user's session.
if 'mobile_view' not in st.session_state:

    # If 'mobile_view' is not already set, initialize it to False.
    # This ensures that the app has a default value for mobile_view,
    # preventing KeyError exceptions when accessing it later.
    # You can later update this value (e.g., based on a JavaScript message)
    # to True if the app is being viewed on a mobile device.
    st.session_state.mobile_view = False


# Adjust column ratios for better responsiveness
# Check if the 'mobile_view' flag in the session state is True.
# The .get() method returns the value of 'mobile_view' if it exists,
# otherwise returns False as the default.
if st.session_state.get('mobile_view', False):

    # If the app is being viewed on a mobile device (mobile_view=True),
    # create two columns with equal width proportions.
    # This layout is simpler and optimized for smaller screens.
    col1, col2 = st.columns([1, 1])
else:

    # If the app is NOT in mobile view (desktop or larger screen),
    # create three columns with width ratios 1:3:1.
    # This layout typically centers the main content in the middle column (col2)
    # with narrower side columns (col1 and col3) for spacing or additional elements.
    # The 'gap="medium"' parameter adds medium spacing between these columns,
    # improving visual separation and readability on wider screens.
    col1, col2, col3 = st.columns([1, 3, 1], gap="medium")


format_str = format_str


def get_enhanced_meaning(word):
    """
    Queries the Gemini API for enhanced word meaning.
    
    Args:
        word (str): The word to look up.
    
    ### Constructs a detailed prompt for the Gemini model, instructing it to provide:
     - Simple definition and usage
     - Etymology
     - Pronunciation guidance
     - Part of speech
     - Verb forms (if applicable)
     - Derivative forms (noun, verb, adjective, adverb)
     - Example sentences
     - Common phrases with usage ratings and context
     - Structured output as specified by 'format_str'
     - Synonyms and antonyms under "Other Details"
    """
    
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

        # Calls the Gemini API's generate_content method using the specified model.
        # - 'model' specifies which Gemini model to use (here, 'gemini-2.0-flash').
        # - 'contents' is the prompt constructed above.
        # The API returns a response object with the generated text.
        response = client.models.generate_content(
                            model='gemini-2.0-flash',
                            contents=prompt
                        )
        
        # Returns the generated text from the model's response.
        return response.text
    except Exception as e:

        # If an error occurs (e.g., network, authentication, API quota, etc.),
        # catch the exception and return a user-friendly error message.
        return f"Error fetching information: {e}"


def get_pronunciation(word):
    """
    Fetches the pronunciation of a word.
    Args:
        word (str): The word to look up.

    ### Creates a prompt asking the Gemini model to provide:
     - A simple US English pronunciation for the given word
     - Indication of which syllable or part to stress
     - A similar-sounding word for reference
    """
    prompt = f"""Simple pronunciation in US English for word={word}. Tell which part to stress and a similar pronunciation word."""
    try:

        # Calls the Gemini API to generate content based on the prompt.
        # - 'model' specifies which Gemini model to use.
        # - 'contents' is the prompt string.
        # The API will return a response object containing the generated text.
        response = client.models.generate_content(
                            model='gemini-2.0-flash',
                            contents=prompt
                        )
        
        # Returns the generated pronunciation text from the response.
        return response.text
    except Exception as e:

        # If any exception occurs during the API call (e.g., network error, API limit, etc.),
        # return a user-friendly error message with the exception details.
        return f"Error fetching information: {e}"
    

# The @st.fragment decorator turns this function into a "fragment" in Streamlit.
# When a user interacts with any widget inside this fragment, only this function reruns,
# instead of the entire Streamlit script. This improves app performance and responsiveness,
# especially in apps with multiple interactive sections.
#
# Key features and behaviors:
# - Only the fragment function reruns when its widgets are interacted with.
# - The rest of the app remains unchanged during a fragment rerun.
# - This helps minimize unnecessary computations and UI updates elsewhere in the app.
# - Fragments make your code more modular and easier to maintain.
# - If you need to trigger a full app rerun from inside a fragment, use st.rerun().
# - Any state or values that need to be shared between fragments or with the main app
#   should be stored in st.session_state.
#
# For more details, see:
# https://docs.streamlit.io/develop/api-reference/execution-flow/st.fragment
@st.fragment
def pronunciation_section():

    # Displays a section heading for pronunciation learning.
    st.write("#### Learn Pronunciation")

    # Indicates the country/variant of English for pronunciation guidance.
    st.write("country: US")

    # Creates a text input box for the user to enter a word.
    # The 'key' ensures this input is uniquely identified in Streamlit's session state.
    word = st.text_input("Enter a word:", key="pronunciation_word")

    # If the user has entered a word:
    if word:

        # Show an informational message to indicate that pronunciation data is loading.
        load2 = st.info(f"Loading pronunciation...")

        # Fetches and displays the pronunciation details using the Gemini API.
        # The get_pronunciation function queries the API and returns a formatted response.
        st.write(get_pronunciation(word))

        # Calls a custom function to pronounce the word (likely plays audio).
        pronounce_word(word)

        # Updates the info message to indicate that the pronunciation is ready for the entered word.
        load2.info(f"Pronunciation for: {word}")


@st.fragment
def meaning_section():

    # Displays the main title of the section with an emoji for emphasis.
    st.title("✨ Go Beyond Word Meanings ✨")

    # Provides a brief description of what this section offers to the user.
    st.write("This is designed to help users learn English words in a comprehensive, engaging, and easy-to-understand format. It provides most common meaning of that word, example sentences, pronunciation guides, verb forms, and common phrases along with usage rating for any English word requested.")

    # Create a text input box for users to enter the word they want to look up.
    # The 'key' ensures this input is uniquely identified in Streamlit's session state.
    word_to_lookup = st.text_input("Enter a word:", key="lookup_word")
    
    # Only proceed if the user has entered a word.
    if word_to_lookup:

        # Displays an info message indicating that the search is in progress.
        a = st.info(f"Searching for: {word_to_lookup}...")

        # Queries the Gemini API (or your backend function) for the enhanced meaning of the word.
        gemini_output = get_enhanced_meaning(word_to_lookup)
        
        # If the API returns an error message, display it as an error in the UI.
        if gemini_output.startswith("Error"):
            st.error(gemini_output)
        else:

            # Update the info message to indicate that the result is ready.
            a.info(f"Result for: {word_to_lookup}")

            # Splits the output at the pronunciation section
            parts = gemini_output.split("### 📢 Pronunciation (US English):")

            if len(parts) == 2:

                # If the output contains a pronunciation section,
                # display the content before the pronunciation section.
                st.markdown(parts[0] + "### 📢 Pronunciation (US English):")

                # Insert pronunciation button here
                # Generate US English pronunciation audio for the word using gTTS.
                tts = gTTS(text=word_to_lookup, lang='en', tld='com')   # 'tld=com' ensures US accent
                mp3_fp1 = BytesIO()   # Create an in-memory file object for the audio.
                tts.write_to_fp(mp3_fp1)   # Write the TTS output to the in-memory file.
                mp3_fp1.seek(0)   # Reset the pointer to the start of the file.

                # Displays an audio player for the generated pronunciation audio.
                st.audio(mp3_fp1, format="audio/mp3")   

                # Inject custom CSS to control the audio player's width for better appearance.
                st.markdown("""
                    <style>
                    audio {
                        width: 120px !important;  /* Set your desired width */
                        min-width: 70px !important;
                        max-width: 350px !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)

                # Display the remaining part of the output (after the pronunciation section).
                st.markdown(parts[1])
            else:

                # If the output doesn't have a separate pronunciation section,
                # display the entire output as markdown.
                st.markdown(gemini_output)


# Places all Streamlit given elements inside the first column (col1).
with col1:

    # Create a container to group related elements together.
    audio_container = st.container()
    with audio_container:

        # Inject a custom HTML <div> to control the maximum width and handle overflow.
        # This can help ensure embedded elements (like audio players) do not exceed the column's width,
        # improving the layout especially on smaller screens.
        st.markdown('<div style="max-width:100%; overflow:hidden;">', unsafe_allow_html=True)

        # Calls the pronunciation_section fragment, which renders the pronunciation UI.
        pronunciation_section()

        # Close the custom HTML <div> tag.
        st.markdown('</div>', unsafe_allow_html=True)
        



def main():

    # Places all given Streamlit elements inside the second column (col2).
    # This is useful for multi-column layouts, where you want to separate
    # different sections of your app visually and functionally.
    with col2:

        # Call the meaning_section fragment, which renders the main word meaning
        # lookup UI and its features, such as definitions, examples, and pronunciation.
        meaning_section()



# ================================================== Footer ==================================================

# displays the content of footer_html in your Streamlit app, rendering any HTML and CSS it contains.
# st.markdown is a Streamlit function that displays text formatted as Markdown by default, but it can also render raw HTML if you set the unsafe_allow_html parameter to True.
# By default, HTML tags in the string are escaped (shown as plain text), but with unsafe_allow_html=True, Streamlit will interpret and render the HTML and CSS.
# This allows you to add custom HTML elements (like <div>, <style>, and <a> tags), CSS styling, and even external resources (like Font Awesome icons) to your app’s UI.
# In my specific case:
# footer_html contains HTML and CSS for a custom footer, including a fixed position, background color, and a LinkedIn icon.
# The line st.markdown(footer_html, unsafe_allow_html=True) injects this styled footer at the bottom of your Streamlit app, making it appear as a persistent, styled element across your app
st.markdown(footer_html, unsafe_allow_html=True)


# This conditional checks if the script is being run directly (not imported as a module).
# If true, it calls the main() function to start the Streamlit app.
# 
# - When you run this file directly (e.g., `streamlit run app.py`), __name__ is set to "__main__".
# - If the file is imported into another script, __name__ will be set to the module's name, 
#   and main() will NOT be called automatically.
# 
# This is a standard Python idiom for making code reusable and import-safe.
if __name__ == "__main__":
    main()
