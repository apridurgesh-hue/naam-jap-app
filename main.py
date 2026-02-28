import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io
from pydub import AudioSegment

# --- UI SETUP ---
st.set_page_config(page_title="Naam Jap Counter", page_icon="🙏")

st.title("🙏 Digital Naam Jap Counter")
st.write("Mic button dabayein, mantra bolein, phir stop karein.")

if 'count' not in st.session_state:
    st.session_state.count = 0

# Sidebar Settings
st.sidebar.header("Settings")
mantra = st.sidebar.text_input("Mantra to Track", "Ram").lower()
target = st.sidebar.number_input("Daily Target", value=108)

# Dashboard
col1, col2 = st.columns(2)
col1.metric("Current Count", st.session_state.count)
col2.metric("Remaining", max(0, target - st.session_state.count))
st.progress(min(st.session_state.count / target, 1.0))

# --- MICROPHONE RECORDER ---
audio_data = mic_recorder(
    start_prompt="🔴 Start Chanting",
    stop_prompt="⚪ Stop & Count",
    key='recorder'
)

if audio_data:
    audio_bytes = audio_data['bytes']
    
    try:
        # 1. Convert WebM/Ogg to WAV using pydub
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)

        # 2. Recognition using SpeechRecognition
        r = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio = r.record(source)
            text = r.recognize_google(audio, language='hi-IN').lower()
            
            st.info(f"Sunna gaya: {text}")
            
            if mantra in text:
                found = text.count(mantra)
                st.session_state.count += found
                st.success(f"Mantra pehchana gaya! +{found}")
                st.rerun()
            else:
                st.warning(f"Awaaz mein '{mantra}' nahi mila.")
                
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Tip: Thoda saaf bolein aur shant jagah par record karein.")

if st.button("Reset Counter"):
    st.session_state.count = 0
    st.rerun()
