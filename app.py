import streamlit as st
import assemblyai as aai
import os

st.set_page_config(page_title="AI Subtitle Generator", page_icon="🎬")
st.title("🎬 AI Subtitle Generator")
st.write("Subtitle sekarang lebih pendek dan lebih pas!")

try:
    aai.settings.api_key = st.secrets["AAI_KEY"]
except:
    st.error("API Key belum ada di Secrets!")

uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mov"])

if st.button("Mulai Proses") and uploaded_file:
    st.info("Lagi diproses... AI lagi motong-motong kalimat biar gak kepanjangan.")
    
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        # SETTING BIAR TEKS PENDEK & SINKRON
        config = aai.TranscriptionConfig(
            speech_models=["universal-3-pro", "universal-2"], 
            language_code="id",
            punctuation=True,
            format_text=True
        )
        
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe("temp_video.mp4", config=config)
        
        if transcript.status == aai.TranscriptStatus.error:
            st.error(f"Error: {transcript.error}")
        else:
            # chars_per_caption=40 biar teksnya pendek (sekitar 1 baris)
            # Ini yang bikin teks nggak numpuk kepanjangan
            srt_data = transcript.export_subtitles_srt(chars_per_caption=40)
            
            st.success("✅ Selesai!")
            st.download_button(
                label="⬇️ DOWNLOAD .SRT",
                data=srt_data,
                file_name="subtitle_pendek.srt",
                mime="text/plain"
            )
            
    except Exception as e:
        st.error(f"Kesalahan: {e}")
    finally:
        if os.path.exists("temp_video.mp4"):
            os.remove("temp_video.mp4")