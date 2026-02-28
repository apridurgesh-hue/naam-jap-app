import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io

# --- UI SETUP ---
st.set_page_config(page_title="Naam Jap Counter", page_icon="🙏")

st.title("🙏 Digital Naam Jap Counter")
st.write("Niche mic button dabayein aur apna Mantra bolein.")

# Session State for Counter
if 'count' not in st.session_state:
    st.session_state.count = 0

# Sidebar Settings
st.sidebar.header("Settings")
mantra = st.sidebar.text_input("Mantra to Track", "Ram").lower()
target = st.sidebar.number_input("Daily Target", value=108)

# Main Dashboard
col1, col2 = st.columns(2)
col1.metric("Current Count", st.session_state.count)
col2.metric("Remaining", max(0, target - st.session_state.count))

st.progress(min(st.session_state.count / target, 1.0))

# --- MICROPHONE RECORDER ---
st.write("### 🎤 Record your Chant")
audio_data = mic_recorder(
    start_prompt="🔴 Start Chanting",
    stop_prompt="⚪ Stop & Count",
    key='recorder'
)

if audio_data:
    # Processing the audio
    r = sr.Recognizer()
    audio_bytes = audio_data['bytes']
    
    with io.BytesIO(audio_bytes) as audio_file:
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
            try:
                # Recognize voice
                text = r.recognize_google(audio, language='hi-IN').lower()
                st.info(f"Sunna gaya: {text}")
                
                if mantra in text:
                    found = text.count(mantra)
                    st.session_state.count += found
                    st.success(f"Added +{found} to your count!")
                    st.rerun()
                else:
                    st.warning(f"Mantra '{mantra}' nahi pehchana gaya. Phir se koshish karein.")
            except:
                st.error("Awaaz samajh nahi aayi. Mic ke paas bolein.")

if st.button("Reset Counter"):
    st.session_state.count = 0
    st.rerun()

st.markdown("---")
st.caption("Tip: Ek baar mein 5-10 baar mantra bolein, phir stop karein.")
