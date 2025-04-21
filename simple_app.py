import streamlit as st
from google import genai
import os

# Configure the Gemini API with your API key from environment variable

api_key = os.environ.get("GEMINI_API_KEY")


if not api_key:
    st.error("Please set the GEMINI_API_KEY environment variable.")
    st.stop()

client = genai.Client(api_key=api_key)

st.set_page_config(layout="wide")
col1, col2, col3 = st.columns([1, 3, 1])

format_str = """

---

### 🧠 Word: *<word goes here>*

---

### ✅ Most Common Usage & Meaning:

#### As an Adjective:
*Abstract* means not concrete or physical; existing in thought or as an idea.  
📘 *Example:* *Love and freedom are abstract concepts.*

#### As a Noun:
An *abstract* is a short summary of a larger text, like a research paper.  
📘 *Example:* *The abstract gives a brief overview of the article.*

#### As a Verb (less common):
To *abstract* means to take away or remove something.  
📘 *Example:* *He abstracted the data from the report.*

---

### 📢 Pronunciation (US English):

- **As a noun/adjective:** pronunciation goes here
- **As a verb:** pronunciation goes here

---

### 🌱 Part of Speech:

- Adjective  
- Noun  
- Verb

---

### 📘 First, Second, and Third Forms (Verb):

- **Base (V1):** abstract  
- **Past Simple (V2):** abstracted  
- **Past Participle (V3):** abstracted

---

### ✨ Other Forms of Speech:

- **Noun:** *abstraction* 👉 *Mathematics often deals in abstraction.*  
- **Adjective:** *abstract* 👉 *She gave an abstract explanation.*  
- **Verb:** *to abstract* 👉 *They abstracted the key ideas.*  
- **Adverb:** *abstractly* 👉 *He spoke abstractly about life.*

---

### ✏️ Example Sentences:

#### As Adjective:
1. *Justice is an abstract concept.*  
2. *He struggled with the abstract ideas in the lecture.*

#### As Noun:
3. *I read the abstract of the journal article before the full paper.*  
4. *The abstract was too vague to understand the full research.*

#### As Verb:
5. *He abstracted the key points from the book.*

---

### 🐦‍🔥 Past, Present and Future Sentences:

1. *<Past tense sentence example goes here>*  
2. *<Present tense sentence example goes here>*
3. *<Future tense sentence example goes here>*  

---

### 📌 Common Phrases with “Abstract”:

#### 1. **Abstract concept**
- **Meaning:** An idea that doesn’t have a physical form.  \n
- **Example:** Justice and equality are abstract concepts that vary across cultures.  \n
- **Usage Rating:** ⭐⭐⭐⭐⭐ (5/5)  
- **Common In:** *Philosophy / Education / Psychology*

#### 2. **Abstract art**
- **Meaning:** A style of art that doesn’t show realistic objects, focusing instead on shapes, colors, and forms.  
- **Example:** The museum’s new exhibit features abstract art that challenges traditional perceptions of beauty. 
- **Usage Rating:** ⭐⭐⭐⭐⭐ (5/5)  
- **Common In:** *Fine Arts / Design / Museums*

#### 3. **Research abstract**
- **Meaning:** A short summary of a research paper.  
- **Example:** Before diving into the full paper, she carefully read the research abstract to grasp the key findings.
- **Usage Rating:** ⭐⭐⭐⭐ (4/5)  
- **Common In:** *Academia / Science / Research*

#### 4. **Abstract thinking**
- **Meaning:** The ability to think about things that are not physically present.  
- **Example:** Children develop the ability for abstract thinking as they grow, enabling them to solve complex problems.
- **Usage Rating:** ⭐⭐⭐⭐ (4/5)  
- **Common In:** *Psychology / Education / Cognitive Science*

---

     """




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
        # response = model.generate_content(prompt)
        response = client.models.generate_content(
                            model='gemini-2.0-flash',
                            contents=prompt
                        )
        return response.text
    except Exception as e:
        return f"Error fetching information: {e}"



def main():
    with col2:
        st.title("✨ Go Beyond Word Meaning ✨")
        
        st.write("This is designed to help users learn English words in a comprehensive, engaging, and easy-to-understand format. It provides most common meaning of that word, example sentences, pronunciation guides, verb forms, and common phrases along with usage rating for any English word requested.")

        word_to_lookup = st.text_input("Enter a word:")
        

        if word_to_lookup:
            a = st.info(f"Searching for: **{word_to_lookup}**...")
            gemini_output = get_enhanced_meaning(word_to_lookup)

            if gemini_output.startswith("Error"):
                st.error(gemini_output)
            else:
                a.info(f"Result for: **{word_to_lookup}**")
                st.markdown(gemini_output)


if __name__ == "__main__":
    main()
