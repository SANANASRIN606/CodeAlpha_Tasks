import streamlit as st
import requests

st.set_page_config(page_title="Language Translation Tool", layout="centered")
st.title("Language Translation Tool")

# Added Malayalam ('ml') to supported languages
LANGUAGES = {
    "English": "en",
    "Malayalam": "ml",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Italian": "it",
    "Arabic": "ar",
    "Japanese": "ja"
}

# 1. UI: Select source & target languages
col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("Source Language", list(LANGUAGES.keys()), index=0)
with col2:
    # Set default target language to Malayalam (index 1)
    target_lang = st.selectbox("Target Language", list(LANGUAGES.keys()), index=1)

# 2. UI: Input text
input_text = st.text_area("Enter text to translate:", height=150)

def query_translation_api(text, sl_code, tl_code):
    """Sends text to the translation API and returns translated output."""
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": f"{sl_code}|{tl_code}"
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    if data.get("responseStatus") == 200:
        return data["responseData"]["translatedText"]
    else:
        raise Exception(data.get("responseDetails", "Failed to translate"))

# 3. Trigger translation API call
if st.button("Translate", type="primary"):
    if not input_text.strip():
        st.warning("Please enter some text before translating.")
    elif src_lang == target_lang:
        st.warning("Source and Target languages must be different.")
    else:
        with st.spinner("Processing via Translation API..."):
            try:
                translated_result = query_translation_api(
                    text=input_text,
                    sl_code=LANGUAGES[src_lang],
                    tl_code=LANGUAGES[target_lang]
                )
                
                # 4. Display translated output clearly on screen
                st.success("Translated Output:")
                st.text_area("Result", value=translated_result, height=150)
                
            except Exception as e:
                st.error(f"API Error: {e}")
