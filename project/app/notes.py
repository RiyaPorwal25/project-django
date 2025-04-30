import re
import nltk
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import spacy
from docx import Document
from io import BytesIO
from googletrans import Translator  # Import Translator for language conversion
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Download NLTK resources
nltk.download('punkt')

# Load the English NLP model from spaCy
nlp = spacy.load("en_core_web_sm")

# Initialize the Google Translator
translator = Translator()

def get_video_id_from_url(url):
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        return None

def get_youtube_transcript(video_url, languages):
    try:
        video_id = get_video_id_from_url(video_url)
        if not video_id:
            return "Invalid YouTube URL"
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        formatter = TextFormatter()
        return formatter.format_transcript(transcript_list)
    except Exception as e:
        return f"Error: {e}"

def neutralize_text(text):
    subjective_words = ['I', 'me', 'my', 'you', 'your', 'he', 'him', 'his', 'she', 'her', 'we', 'us', 'our', 'they', 'them', 'their']
    words = text.split()
    return ' '.join([word for word in words if word not in subjective_words])

def summarize_text(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 2)  # Summarize to 2 sentences
    return ' '.join(str(sentence) for sentence in summary)

def extract_key_points(summary_text):
    doc = nlp( summary_text)
    key_points = []
    for sent in doc.sents:
        if len(sent.text.split()) > 5:  # Filter out very short sentences
            key_points.append(sent.text)
    return key_points

def generate_word(text):
    doc = Document()
    doc.add_paragraph(text)
    word_output = BytesIO()
    doc.save(word_output)
    word_output.seek(0)
    return word_output

def translate_to_hindi(text):
    try:
        translated = translator.translate(text, src='en', dest='hi')  # Synchronous call
        return translated.text
    except Exception as e:
        return f"Translation Error: {e}"

# Initialize session state variables
if "transcript" not in st.session_state:
    st.session_state.transcript = None
if "translated_transcript" not in st.session_state:
    st.session_state.translated_transcript = None

st.title("YouTube Video Information Extraction and Summarization Tool")
video_url = st.text_input("Enter YouTube Video URL:", "", key="video_url")
languages = ['en', 'fr', 'hi']

if st.button("Process Video"):
    transcript = get_youtube_transcript(video_url, languages)
    if "Error" not in transcript and "Invalid" not in transcript:
        st.session_state.transcript = transcript  # Store transcript in session state
        neutralized = neutralize_text(transcript)
        summary = summarize_text(transcript)
        key_points = extract_key_points(transcript)
        
        col1, col2 = st.columns([4.5, 4.5])

        with col1:
            st.subheader("Neutralized Text")
            st.text_area("", neutralized, height=400, key="neutralized_text")
        with col2:
            st.subheader("Summary")
            st.text_area("", summary, height=400, key="summary_text")
            st.subheader("Key Points")
            st.text_area("", "\n".join(key_points), height=400, key="key_points_text")
        
        # Add download button for Word file only
        st.subheader("Download Options")
        word_file = generate_word(transcript)
        st.download_button(
            label="Download Transcript as Word",
            data=word_file,
            file_name="transcript.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.error(transcript)

# Add translation button
if st.session_state.transcript:  # Ensure transcript exists before showing the translation button
    if st.button("Translate Transcript to Hindi"):
        st.session_state.translated_transcript = translate_to_hindi(st.session_state.transcript)

    if st.session_state.translated_transcript:
        st.subheader("Translated Transcript (Hindi)")
        st.text_area("", st.session_state.translated_transcript, height=400, key="translated_text")