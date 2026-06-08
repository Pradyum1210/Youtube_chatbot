import streamlit as st
from dotenv import load_dotenv

from utils.transcript import get_transcript
from utils.vector_store import create_vector_store
from utils.chain import create_chain


load_dotenv()

st.set_page_config(
    page_title="YouTube Chatbot",
    page_icon="🎥",
    layout="wide"
)

# ---------------- UI Design ---------------- #

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #FF4B4B;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #B0B0B0;
    margin-bottom: 40px;
}

.stTextInput > div > div > input {
    background-color: #262730;
    color: white;
    border-radius: 10px;
}

.stTextArea textarea {
    background-color: #262730;
    color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">🎥 YouTube Chatbot</div>',
    unsafe_allow_html=True
)


# ---------------- Session State ---------------- #

if "chain" not in st.session_state:
    st.session_state.chain = None

if "processed" not in st.session_state:
    st.session_state.processed = False

# ---------------- Video Section ---------------- #

st.markdown("## 📹 Video Processing")

video_id = st.text_input(
    "Enter YouTube Video ID",
    placeholder="Example: Gfr50f6ZBvo"
)

language_options = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh",
    "Russian": "ru"
}

selected_language = st.selectbox(
    "Select Video Language",
    list(language_options.keys())
)

language = language_options[selected_language]

# ---------------- Process Button ---------------- #

if st.button("Process Video"):

    if not video_id or not language:
        st.warning("Please enter both Video ID and Language")
    else:

        with st.spinner("Fetching transcript..."):

            transcript = get_transcript(video_id, language)

        if transcript is None:
            st.error("Transcript not available for this language.")
        else:

            with st.spinner("Creating vector store..."):

                vector_store = create_vector_store(transcript)

            retriever = vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )

            chain = create_chain(retriever)

            st.session_state.chain = chain
            st.session_state.processed = True

            st.success("Video Processed Successfully")

# ---------------- Question Section ---------------- #

if st.session_state.processed:

    st.markdown("---")
    st.markdown("## 💬 Ask Questions")

    question = st.text_area(
        "Ask your question from the video"
    )

    if st.button("Generate Answer"):

        if question:

            with st.spinner("Generating answer..."):

                response = st.session_state.chain.invoke(question)

            st.markdown("### ✅ Answer")
            st.write(response)

        else:
            st.warning("Please enter a question")