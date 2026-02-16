import streamlit as st
import assemblyai as aai
import os

st.set_page_config(page_title="AI Subtitle Generator", page_icon="🎬")
st.title("🎬 AI Subtitle Generator")
st.write("Versi Fix: Teks lebih pendek & sinkron.")

try:
    aai.settings.api_key = st.secrets["AAI_KEY"]
except:
    st.error("API Key belum ada di Secrets!")

uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mov"])

if st.button("Mulai Proses") and uploaded_file:
    st.info("Lagi diproses... AI lagi dengerin & motong kalimat.")
    
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        # PERBAIKAN: Pakai 'punctuate' dan 'format_text'
        config = aai.TranscriptionConfig(
            speech_models=["universal-3-pro", "universal-2"], 
            language_code="id",
            punctuate=True,
            format_text=True
        )
        
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe("temp_video.mp4", config=config)
        
        if transcript.status == aai.TranscriptStatus.error:
            st.error(f"Error: {transcript.error}")
        else:
            # Kita kecilin lagi chars_per_caption ke 35 biar makin pendek
            srt_data = transcript.export_subtitles_srt(chars_per_caption=35)
            
            st.success("✅ Selesai!")
            st.download_button(
                label="⬇️ DOWNLOAD .SRT",
                data=srt_data,
                file_name="subtitle_fix.srt",
                mime="text/plain"
            )
            
    except Exception as e:
        st.error(f"Kesalahan: {e}")
    finally:
        if os.path.exists("temp_video.mp4"):
            os.remove("temp_video.mp4")