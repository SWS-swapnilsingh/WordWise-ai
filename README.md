## ✨ Go Beyond Word Meanings ✨ – Streamlit App

A modern, interactive Streamlit web app that helps users learn English words in a comprehensive, engaging, and easy-to-understand format. Powered by Google's Gemini API and Google Text-to-Speech (gTTS), this app provides simple definitions, usage examples, pronunciation guides (with audio), verb forms, etymology, and much more for any English word.

---

### Features

- **Comprehensive Word Lookup:**  
  Get the most common meaning, simple definition, example sentences, part of speech, etymology, and verb forms for any English word.

- **Pronunciation Guidance:**  
  See and hear US English pronunciation for any word, with stress guidance and similar-sounding words.

- **Common Phrases with Usage:**  
  Discover phrases using the word, with usage frequency, context (business, casual, etc.), and example sentences.

- **Synonyms & Antonyms:**  
  Find related words and opposites for richer vocabulary.

- **Mobile-Friendly & Responsive:**  
  The layout adapts for mobile and desktop, ensuring a smooth experience everywhere.

- **Audio Pronunciation:**  
  Listen to correct US English pronunciation via gTTS-powered audio.

---

### How It Works

1. **Word Meaning Section:**  
   - Enter an English word.
   - Instantly receive a structured, easy-to-read summary: definition, usage, etymology, verb forms, example sentences, phrases, synonyms, antonyms, and more.

2. **Pronunciation Section:**  
   - Enter a word.
   - See a text-based pronunciation guide (with stress and similar word).
   - Listen to the word pronounced in US English.

---

### Tech Stack

- [Streamlit](https://streamlit.io/) – for interactive web UI
- [Google Gemini API](https://ai.google.dev/) – for generative AI-powered explanations
- [gTTS (Google Text-to-Speech)](https://gtts.readthedocs.io/) – for generating pronunciation audio
- Python standard libraries (`os`, `io`)
- Custom modules: `format.py`, `speech.py`, `footer.py`

---

### Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Gemini API key:**
   - Obtain a Gemini API key from [Google AI Studio](https://ai.google.dev/).
   - Set the environment variable:
     ```bash
     export GEMINI_API_KEY="your_api_key_here"
     ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

---

### File Structure

```
.
├── app.py             # Main Streamlit app (your provided code)
├── format.py          # Formatting helpers for structured output
├── speech.py          # Pronunciation audio helpers
├── footer.py          # Custom HTML/CSS for app footer
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

---

### Environment Variables

- `GEMINI_API_KEY` – Your Google Gemini API key (required)

---

### Contributing

Pull requests and suggestions are welcome! Please open an issue or submit a PR for improvements.

---
